"""Build every custom YAML and run a small inference smoke test."""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

# Importing scr.tasks registers the custom modules before YOLO parses a YAML.
from .tasks import install_custom_parser

install_custom_parser()

from ultralytics import YOLO  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
MODEL_FILES = (
    "yolo26s_base.yaml",
    "yolo26s_ca.yaml",
    "yolo26s_rcac3k2.yaml",
    "yolo26s_cbam_akconv.yaml",
)


def validate_models(image_size: int = 640) -> None:
    """Instantiate and forward all model variants without downloading weights."""
    if image_size <= 0 or image_size % 32:
        raise ValueError("image_size must be a positive multiple of 32.")

    for filename in MODEL_FILES:
        model_path = ROOT / "models" / filename
        yolo = YOLO(str(model_path), task="detect")
        network = yolo.model.eval()
        device = next(network.parameters()).device
        sample = torch.zeros(1, 3, image_size, image_size, device=device)
        with torch.no_grad():
            network(sample)
        print(f"OK: {filename} ({image_size}x{image_size})")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="Square smoke-test image size; must be a positive multiple of 32.",
    )
    args = parser.parse_args()
    validate_models(args.imgsz)


if __name__ == "__main__":
    main()
