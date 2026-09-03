# YOLO26s RCAC3k2 Model Results

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

This directory contains the training artifacts and evaluation summary for the YOLO26s RCAC3k2 object-detection model. The model was trained from scratch without pretrained weights.

## Environment

| Component | Configuration |
|---|---|
| Ultralytics | 8.4.127 |
| Python | 3.11.15 |
| PyTorch | 2.11.0+cu128 |
| CUDA device | NVIDIA GeForce RTX 5060 Ti |
| GPU memory | 16,311 MiB |
| Image size | 640 × 640 |
| Batch size | 16 |
| AMP | Enabled |

## Model Summary

| Property | Value |
|---|---:|
| Model | YOLO26s RCAC3k2 |
| Fused layers | 144 |
| Parameters | 9,210,639 |
| Gradients during evaluation | 0 |
| Computational complexity | 20.6 GFLOPs |

## Training Configuration

The configuration recorded in `args.yaml` includes:

- Task: object detection
- Training mode: from scratch
- Configured epochs: 300
- Recorded epochs: 125
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

The highest validation `mAP50–95` recorded in `results.csv` occurred at epoch 75.

| Metric | Best epoch (75) | Final recorded epoch (125) |
|---|---:|---:|
| Precision | 0.96659 | 0.96329 |
| Recall | 0.94456 | 0.95122 |
| mAP50 | 0.97582 | 0.97426 |
| mAP50–95 | **0.81353** | 0.81200 |
| Training box loss | 0.85941 | 0.79512 |
| Training classification loss | 0.45231 | 0.40402 |
| Training L1 loss | 0.00623 | 0.00570 |
| Validation box loss | 0.76894 | 0.75398 |
| Validation classification loss | 0.41900 | 0.44743 |
| Validation L1 loss | 0.00759 | 0.00728 |

- Time at the best recorded epoch: 15,884.1 seconds (approximately 4 h 25 min).
- Total recorded training time: 26,474.1 seconds (approximately 7 h 21 min).

## Best-Checkpoint Evaluation

The fused `best.pt` checkpoint was evaluated using 1,226 images containing 2,665 object instances.

| Precision | Recall | mAP50 | mAP50–95 |
|---:|---:|---:|---:|
| 0.967 | 0.945 | 0.976 | 0.814 |

### Inference Speed

| Stage | Time per image |
|---|---:|
| Preprocessing | 0.1 ms |
| Inference | 2.6 ms |
| Loss computation | 0.0 ms |
| Postprocessing | 0.3 ms |
| Total pipeline time | approximately 3.0 ms |
