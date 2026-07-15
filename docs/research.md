# SnapLM Research Notes

## Project Goal

SnapLM is a hardware-aware local LLM manager designed to make running AI models efficiently on consumer devices easier.

The initial focus is optimizing local inference on Snapdragon Windows ARM laptops by investigating available GPU and NPU acceleration paths.

---

## Target Hardware

Device:
- Lenovo IdeaPad Slim 5 14Q8X9

Processor:
- Snapdragon X Plus X1P-42-100
- Qualcomm Oryon CPU

Memory:
- 16 GB LPDDR5X unified memory

GPU:
- Qualcomm Adreno X1-45

NPU:
- Qualcomm Hexagon

Operating System:
- Windows 11 ARM64

---

## Main Problem

Current local LLM tools appear to rely primarily on CPU inference.

Goal:

Investigate whether local models can be accelerated using:
- GPU
- NPU
- Other hardware-specific runtimes

---

## Research Questions

### Hardware Acceleration

- Can the Adreno GPU accelerate LLM inference?
- Can the Hexagon NPU accelerate transformer models?
- Which runtimes support Snapdragon X?

### Model Support

- Which model formats are supported?
    - GGUF
    - ONNX
    - Safetensors

### Runtime Candidates

- llama.cpp
- ONNX Runtime
- Qualcomm QNN
- Vulkan
- DirectML

---

## Initial Milestones

### Phase 1: Research
- Identify available inference backends
- Benchmark current performance

### Phase 2: Prototype
- Hardware detection
- Model management
- Backend selection

### Phase 3: Optimization
- GPU/NPU acceleration
- Automatic backend selection