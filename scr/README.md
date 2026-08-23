# YOLO Model Extensions and Custom Blocks

The `scr` folder contains custom neural-network blocks and model-building logic for the dissertation's YOLO experiments.

## Folder structure

```text
scr/
├── README.md       # Explains the files in this folder
├── block_add.py    # Defines custom neural-network blocks
└── tasks.py        # Builds YOLO models using standard and custom blocks
```

## Files

### `block_add.py`

Contains custom PyTorch components used to modify the YOLO architecture:

- `CA` — Coordinate Attention
- `RCAB` — Residual Coordinate Attention Block
- `RCAC3k` and `RCAC3k2` — YOLO blocks enhanced with coordinate attention
- `SAM` — Spatial Attention Module
- `CAM` — Channel Attention Module
- `CBAM` — Combines channel and spatial attention
- `AKConv` — Adaptive Kernel Convolution

The file is structured with imports first, followed by the implementation of each custom block as a PyTorch class.

### `tasks.py`

Contains the `parse_model()` function. It reads a YOLO model configuration and converts it into a PyTorch model.

Its main tasks are:

1. Read model settings such as depth, width, channels, and activation.
2. Process the backbone and detection head layers.
3. Recognize standard Ultralytics modules and the custom blocks from `block_add.py`.
4. Calculate the input and output channels for each layer.
5. Assemble and return the complete model.

## How the files work together

```text
YOLO model configuration
          ↓
tasks.py reads the configuration
          ↓
block_add.py provides custom blocks
          ↓
A complete PyTorch YOLO model is created
```

These files are supporting components and are not normally run directly.
