# YOLO26s Base Model Results

## File and Folder Guide

| Item | Description |
|---|---|
| `README.md` | Summary of the model configuration, training results, and test evaluation. |
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
| `weights/epoch*.pt` | Periodic checkpoints saved every 10 epochs. |
| `.gitkeep` | Placeholder originally used to keep the directory in Git while it was empty. |

## Overview

This directory contains the training artifacts and evaluation summary for the baseline YOLO26s object-detection model. The model was trained from scratch without pretrained weights.

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
| Model | YOLO26s base |
| Fused layers | 122 |
| Parameters | 9,465,567 |
| Gradients during evaluation | 0 |
| Computational complexity | 20.8 GFLOPs |

## Training Configuration

The configuration recorded in `args.yaml` includes:

- Task: object detection
- Training mode: from scratch
- Configured epochs: 300
- Recorded epochs: 190
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

The highest validation `mAP50–95` recorded in `results.csv` occurred at epoch 140.

| Metric | Best epoch (140) | Final recorded epoch (190) |
|---|---:|---:|
| Precision | 0.96513 | 0.96474 |
| Recall | 0.95009 | 0.94456 |
| mAP50 | 0.97620 | 0.97429 |
| mAP50–95 | **0.82120** | 0.81887 |
| Training box loss | 0.77295 | 0.69702 |
| Training classification loss | 0.38471 | 0.33599 |
| Training L1 loss | 0.00544 | 0.00489 |
| Validation box loss | 0.73064 | 0.72713 |
| Validation classification loss | 0.46108 | 0.45758 |
| Validation L1 loss | 0.00717 | 0.00713 |

- Time at the best recorded epoch: 14,704.8 seconds (approximately 4 h 05 min).
- Total recorded training time: 19,918.6 seconds (approximately 5 h 32 min).

## Best-Checkpoint Evaluation

The fused `best.pt` checkpoint was evaluated using 1,226 images containing 2,665 object instances.

| Precision | Recall | mAP50 | mAP50–95 |
|---:|---:|---:|---:|
| 0.940 | 0.942 | 0.967 | 0.764 |

### Inference Speed

| Stage | Time per image |
|---|---:|
| Preprocessing | 0.7 ms |
| Inference | 3.3 ms |
| Loss computation | 0.0 ms |
| Postprocessing | 0.2 ms |
| Total pipeline time | approximately 4.2 ms |
