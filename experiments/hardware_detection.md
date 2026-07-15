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