# SnapLM Development Progress

This document tracks the development of SnapLM, including completed milestones, observations, and upcoming work.

---

## Milestone 1 — Project Foundation

### Completed

- Created the SnapLM GitHub repository
- Added Apache 2.0 license
- Created the initial project structure
- Set up the `src/` Python package layout
- Added project documentation and experiment directories
- Created the initial development roadmap

### Project Structure

```text
snaplm/
├── docs/
├── experiments/
├── src/
│   └── snaplm/
├── tests/
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

---

## Milestone 2 — Basic Hardware Detection

### Goal

Determine whether SnapLM could retrieve useful information about the machine it was running on.

### Initial Implementation

The first hardware detector used:

- Python's `platform` module
- `psutil`

The initial output included:

```text
system: Windows
architecture: ARM64
processor: ARMv8 (64-bit) Family 8 Model 1 Revision 201, Qualcomm Technologies Inc
memory_gb: 15.61
```

### What I Learned

The basic Python APIs could identify the operating system, architecture, processor family, and installed memory.

However, `platform.processor()` did not return the friendly Snapdragon processor name.

This established the first limitation of relying entirely on generic Python system-information APIs.

---

## Milestone 3 — Structured Hardware Profile

### Goal

Restructure hardware detection so future components could consume the information more easily.

Instead of returning one flat dictionary, hardware detection was divided into separate functions:

```text
get_os()
get_cpu()
get_memory()
get_python()
get_hardware_info()
```

`get_hardware_info()` now acts as an aggregator that combines the individual hardware components into one structured profile.

### Current Structure

```text
Hardware Profile
│
├── OS
├── CPU
├── Memory
└── Python
```

### Why This Matters

SnapLM will eventually need considerably more information, including GPUs, NPUs, runtimes, inference backends, and accelerator capabilities.

Separating detection responsibilities now makes those components easier to add, test, and replace later.

---

## Milestone 4 — CLI and Python Packaging

### Goal

Turn SnapLM from a collection of Python scripts into an installable command-line application.

### Completed

- Added Typer for the CLI
- Created `pyproject.toml`
- Defined project dependencies
- Configured the SnapLM command entry point
- Installed SnapLM in editable mode

SnapLM can now be executed from anywhere using:

```powershell
snaplm
```

rather than:

```powershell
py src/snaplm/cli.py
```

The editable installation means changes to the source code are immediately reflected in the installed command during development.

---

## Milestone 5 — Improved Memory Detection

SnapLM now reports both installed and currently available memory.

Example:

```text
MEMORY
  total_gb: 15.61
  available_gb: 0.43
  used_gb: 15.18
  percent_used: 97.2
```

### Why This Matters

Total RAM alone is not sufficient for determining whether a model can be loaded.

For example, a model may theoretically fit within a 16 GB system while still failing to load if most of that memory is already being used.

Future model recommendations should therefore consider **available memory at runtime**, rather than only installed memory.

---

## Milestone 6 — GPU Detection

### Goal

Determine whether SnapLM could identify the GPU on Windows on ARM.

### Initial Investigation

Windows GPU information was queried using:

```powershell
Get-CimInstance Win32_VideoController
```

This successfully exposed:

- GPU name
- GPU vendor
- driver version
- device status

However, the reported `AdapterRAM` value was `0`, meaning this interface could not provide a useful GPU-memory figure on the development machine.

### Implementation

GPU detection was added to `hardware.py`.

Python invokes the Windows CIM query through `subprocess`, converts the PowerShell response to JSON, and parses the result into the SnapLM hardware profile.

The current GPU profile includes:

```text
GPU
  name: Qualcomm(R) Adreno(TM) X1-45 GPU
  vendor: Qualcomm Incorporated
  driver_version: 31.0.128.0
  status: OK
```

### Current Hardware Profile

SnapLM can currently detect:

```text
OS
├── name
├── version
└── architecture

CPU
├── name
├── physical cores
└── logical cores

Memory
├── total
├── available
├── used
└── utilization

GPU
├── name
├── vendor
├── driver version
└── status

Python
└── version
```

---

# Current Status

The basic hardware-detection layer is operational.

SnapLM can now identify the development machine as a Windows ARM64 system with a Qualcomm Adreno GPU and dynamically report its current memory availability.

However, **detecting an accelerator does not mean SnapLM can use it yet**.

The next stage is determining which machine-learning acceleration runtimes can actually access the detected GPU and NPU.

---

# Next Milestone — Accelerator Detection

## Goal

Move from:

```text
Accelerator exists
```

to:

```text
Accelerator exists
        ↓
Compatible runtime exists
        ↓
Runtime can execute model
```

### Investigation Targets

#### Adreno GPU

Investigate:

- DirectML
- Windows ML
- Vulkan

#### Hexagon NPU

Investigate:

- Qualcomm QNN
- Windows ML

SnapLM should eventually distinguish between:

```text
Hardware detected
Runtime available
Runtime compatible
Runtime successfully tested
```

---

# Upcoming Inference Experiment

Once an accelerated execution path is identified:

1. Select one small open-weight language model.
2. Establish CPU inference performance as a baseline.
3. Run the same model/workload through an accelerated backend.
4. Measure:
   - time to first token
   - tokens per second
   - memory usage
   - execution device
5. Compare results.

The immediate success criterion is:

> Run a local language model on the Snapdragon X Plus using an appropriate hardware accelerator rather than relying exclusively on CPU inference.

If this works, SnapLM will have demonstrated the core idea that originally motivated the project.