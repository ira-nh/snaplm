# SnapLM Architecture

## Goal

SnapLM helps users determine how to run local language models efficiently based on their hardware.

Rather than implementing language model inference itself, SnapLM is intended to act as an orchestration layer between the user's hardware, available inference runtimes, and local models.

---

## Current Pipeline

```text
User
 |
 v
CLI
 |
 v
Hardware Detection
 |
 v
Hardware Profile
 |
 v
CPU Benchmarking
```

The current implementation can detect:

* Operating system and architecture
* CPU information
* RAM availability and utilization
* GPU
* NPU
* Python environment

Initial Ollama benchmarks have also established CPU-only inference baselines for Qwen3 4B and Qwen3 8B.

---

## Planned Pipeline

```text
User
 |
 v
CLI
 |
 v
Hardware Detection
 |
 v
Runtime Detection
 |
 v
Compatibility Analysis
 |
 +-------------------+
 |                   |
 v                   v
Model Discovery   Benchmarking
 |                   |
 +---------+---------+
           |
           v
   Recommendation
           |
           v
    Backend Selection
           |
           v
     Configuration
           |
           v
      Model Runtime
           |
           v
 Performance Monitoring
```

---

## Components

### `hardware.py`

Responsible for answering:

> What hardware is available?

Currently detects:

* Operating system
* CPU architecture and information
* Physical and logical CPU cores
* Total and available RAM
* GPU
* NPU
* Hardware driver/status information where available

The hardware layer reports information but does not decide which execution device should be used.

---

### `runtime.py` *(next)*

Responsible for answering:

> What inference software is available that could use this hardware?

Planned runtime detection includes:

* Ollama
* ONNX Runtime
* Qualcomm QNN
* Windows ML
* DirectML
* llama.cpp
* Other platform-specific runtimes

SnapLM should distinguish between:

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

Detecting an accelerator does not necessarily mean an installed runtime can use it.

---

### `benchmark.py` *(future)*

Responsible for measuring actual inference performance.

Metrics may include:

* Model load time
* Time to first token
* Prompt processing speed
* Generation speed
* Total response time
* Memory usage
* Execution device

Current manual baseline:

```text
Qwen3 4B
Ollama / 100% CPU
~11.14 tokens/s

Qwen3 8B
Ollama / 100% CPU
~5.99 tokens/s
```

These results will eventually be collected automatically.

---

### `model_manager.py` *(future)*

Responsible for understanding available models.

Planned responsibilities:

* Search model providers such as Hugging Face
* Download models
* Track installed models
* Read model metadata
* Identify parameter count and quantization
* Estimate memory requirements
* Determine runtime compatibility

The model catalogue should eventually be dynamic rather than relying entirely on a hardcoded list.

---

### `backend.py` *(future)*

Responsible for providing a common interface to different inference backends.

Potential execution paths include:

```text
Ollama
   |
   v
CPU

ONNX Runtime
   |
   v
QNN
   |
   v
Hexagon NPU

Windows ML / DirectML
   |
   v
Adreno GPU
```

This abstraction allows SnapLM to work with multiple inference engines without the rest of the application needing to understand each backend individually.

---

### Compatibility Engine *(future)*

Responsible for answering:

> Can this model realistically run through this backend on this machine?

It will combine:

```text
Hardware Profile
       +
Runtime Availability
       +
Model Requirements
       |
       v
Compatibility
```

Factors may include:

* Available RAM
* Model size
* Quantization
* Context length
* Runtime support
* Accelerator support

---

### Recommendation Engine *(future)*

Responsible for selecting an appropriate combination of:

```text
Model
+
Quantization
+
Backend
+
Execution Device
```

Recommendations should eventually use measured performance where available rather than relying only on theoretical hardware specifications.

---

### Diagnostic Engine *(future)*

Responsible for explaining poor inference performance.

For example:

```text
Current model: Qwen3 8B

Execution:
100% CPU

Detected accelerators:
Adreno GPU
Hexagon NPU

Diagnosis:
Current backend is not using available acceleration.

Recommendation:
Test a compatible accelerated runtime.
```

This is one of the central goals of SnapLM: not merely identifying hardware, but explaining what is happening during local inference and what the user can do about it.

---

## Separation of Responsibilities

Each component answers a different question:

```text
hardware.py
"What hardware exists?"

runtime.py
"What inference software exists?"

model_manager.py
"What models are available?"

Compatibility Engine
"What combinations can work?"

benchmark.py
"How well do they actually work?"

backend.py
"How do we execute through each runtime?"

Recommendation Engine
"Which combination should we use?"

Diagnostic Engine
"Why is the current setup behaving this way?"

cli.py
"How does the user interact with SnapLM?"
```

---

## Current Development State

```text
Project setup             ✓
Python packaging          ✓
CLI                       ✓
CPU detection             ✓
Memory detection          ✓
GPU detection             ✓
NPU detection             ✓
CPU inference baseline    ✓

Runtime detection         ← CURRENT
Accelerated inference
Automated benchmarking
Backend abstraction
Model discovery
Compatibility analysis
Recommendations
Diagnostics
Automatic execution
```

---

## Immediate Goal

The development machine currently exposes:

```text
Snapdragon X Plus
 |
 +-- Oryon CPU
 |
 +-- Adreno X1-45 GPU
 |
 +-- Hexagon NPU
```

However, current Ollama testing shows both Qwen3 4B and Qwen3 8B executing entirely on the CPU.

The next milestone is therefore:

```text
Detected accelerator
        |
        v
Find compatible runtime
        |
        v
Execute model
        |
        v
Benchmark
        |
        v
Compare against CPU baseline
```

Once an accelerated path has been successfully demonstrated, SnapLM can begin automating runtime selection and performance optimization.
