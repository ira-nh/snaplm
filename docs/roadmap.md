# SnapLM Roadmap

## Vision

SnapLM is a hardware-aware local language model manager that helps users run AI models efficiently by selecting appropriate inference backends based on their hardware.

## Version 0.1 — Hardware Detection

Goal:
Understand the machine SnapLM is running on.

Features:
- Detect operating system
- Detect CPU
- Detect GPU
- Detect NPU (if available)
- Detect available memory

Output example:

CPU:
Snapdragon X Plus X1P-42-100

GPU:
Adreno X1-45

NPU:
Hexagon

Memory:
15.6 GB


## Version 0.2 — Model Management

Goal:
Make downloading and organizing models simple.

Features:
- Search Hugging Face models
- Download models
- Store metadata
- List installed models


## Version 0.3 — Backend Research

Goal:
Find the fastest inference path.

Investigate:
- llama.cpp
- ONNX Runtime
- Qualcomm QNN
- Vulkan
- DirectML


## Version 0.4 — Runtime Selection

Goal:
Automatically choose the best backend.

Example:

NVIDIA GPU detected:
→ CUDA backend

Apple Silicon detected:
→ Metal backend

Snapdragon detected:
→ Snapdragon-compatible backend


## Version 0.5 — User Experience

Features:
- Improved CLI
- Configuration
- Performance reports