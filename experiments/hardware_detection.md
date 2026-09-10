# Hardware Detection Experiment

## Goal

Determine what hardware information SnapLM can currently retrieve from the system.

## Implementation

Used Python's:
- platform module
- psutil library

The current detector retrieves:
- operating system
- architecture
- processor information
- total system memory

## Command Used

```powershell
py experiments/test_hardware.py
```

## Output

```text
{'system': 'Windows', 'architecture': 'ARM64', 'processor': 'ARMv8 (64-bit) Family 8 Model 1 Revision 201, Qualcomm Technologies Inc', 'memory_gb': 15.61}
```


## Reflections

The first prototype successfully detects basic system information.

Observations:

- The system architecture is correctly identified as ARM64.
- The memory value matches the expected ~16 GB RAM.
- The processor information is too generic and does not identify the Snapdragon X Plus model.

## Lessons Learned

`platform.processor()` is not sufficient for detailed hardware identification.

A future implementation will need a more reliable method to detect:
- exact CPU model
- GPU
- NPU availability

## Next Steps

Investigate Windows hardware APIs and other methods for retrieving:
- Snapdragon CPU information
- Adreno GPU information
- Hexagon NPU information

### NPU Detection

The Windows Plug and Play device interface was queried to identify
compute accelerators:

```powershell
Get-PnpDevice | Where-Object {
    $_.FriendlyName -match "NPU|Neural|Hexagon|Qualcomm"
}

Windows successfully identified the Snapdragon NPU:

Class:        ComputeAccelerator
Name:         Snapdragon(R) X Plus - X1P42100 - Qualcomm(R) Hexagon(TM) NPU
Status:       OK

The signed driver information was then queried:

Get-CimInstance Win32_PnPSignedDriver |
Where-Object {
    $_.DeviceName -match "NPU|Neural|Hexagon"
} |
Select-Object DeviceName, DriverVersion, Manufacturer

Result:

Device:
Snapdragon(R) X Plus - X1P42100 - Qualcomm(R) Hexagon(TM) NPU

Driver:
30.0.216.0

Manufacturer:
Qualcomm Technologies, Inc.
Observation

The NPU is exposed by Windows as a ComputeAccelerator device and
reports a healthy status.

This establishes that the accelerator hardware and its Windows driver
are present.

However, hardware detection alone does not establish that an inference
runtime can successfully execute a language model on the NPU.

The next step is therefore runtime detection and an actual accelerated
inference test.


## Then we'll implement `get_npu()`

And this time **I want you to try writing part of it**, because you've already seen exactly how we implemented `get_gpu()`.

Conceptually we need:

```python
def get_npu():
    # Run PowerShell
    # Find ComputeAccelerator / Hexagon
    # Parse JSON
    # Return structured information

We want it eventually returning:

{
    "name": "Snapdragon(R) X Plus - X1P42100 - Qualcomm(R) Hexagon(TM) NPU",
    "vendor": "Qualcomm Technologies, Inc.",
    "driver_version": "30.0.216.0",
    "status": "OK",
}

## Milestone 7 — CPU Inference Baseline

### Goal

Determine whether the original SnapLM performance problem could be reproduced and measured rather than relying on subjective observations of model responsiveness.

### Result

A Qwen3 4B model was executed using Ollama 0.34.0.

Measured generation performance:

```text
~11.14 tokens/second
```

Ollama reported:

```text
PROCESSOR: 100% CPU
```

despite SnapLM independently detecting:

```text
Qualcomm Adreno X1-45 GPU
Qualcomm Hexagon NPU
```

### Significance

This confirms that the tested Ollama execution path is relying entirely on the CPU.

The result also refined the project's original hypothesis.

The issue is not simply whether the model can access the machine's RAM. The model successfully loads into system memory.

Instead, a central question for SnapLM is:

> Can a compatible inference runtime route the workload through the available GPU or NPU and provide meaningfully better performance?

This changes the immediate development focus from hardware identification to **runtime and accelerator utilization**.

---

## Current Pipeline

```text
Hardware Detection
        │
        ├── CPU ✓
        ├── Memory ✓
        ├── GPU ✓
        └── NPU ✓
              │
              ▼
CPU Baseline ✓
              │
              ▼
Runtime Detection
              │
              ▼
Accelerated Inference
              │
              ▼
Benchmark Comparison
              │
              ▼
Backend Selection
```

---

## Next Milestone — Accelerated Runtime Testing

### Objective

Determine whether the same class of language model can execute using the Adreno GPU or Hexagon NPU instead of relying exclusively on CPU inference.

Potential execution paths include:

```text
Adreno GPU
├── Windows ML
├── DirectML
└── other compatible GPU runtimes

Hexagon NPU
├── Qualcomm QNN
└── Windows ML / compatible execution providers
```

The successful path, if one exists, will be compared against the Ollama CPU baseline.

The primary metrics will include:

- execution device
- model/quantization
- generation speed
- time to first token where measurable
- total response duration
- memory consumption
- model loading time

### Success Criterion

The next major technical success for SnapLM is not merely detecting an accelerator.

It is demonstrating that a local language model can actually execute through an available accelerator and measuring whether doing so improves inference performance.

The NPU is exposed by Windows as a `ComputeAccelerator`, confirming that it is visible to the operating system independently of whether a particular LLM runtime currently uses it.