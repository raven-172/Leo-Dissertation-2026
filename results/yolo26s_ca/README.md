# YOLO26s CA Model Results

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
| `weights/epoch*.pt` | Periodic checkpoints saved every 10 epochs, from epoch 0 through epoch 220. |
| `.gitkeep` | Placeholder originally used to keep the directory in Git while it was empty. |

## Overview

This directory contains the training artifacts and evaluation summary for the YOLO26s CA object-detection model. The model was trained from scratch without pretrained weights.

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
| Model | YOLO26s CA |
| Fused layers | 129 |
| Parameters | 14,051,919 |
| Gradients during evaluation | 0 |
| Computational complexity | 43.3 GFLOPs |

## Training Configuration

The configuration recorded in `args.yaml` includes:

- Task: object detection
- Training mode: from scratch
- Configured epochs: 300
- Recorded epochs: 227
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

The highest validation `mAP50–95` recorded in `results.csv` occurred at epoch 177.

| Metric | Best epoch (177) | Final recorded epoch (227) |
|---|---:|---:|
| Precision | 0.96821 | 0.95917 |
| Recall | 0.93702 | 0.94328 |
| mAP50 | 0.97316 | 0.96836 |
| mAP50–95 | **0.81516** | 0.81277 |
| Training box loss | 0.73771 | 0.65748 |
| Training classification loss | 0.35941 | 0.31766 |
| Training L1 loss | 0.00521 | 0.00459 |
| Validation box loss | 0.75198 | 0.74963 |
| Validation classification loss | 0.47940 | 0.46211 |
| Validation L1 loss | 0.00747 | 0.00747 |

- Time at the best recorded epoch: 31,713.1 seconds (approximately 8 h 49 min).
- Total recorded training time: 40,669.6 seconds (approximately 11 h 18 min).

## Best-Checkpoint Evaluation

The fused `best.pt` checkpoint was evaluated using 1,226 images containing 2,665 object instances.

| Precision | Recall | mAP50 | mAP50–95 |
|---:|---:|---:|---:|
| 0.968 | 0.937 | 0.973 | 0.815 |

### Inference Speed

| Stage | Time per image |
|---|---:|
| Preprocessing | 0.1 ms |
| Inference | 2.8 ms |
| Loss computation | 0.0 ms |
| Postprocessing | 0.2 ms |
| Total pipeline time | approximately 3.1 ms |
