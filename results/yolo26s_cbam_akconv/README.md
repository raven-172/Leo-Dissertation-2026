# YOLO26s CBAM AKConv Model Results

## File and Folder Guide

| Item | Description |
|---|---|
| `README.md` | Summary of the model configuration, training results, and evaluation. |
| `args.yaml` | Configuration and hyperparameters used for training. |
| `results.csv` | Training and validation metrics recorded for each epoch. |
| `results.png` | Combined plots showing how losses and evaluation metrics changed during training. |
| `BoxF1_curve.png` | F1 score at different confidence thresholds. |
| `BoxPR_curve.png` | Relationship between precision and recall. |
| `BoxP_curve.png` | Precision at different confidence thresholds. |
| `BoxR_curve.png` | Recall at different confidence thresholds. |
| `confusion_matrix.png` | Raw confusion matrix showing model predictions for each class. |
| `confusion_matrix_normalized.png` | Normalized confusion matrix for easier comparison between classes. |
| `labels.jpg` | Distribution and locations of object labels in the training dataset. |
| `train_batch0.jpg` – `train_batch2.jpg` | Example training batches with labels and augmentations applied. |
| `val_batch0_labels.jpg` – `val_batch2_labels.jpg` | Ground-truth labels from example validation batches. |
| `val_batch0_pred.jpg` – `val_batch2_pred.jpg` | Model predictions for the corresponding validation batches. |
| `weights/` | Model checkpoint files saved during training. |
| `weights/best.pt` | Checkpoint with the best validation performance. |
| `weights/last.pt` | Checkpoint saved at the end of training. |
| `weights/epoch*.pt` | Periodic checkpoints saved every 10 epochs, from epoch 0 through epoch 120. |

## Overview

This directory contains the training artifacts and evaluation summary for the YOLO26s model combining CBAM and AKConv modules. The model was trained from scratch without pretrained weights.

## Environment

| Component | Configuration |
|---|---|
| Ultralytics | 8.4.127 |
| Python | 3.11.15 |
| PyTorch | 2.11.0+cu128 |
| CUDA device | NVIDIA GeForce RTX 5060 Ti |
| GPU memory | 16,311 MiB |
| Image size | 640 × 640 |
| Batch size | 8 |
| AMP | Enabled |

## Model Summary

| Property | Value |
|---|---:|
| Model | YOLO26s CBAM AKConv |
| Fused layers | 131 |
| Parameters | 11,357,517 |
| Gradients during evaluation | 0 |

## Numerical Stability Warning

During validation, the AKConv module reported a non-finite input tensor with the following information:

| Property | Value |
|---|---:|
| Data type | `torch.float32` |
| Tensor shape | `(1, 512, 20, 20)` |
| NaN values | 204,800 |
| Infinite values | 0 |

All 204,800 elements in the reported tensor were NaN. Validation still completed and produced the metrics below, but this warning indicates numerical instability during at least one forward pass. The results should therefore be interpreted cautiously until the source of the NaN values has been investigated.

## Training Configuration

The configuration recorded in `args.yaml` includes:

- Task: object detection
- Training mode: from scratch
- Configured epochs: 300
- Recorded epochs: 126
- Early-stopping patience: 50 epochs
- Optimizer: automatic selection
- Initial learning rate: 0.01
- Final learning-rate factor: 0.01
- Momentum: 0.937
- Weight decay: 0.0005
- Random seed: 42
- Deterministic training: enabled
- Validation during training: enabled
- Checkpoint interval: every 10 epochs
- Mosaic augmentation: enabled and disabled for the final 10 epochs

## Training Results

The highest validation `mAP50–95` recorded in `results.csv` occurred at epoch 76.

| Metric | Best epoch (76) | Final recorded epoch (126) |
|---|---:|---:|
| Precision | 0.96627 | 0.96622 |
| Recall | 0.94588 | 0.94146 |
| mAP50 | 0.97451 | 0.96945 |
| mAP50–95 | **0.81036** | 0.80660 |
| Training box loss | 0.87728 | 0.79665 |
| Training classification loss | 0.47813 | 0.41412 |
| Training L1 loss | 0.00646 | 0.00571 |
| Validation box loss | 0.72949 | 0.73780 |
| Validation classification loss | 0.40809 | 0.40480 |
| Validation L1 loss | 0.00730 | 0.00731 |

- Time at the best recorded epoch: 15,902.8 seconds (approximately 4 h 25 min).
- Total recorded training time: 26,314.3 seconds (approximately 7 h 18 min).

## Best-Checkpoint Evaluation

The fused `best.pt` checkpoint was evaluated using 1,226 images containing 2,665 object instances.

| Precision | Recall | mAP50 | mAP50–95 |
|---:|---:|---:|---:|
| 0.966 | 0.946 | 0.975 | 0.810 |

### Inference Speed

| Stage | Time per image |
|---|---:|
| Preprocessing | 0.1 ms |
| Inference | 2.3 ms |
| Loss computation | 0.0 ms |
| Postprocessing | 0.1 ms |
| Total pipeline time | approximately 2.5 ms |
