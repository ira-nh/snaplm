## GPU Detection

### Goal

Detect the system GPU and collect information that may be relevant to local LLM inference and backend selection.

Relevant information may include:

- GPU name
- GPU vendor
- Driver version
- Available GPU memory
- Whether the GPU uses dedicated or shared/unified memory
- Potential hardware acceleration capabilities

### Initial Windows Approach

Windows provides GPU information through `Win32_VideoController`, which can be queried using PowerShell:

```powershell
Get-CimInstance Win32_VideoController | Select-Object Name, AdapterCompatibility, AdapterRAM, DriverVersion
```

On the development machine, this returned:

```Name:                  Qualcomm(R) Adreno(TM) X1-45 GPU
AdapterCompatibility:  Qualcomm Incorporated
AdapterRAM:            0
DriverVersion:         31.0.98.
```

### Observation

The GPU name, vendor, and driver version can be retrieved successfully.

However, AdapterRAM is reported as 0. This does not necessarily mean that the GPU has no usable memory. The development machine uses a Snapdragon platform with unified/shared memory, so the AdapterRAM field may not represent the memory available to the GPU in a useful way.

Therefore, SnapLM should not assume that AdapterRAM is an accurate representation of GPU memory on unified-memory systems.