# Adjusted Ultralytics Source

## Overview

This directory contains a customized copy of the [official Ultralytics repository](https://github.com/ultralytics/ultralytics). The source was pulled from Ultralytics and adjusted for the dissertation experiments using Ultralytics 8.4.127.

The custom neural-network blocks and supporting functions developed in [`scr/`](../scr/) were integrated directly into the copied Ultralytics source. This allows the Ultralytics model parser to recognize the additional modules used by the proposed model configurations and enables those models to be constructed and trained through the standard Ultralytics workflow.

## Directory Structure

| Path | Description |
|---|---|
| [`ultralytics/`](./ultralytics/) | Customized Ultralytics source tree used to build and train the dissertation models. |
| [`../scr/`](../scr/) | Reference implementations of the custom blocks, parser integration, and model-validation utilities. |
| [`../models/`](../models/) | YAML configurations for the baseline and proposed YOLO26s model variants. |
| [`../results/`](../results/) | Training artifacts, checkpoints, plots, and evaluation summaries for the model variants. |

## Integrated Extensions

The adjusted source includes direct support for:

- `CA` — Coordinate Attention.
- `RCAB` — Residual Coordinate Attention Block.
- `RCAC3k2` — a C3k2-style block using residual coordinate-attention components.
- `AKConv` — adaptive kernel convolution.
- `CBAM` — Ultralytics' existing CBAM block with the parser handling required by the proposed configuration.

The block implementations are included in the adjusted neural-network module files, exported through the module package, and registered in the Ultralytics model parser. These changes allow the custom module names to be used directly in the YAML model configurations.

## Purpose

The adjusted Ultralytics copy is maintained so that the proposed architectures can be trained reproducibly without modifying an external Ultralytics installation at runtime. It provides the framework-level changes required by:

- `yolo26s_ca`
- `yolo26s_rcac3k2`
- `yolo26s_cbam_akconv`

The unmodified `yolo26s_base` configuration is retained as the experimental baseline.

> This directory is a research-specific modification of Ultralytics and should not be treated as the canonical upstream source.
