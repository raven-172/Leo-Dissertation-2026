# YOLO Model Extensions and Custom Blocks

The `scr` package contains the custom neural-network blocks and the parser integration used by the dissertation's YOLO26 experiments.

## Folder structure

```text
scr/
├── __init__.py          # Activates the custom parser when `scr` is imported
├── block_add.py         # Defines CA, RCAB, RCAC3k2, CBAM and AKConv
├── tasks.py             # Extends the pinned Ultralytics parser
├── validate_models.py   # Builds and forwards every model YAML
└── README.md
```

## Installation

The parser is synchronized with Ultralytics 8.4.127. Install the pinned dependencies from the repository root:

```bash
pip install -r requirements.txt
```

## Using a custom YAML

Import `scr` before constructing the model. This registers the custom classes and replaces Ultralytics' parser for the current Python process:

```python
import scr
from ultralytics import YOLO

model = YOLO("models/yolo26s_ca.yaml")
model.train(data="path/to/data.yaml")
```

Without `import scr`, Ultralytics does not know the names `CA`, `RCAC3k2`, `CBAM`, or `AKConv` from the YAML files.

## Parser differences

Every intentional change inside the copied parser flow is labelled:

```python
# [KHÁC PARSER GỐC] ...
```

The custom flow:

- registers all classes from `block_add.py` in `ultralytics.nn.tasks`;
- scales the declared output channels of `CA` and `AKConv` by the selected model width;
- passes the scaled repeat count into `RCAC3k` and `RCAC3k2`;
- treats `RCAB`, `CAM`, and `CBAM` as channel-preserving blocks;
- keeps `CA` input and output channels equal so its element-wise attention multiplication is valid.

## Validation

Run a construction and inference smoke test for all four YAML files:

```bash
python -m scr.validate_models --imgsz 640
```

The command does not download pretrained weights. It creates each architecture from YAML and forwards one zero-valued image through it.
