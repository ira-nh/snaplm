# SnapLM Roadmap

## Vision

SnapLM is a hardware-aware local language model companion that helps users understand, benchmark, and optimize local language model inference by selecting the most appropriate execution backend for their hardware.

---

# Version 0.1 — System Detection

### Goal

Understand the machine SnapLM is running on.

### Features

- Detect operating system
- Detect architecture
- Detect Python version
- Detect CPU information
- Detect memory information
- Produce a structured hardware report

Example:

```text
System
------
Windows 11
ARM64

CPU
---
Snapdragon X Plus X1P-42-100
12 cores

Memory
------
15.6 GB total
11.2 GB available
```

---

# Version 0.2 — Accelerator Detection

### Goal

Identify available hardware acceleration.

### Features

- Detect GPU
- Detect GPU vendor
- Detect NPU (where supported)
- Detect available acceleration runtimes
- Improve hardware reporting

Example:

```text
GPU
---
Adreno X1-45

NPU
---
Hexagon

Acceleration
------------
DirectML
QNN
```

---

# Version 0.3 — Benchmarking

### Goal

Measure local inference performance.

### Features

- CPU benchmark
- Backend benchmark
- Performance reporting
- Compare execution speeds

Example:

```text
Backend: Ollama

Prompt Processing
-----------------
42 tokens/sec

Generation
----------
28 tokens/sec
```

---

# Version 0.4 — Model Intelligence

### Goal

Recommend models that fit the user's hardware.

### Features

- Estimate maximum practical model size
- Recommend quantization levels
- Estimate memory usage
- Estimate inference speed
- Warn about hardware limitations

Example:

```text
Recommended

✓ Qwen3 4B Q4_K_M
✓ Phi-4 Mini

Not Recommended

✗ Gemma 27B
Reason:
Insufficient available memory.
```

---

# Version 0.5 — Backend Intelligence

### Goal

Recommend the best inference backend.

### Features

- Detect installed backends
- Compare backend compatibility
- Recommend optimal backend
- Explain performance bottlenecks

Example:

```text
Detected Hardware
-----------------
Snapdragon X Elite

Installed Backends
------------------
✓ Ollama
✓ llama.cpp

Recommendation
--------------
Use llama.cpp.

Reason:
Better hardware acceleration is available.
```

---

# Version 0.6 — Backend Integration

### Goal

Automatically configure and launch local inference.

### Features

- Configure supported backends
- Generate optimized launch settings
- Automatically select execution backend
- Launch models directly through SnapLM

---

# Long-Term Goals

- Support Windows on ARM
- Support x86 Windows
- Support Linux
- Support macOS
- Support Apple Silicon
- Support NVIDIA CUDA
- Support AMD ROCm
- Support Intel accelerators
- Support Qualcomm QNN
- Explain inference bottlenecks
- Simplify local AI deployment across hardware platforms