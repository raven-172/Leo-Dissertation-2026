from __future__ import annotations

import torch
from torch import Tensor, nn
import torch.nn.functional as F

from ultralytics.nn.modules.block import C2f, C3

__all__ = ["CA", "RCAB", "RCAC3k", "RCAC3k2", "SAM", "CAM", "CBAM"]


class CA(nn.Module):

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



class RCAB(nn.Module):
    """Residual block containing Coordinate Attention.

    Structure from Paper 22, equations (8) and (9):

        X_C = CBS_3x3(CBS_1x1(X_R))
        Y_C = CA(X_C)
        Y_R = Y_C + X_R

    The residual coefficient matrix K in equation (9) is set to one, which
    corresponds to the standard residual connection shown in Figure 3.
    """

    def __init__(self, channels: int, reduction: int = 32) -> None:
        super().__init__()

        self.cbs_1x1 = nn.Sequential(
            nn.Conv2d(
                channels,
                channels,
                kernel_size=1,
                stride=1,
                padding=0,
                bias=False,
            ),
            nn.BatchNorm2d(channels),
            nn.SiLU(inplace=True),
        )

        self.cbs_3x3 = nn.Sequential(
            nn.Conv2d(
                channels,
                channels,
                kernel_size=3,
                stride=1,
                padding=1,
                bias=False,
            ),
            nn.BatchNorm2d(channels),
            nn.SiLU(inplace=True),
        )

        self.ca = CA(channels, reduction)

    def forward(self, x: Tensor) -> Tensor:
        x_c = self.cbs_3x3(self.cbs_1x1(x))
        y_c = self.ca(x_c)
        return y_c + x


class RCAC3k(C3):
    """C3 block whose internal Bottleneck blocks are replaced by RCAB."""

    def __init__(
        self,
        c1: int,
        c2: int,
        n: int = 1,
        shortcut: bool = True,
        g: int = 1,
        e: float = 0.5,
        reduction: int = 32,
    ) -> None:
        super().__init__(c1, c2, n, shortcut, g, e)
        hidden_channels = int(c2 * e)
        self.m = nn.Sequential(
            *(RCAB(hidden_channels, reduction) for _ in range(n))
        )


class RCAC3k2(C2f):
    """C3k2 variant that replaces every Bottleneck with RCAB.

    When ``c3k=False``, each repeated unit inside C2f is one RCAB.

    When ``c3k=True``, each repeated unit inside C2f is one RCAC3k block
    containing two consecutive RCAB blocks.
    """

    def __init__(
        self,
        c1: int,
        c2: int,
        n: int = 1,
        c3k: bool = False,
        e: float = 0.5,
        g: int = 1,
        shortcut: bool = True,
        reduction: int = 32,
    ) -> None:
        super().__init__(c1, c2, n, shortcut, g, e)
        self.m = nn.ModuleList(
            RCAC3k(
                self.c,
                self.c,
                n=2,
                shortcut=shortcut,
                g=g,
                reduction=reduction,
            )
            if c3k
            else RCAB(self.c, reduction)
            for _ in range(n)
        )


class SAM(nn.Module):
    def __init__(self, bias=False):
        super(SAM, self).__init__()
        self.bias = bias
        self.conv = nn.Conv2d(in_channels=2, out_channels=1, kernel_size=7, stride=1, padding=3, dilation=1, bias=self.bias)

    def forward(self, x):
        max = torch.max(x,1)[0].unsqueeze(1)
        avg = torch.mean(x,1).unsqueeze(1)
        concat = torch.cat((max,avg), dim=1)
        output = self.conv(concat)
        output = F.sigmoid(output) * x 
        return output 

class CAM(nn.Module):
    def __init__(self, channels, r):
        super(CAM, self).__init__()
        self.channels = channels
        self.r = r
        self.linear = nn.Sequential(
            nn.Linear(in_features=self.channels, out_features=self.channels//self.r, bias=True),
            nn.ReLU(inplace=True),
            nn.Linear(in_features=self.channels//self.r, out_features=self.channels, bias=True))

    def forward(self, x):
        max = F.adaptive_max_pool2d(x, output_size=1)
        avg = F.adaptive_avg_pool2d(x, output_size=1)
        b, c, _, _ = x.size()
        linear_max = self.linear(max.view(b,c)).view(b, c, 1, 1)
        linear_avg = self.linear(avg.view(b,c)).view(b, c, 1, 1)
        output = linear_max + linear_avg
        output = F.sigmoid(output) * x
        return output
    
class CBAM(nn.Module):
    def __init__(self, channels, r):
        super(CBAM, self).__init__()
        self.channels = channels
        self.r = r
        self.sam = SAM(bias=False)
        self.cam = CAM(channels=self.channels, r=self.r)

    def forward(self, x):
        output = self.cam(x)
        output = self.sam(output)
        return output + x