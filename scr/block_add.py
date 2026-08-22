from __future__ import annotations

import torch
from torch import Tensor, nn

__all__ = ["CoordinateAttention"]


class CoordinateAttention(nn.Module):

    def __init__(self, channels: int, reduction: int = 32) -> None:
        super().__init__()

        if not isinstance(channels, int) or channels <= 0:
            raise ValueError(f"channels must be a positive integer, got {channels!r}")
        if not isinstance(reduction, int) or reduction <= 0:
            raise ValueError(
                f"reduction must be a positive integer, got {reduction!r}"
            )

        self.channels = channels
        self.reduction = reduction
        reduced_channels = max(1, channels // reduction)

        # Shared F1 in equation (6): C -> C/r.
        self.conv_shared = nn.Conv2d(
            channels,
            reduced_channels,
            kernel_size=1,
            stride=1,
            padding=0,
            bias=False,
        )
        self.bn = nn.BatchNorm2d(reduced_channels)

        # Paper 13 explicitly uses ReLU as delta in equation (6).
        self.relu = nn.ReLU(inplace=True)

        # F_h and F_w in equations (7) and (8): C/r -> C.
        self.conv_h = nn.Conv2d(
            reduced_channels,
            channels,
            kernel_size=1,
            stride=1,
            padding=0,
        )
        self.conv_w = nn.Conv2d(
            reduced_channels,
            channels,
            kernel_size=1,
            stride=1,
            padding=0,
        )
        self.sigmoid = nn.Sigmoid()

    def forward(self, x: Tensor) -> Tensor:
        """Apply coordinate attention to a four-dimensional feature map."""
        identity = x
        height, width = x.shape[2:]

        # Equation (4): average each row along W -> z_h in R^(N,C,H,1).
        z_h = x.mean(dim=3, keepdim=True)

        # Equation (5): average each column along H -> z_w in R^(N,C,1,W).
        z_w = x.mean(dim=2, keepdim=True)

        # Rotate z_w so both descriptors can be concatenated along one spatial
        # dimension: (N,C,H,1) + (N,C,W,1) -> (N,C,H+W,1).
        z_w_for_concat = z_w.permute(0, 1, 3, 2)

        # Equation (6): f = ReLU(BN(F1([z_h, z_w]))).
        f = torch.cat((z_h, z_w_for_concat), dim=2)
        f = self.relu(self.bn(self.conv_shared(f)))

        # Recover the two coordinate branches described after equation (6).
        f_h, f_w = torch.split(f, (height, width), dim=2)
        f_w = f_w.permute(0, 1, 3, 2)

        # Equations (7) and (8).
        g_h = self.sigmoid(self.conv_h(f_h))  # (N,C,H,1)
        g_w = self.sigmoid(self.conv_w(f_w))  # (N,C,1,W)

        # Equation (9): y_c(i,j) = x_c(i,j) * g_h_c(i) * g_w_c(j).
        return identity * g_h * g_w
