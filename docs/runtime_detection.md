# Runtime Detection and Acceleration Investigation

## Objective

Determine which inference runtimes are available on the development machine and identify a viable execution path capable of using the Snapdragon X Plus GPU or NPU.

The hardware detection stage established that the machine contains:

```text
CPU: Qualcomm Oryon
GPU: Qualcomm Adreno X1-45
NPU: Qualcomm Hexagon
RAM: 15.61 GB
Architecture: ARM64
```

The next question is no longer whether acceleration hardware exists, but whether an installed or installable inference runtime can actually use it.

---

## Ollama Detection

A new runtime layer was started in:

```text
src/snaplm/runtime.py
```

The first runtime detector checks whether Ollama is installed and retrieves its version.

Current result:

```text
Ollama
Installed: True
Version: 0.34.0
```

The implementation uses `subprocess.run()` to invoke:

```powershell
ollama --version
```

and parses the resulting string.

The detector uses `try` / `except` so the absence of Ollama can be treated as runtime information rather than causing SnapLM to crash.

---

## Ollama Execution Investigation

Two models were benchmarked using the same prompt:

```text
Explain what DNA is in approximately 100 words.
```

### Qwen3 4B

```text
Loaded size: 3.2 GB
Context: 4096
Execution: 100% CPU
Generation speed: ~11.14 tokens/s
Generation duration: ~37.96 s
```

### Qwen3 8B

```text
Loaded size: 5.9 GB
Context: 4096
Execution: 100% CPU
Generation speed: ~5.99 tokens/s
Generation duration: ~89.28 s
Total request duration: ~103.87 s
```

`ollama ps` confirmed that both models were executing entirely on the CPU.

This establishes that the current Ollama execution path is not using the detected Adreno GPU or Hexagon NPU for these workloads.

---

## Refined Performance Hypothesis

The original project hypothesis focused heavily on the Snapdragon system's shared memory architecture.

The experiments have produced a more precise working hypothesis.

The models can successfully load into system memory.

However:

```text
Model
  |
  v
Ollama
  |
  v
100% CPU
```

while the machine also contains:

```text
Adreno X1-45 GPU
Hexagon NPU
```

The immediate optimization problem is therefore accelerator utilization rather than simply whether the model can access RAM.

---

## Runtime Discovery

The following commands were used to search for existing acceleration runtimes:

```powershell
where.exe qnn-net-run
where.exe onnxruntime_perf_test
```

Neither executable was found.

Installed packages were also searched for:

```powershell
Get-Package | Where-Object {
    $_.Name -match "Qualcomm|QNN|ONNX|AI Hub"
}
```

No relevant installed runtime was detected.

The Python environment was checked for:

```text
ONNX
QNN
DirectML
```

and no corresponding packages were currently installed.

---

## Python Environment Investigation

The Windows Python launcher reported:

```text
Python 3.14
Python 3.13 ARM64
Python 3.11
```

Further testing showed that the environments are not equivalent.

### Python 3.11

```text
platform.machine(): AMD64
```

This environment is unsuitable for the planned native ARM64 QNN inference experiment.

### Python 3.13 ARM64

The launcher contains a registered Microsoft Store ARM64 Python entry, but attempting to execute it produced:

```text
The file cannot be accessed by the system.
```

The environment therefore cannot currently be used.

### Python 3.14

The active SnapLM environment reports:

```text
Python: 3.14.5
Machine architecture: ARM64
```

SnapLM itself can therefore continue running through the existing Python 3.14 environment.

---

## Candidate Acceleration Paths

### Path A — Windows ML + QNN

```text
Model
  |
  v
Windows ML
  |
  v
QNN Execution Provider
  |
  v
Qualcomm Hexagon NPU
```

Advantages:

* Designed to provide a common Windows interface to hardware-specific execution providers.
* Supports Qualcomm QNN.
* Also provides a future path to GPU execution through DirectML.
* Better aligned with SnapLM's eventual cross-hardware architecture.

Current obstacle:

A usable native ARM64 Python version supported by Windows ML must be available.

---

### Path B — ONNX Runtime QNN

```text
Model
  |
  v
ONNX Runtime
  |
  v
QNN Execution Provider
  |
  v
HTP Backend
  |
  v
Hexagon NPU
```

Advantages:

* Direct QNN integration.
* Explicit HTP/NPU execution.
* Suitable for proving that the Hexagon NPU can execute a model.

Current obstacle:

The prebuilt Windows ARM64 Python package has specific Python-version requirements, requiring a suitable native ARM64 environment.

---

### Path C — GPU Acceleration

```text
Model
  |
  v
GPU-compatible runtime
  |
  v
DirectML / other backend
  |
  v
Adreno X1-45
```

This remains a secondary acceleration path if NPU execution is unavailable or unsuitable for a particular model.

---

## Current Runtime Architecture

```text
SnapLM
  |
  +-- Hardware Engine
  |      |
  |      +-- CPU
  |      +-- Memory
  |      +-- GPU
  |      +-- NPU
  |
  +-- Runtime Engine
         |
         +-- Ollama              DETECTED
         +-- Windows ML          TO TEST
         +-- QNN                 TO TEST
         +-- ONNX Runtime        TO TEST
         +-- DirectML            FUTURE
```

---

## Runtime Selection Strategy

For the initial Snapdragon proof-of-concept:

```text
Try Windows ML + QNN
        |
        +-- success
        |      |
        |      v
        |  benchmark NPU
        |
        +-- blocked
               |
               v
       ONNX Runtime QNN
               |
               v
       benchmark NPU
```

GPU acceleration will remain available as an additional route after the first NPU execution path has been demonstrated.

---

## Immediate Next Goal

Create a valid native ARM64 Python environment compatible with the selected acceleration runtime.

Then verify the following sequence:

```text
Runtime imports successfully
        |
        v
QNN provider discovered
        |
        v
QNN provider usable
        |
        v
Small ONNX model executes
        |
        v
Execution confirmed on NPU
        |
        v
Language model experiment
```

The NPU path will not be considered successful merely because QNN installs.

The proof-of-concept requires **actual model execution through the accelerator**.

---

## Long-Term SnapLM Implication

This investigation demonstrates why runtime detection belongs separately from hardware detection.

A machine may contain a functioning accelerator while having no compatible inference runtime installed.

SnapLM should eventually automate the reasoning currently being performed manually:

```text
Hardware exists?
        |
        v
Runtime installed?
        |
        v
Correct architecture?
        |
        v
Compatible execution provider?
        |
        v
Model compatible?
        |
        v
Benchmark
        |
        v
Recommend / Run
```

This runtime-awareness is a core part of SnapLM's intended role as an orchestration layer for local AI.
