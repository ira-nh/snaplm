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

## Milestone 8 — Runtime Detection

### Goal

Move beyond detecting hardware and determine which inference runtimes can actually use it.

The important distinction is:

```text
Hardware detected
        |
        v
Runtime available
        |
        v
Runtime compatible
        |
        v
Model successfully executed
```

Detecting a GPU or NPU does not necessarily mean that an installed inference runtime can use it.

### Runtime Module

A new module was created:

```text
src/snaplm/runtime.py
```

The first runtime detector implemented was:

```python
detect_ollama()
```

It uses `subprocess.run()` to execute:

```powershell
ollama --version
```

and currently detects:

```text
Ollama
Installed: True
Version: 0.34.0
```

The detector uses `try` / `except` so that a missing runtime can be reported rather than causing SnapLM to crash.

### Ollama Investigation

Ollama was benchmarked using Qwen3 4B and Qwen3 8B.

Results:

```text
Qwen3 4B
Execution: 100% CPU
Generation: ~11.14 tokens/s

Qwen3 8B
Execution: 100% CPU
Generation: ~5.99 tokens/s
```

Despite SnapLM detecting both:

```text
Qualcomm Adreno X1-45 GPU
Qualcomm Hexagon NPU
```

the tested Ollama execution path used neither accelerator.

### Runtime Discovery

The machine was checked for:

* ONNX Runtime
* Qualcomm QNN tools
* DirectML packages
* Qualcomm AI tools

None were currently detected.

This means an accelerated inference environment will need to be configured before GPU or NPU performance can be tested.

### Python Environment Investigation

Available Python environments were also inspected.

```text
Python 3.14
Architecture: ARM64
Status: Working

Python 3.11
Architecture: AMD64
Status: Working

Python 3.13 ARM64
Status: Registered but inaccessible
```

This established that Python version alone is not sufficient when evaluating hardware-specific runtimes. Architecture and runtime compatibility also matter.

### Candidate Acceleration Paths

Current options:

```text
Hexagon NPU
├── Windows ML + QNN
└── ONNX Runtime + QNN

Adreno GPU
└── DirectML / compatible GPU runtime
```

Windows ML + QNN will be investigated first, with ONNX Runtime QNN as an alternative route.

### Current Status

```text
Hardware Detection
        |
        +-- CPU       ✓
        +-- Memory    ✓
        +-- GPU       ✓
        +-- NPU       ✓
              |
              v
Runtime Detection
        |
        +-- Ollama    ✓
        +-- Windows ML ?
        +-- QNN       ?
        +-- ONNX      ?
              |
              v
Accelerated Inference
              |
              v
             NEXT
```

### Next Milestone

Establish an accelerated inference environment and successfully execute a model through the Hexagon NPU or Adreno GPU.

Success requires more than installing a runtime:

```text
Runtime installed
        |
        v
Execution provider available
        |
        v
Model loaded
        |
        v
Inference executed
        |
        v
Accelerator confirmed
        |
        v
Performance benchmarked
```

The resulting performance will then be compared against the existing Ollama CPU baseline.
