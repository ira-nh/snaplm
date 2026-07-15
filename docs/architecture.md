# SnapLM Architecture

## Goal

SnapLM helps users determine how to run local language models efficiently based on their hardware.

## Current Pipeline

User
 |
 v
CLI
 |
 v
Hardware Detection
 |
 v
Hardware Report

## Planned Pipeline

User
 |
 v
CLI
 |
 v
Hardware Detection
 |
 v
Capability Analysis
 |
 v
Model Recommendation
 |
 v
Backend Selection
 |
 v
Model Runtime

## Components

### hardware.py

Responsible for detecting:

- CPU architecture
- CPU information
- RAM
- GPU availability
- Accelerator availability

### model_manager.py (future)

Responsible for:

- Downloading models
- Tracking installed models
- Model metadata

### backend.py (future)

Responsible for:

- Selecting execution backend
- CPU/GPU/NPU acceleration