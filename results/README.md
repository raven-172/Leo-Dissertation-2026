# YOLO26s Model Results

## Folder Guide

| Folder | Description |
|---|---|
| [`yolo26s_base/`](./yolo26s_base/) | Training artifacts, checkpoints, plots, and evaluation results for the baseline YOLO26s model. |
| [`yolo26s_ca/`](./yolo26s_ca/) | Training artifacts, checkpoints, plots, and evaluation results for the YOLO26s model using the CA attention module. |
| [`yolo26s_rcac3k2/`](./yolo26s_rcac3k2/) | Training artifacts, checkpoints, plots, and evaluation results for the YOLO26s RCAC3k2 model. |
| [`yolo26s_cbam_akconv/`](./yolo26s_cbam_akconv/) | Training artifacts, checkpoints, plots, and evaluation results for the YOLO26s model combining CBAM and AKConv modules. |

## Common Contents

Each model directory generally contains:

| Item | Description |
|---|---|
| `README.md` | Summary of the model, training configuration, recorded results, and evaluation metrics. |
| `args.yaml` | Configuration and hyperparameters used for training. |
| `results.csv` | Training and validation metrics recorded for each epoch. |
| `results.png` | Combined visualization of training losses and evaluation metrics. |
| `Box*_curve.png` | Precision, recall, F1, and precision–recall curves. |
| `confusion_matrix*.png` | Raw and normalized confusion matrices. |
| `labels.jpg` | Visualization of the training-label distribution. |
| `train_batch*.jpg` | Example training batches with labels and augmentations. |
| `val_batch*_labels.jpg` | Ground-truth labels from example validation batches. |
| `val_batch*_pred.jpg` | Predictions from the corresponding validation batches. |
| `weights/` | Best, final, and periodic model checkpoints saved during training. |

Refer to the `README.md` inside each model directory for its detailed architecture, training results, evaluation metrics, and inference speed.
