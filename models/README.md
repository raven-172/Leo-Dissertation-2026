# YOLO26 Model Variants

This folder contains four YOLO26s model configurations. They are designed to compare the original YOLO26s architecture with variants that add attention or adaptive convolution components for improving partially occluded object detection.

## Common model structure

All four models follow the same general pipeline:

```text
Input image
    ↓
Backbone
Conv → C3k2 blocks → SPPF → C2PSA
    ↓
Feature-fusion head
Upsample → Concat → C3k2
    ↓
Three detection scales
P3/8 → small objects
P4/16 → medium objects
P5/32 → large objects
    ↓
Detect
```

The YAML layers use this format:

```yaml
[from, repeats, module, arguments]
```

For example:

```yaml
- [-1, 2, C3k2, [512, True]]
```

This means:

- Take the output from the previous layer (`-1`).
- Repeat the module twice.
- Use the `C3k2` module.
- Configure it with the supplied arguments.

The configurations use:

- `nc: 1` for 1 object classes (person).
- `end2end: True` for end-to-end detection.
- `reg_max: 1` for the YOLO26 DFL-free regression design.
- P3, P4 and P5 outputs for multi-scale detection.

## Model configurations

### [`yolo26s_base.yaml`](yolo26s_base.yaml)

**Purpose**

Provide the standard YOLO26s model as the baseline. Experimental variants can be compared with this model to measure whether their custom components improve detection.

**Research basis**

- [Official Ultralytics YOLO26 documentation](https://docs.ultralytics.com/models/yolo26/)

**Structure**

```text
Backbone:
Conv → Conv → C3k2 → Conv → C3k2
→ Conv → C3k2 → Conv → C3k2
→ SPPF → C2PSA

Head:
Upsample and combine P5 with P4
→ Upsample and combine P4 with P3
→ Downsample and rebuild P4
→ Downsample and rebuild P5
→ Detect at P3, P4 and P5
```

- `C3k2` extracts and refines image features.
- `SPPF` collects information from different receptive-field sizes.
- `C2PSA` applies spatial attention to the deepest features.
- The detection head combines shallow detail with deeper semantic information.

---

### [`yolo26s_ca.yaml`](yolo26s_ca.yaml)

**Purpose**

Improve the model's ability to locate useful visible features when part of an object is hidden.

**Research basis**

- [Paper 13 — Occlusion Target Detection Based on Improved YOLOv5](../docs/paper/paper13.pdf)
- [Paper 34 — Coordinate Attention for Efficient Mobile Network Design](../docs/paper/paper34.pdf)

**Structure**

This model adds a Coordinate Attention (`CA`) layer near the end of the backbone:

```text
C3k2 → CA → SPPF → C2PSA
```

Coordinate Attention separately analyses information along the image's height and width. This helps the network understand:

- **What** feature is important.
- **Where** that feature is located.

It may help the detector focus on visible parts of an occluded object while reducing attention to irrelevant background regions.

---

### [`yolo26s_cbam_akconv.yaml`](yolo26s_cbam_akconv.yaml)

**Purpose**

Use attention and adaptive feature sampling to improve the detection of objects whose normal shape is interrupted by occlusion.

**Research basis**

- [Paper 1 — CAE-YOLOV8](../docs/paper/paper1.pdf)
- [Paper 32 — Convolutional Block Attention Module](../docs/paper/paper32.pdf)
- [Paper 41 — Linear Deformable Convolution](../docs/paper/paper41.pdf)

**Intended structure**

```text
YOLO26 backbone
    ↓
CBAM
Channel attention → Spatial attention
    ↓
AKConv
Learned adaptive sampling positions
    ↓
YOLO26 feature-fusion head
    ↓
P3, P4 and P5 detection
```

- `CBAM` determines which feature channels and image locations are important.
- `AKConv` learns where to sample features instead of being restricted to a fixed square convolution pattern.
- Together, they are intended to capture useful visible fragments when an object is partly hidden.

**Current configuration note**

The current YAML contains an `AKConv` layer, but it does not contain a `CBAM` layer. Therefore, the current file implements an AKConv variant rather than the complete CBAM–AKConv design suggested by its filename.

---

### [`yolo26s_rcac3k2.yaml`](yolo26s_rcac3k2.yaml)

**Purpose**

Combine Coordinate Attention with residual feature learning while preserving the efficient C3k2-style structure.

**Research basis**

- [Paper 22 — AodeMar](../docs/paper/paper22.pdf)
- [Paper 34 — Coordinate Attention for Efficient Mobile Network Design](../docs/paper/paper34.pdf)

**Structure**

This model replaces the final backbone `C3k2` block with `RCAC3k2`:

```text
Standard model:
C3k2 → SPPF → C2PSA

Modified model:
RCAC3k2 → SPPF → C2PSA
```

Internally, `RCAC3k2` contains Residual Coordinate Attention Blocks:

```text
Input
  ├──────────────────────────────┐
  ↓                              │
1×1 convolution                  │
  ↓                              │
3×3 convolution                  │
  ↓                              │
Coordinate Attention             │
  ↓                              │
Add original input ──────────────┘
  ↓
Output
```

The residual connection preserves the original information, while Coordinate Attention emphasises useful features and their positions.
