## Benchmark 001 — Ollama CPU Baseline

### Objective

Establish a baseline for local LLM inference on the development machine before attempting GPU or NPU acceleration.

One of the original motivations behind SnapLM was the hypothesis that Ollama was executing local models primarily on the CPU despite the presence of an Adreno GPU and Hexagon NPU.

This experiment tests that hypothesis and establishes a performance baseline for future accelerated runtimes.

### System

```text
Device: Lenovo IdeaPad Slim 5 14Q8X9
Processor: Snapdragon X Plus X1P-42-100
Architecture: ARM64
RAM: 15.61 GB
GPU: Qualcomm Adreno X1-45
NPU: Qualcomm Hexagon
Ollama: 0.34.0
```

Available RAM before the benchmark was approximately:

```text
3.77 GB
```

### Model

```text
Model: qwen3:4b
Installed size: 2.5 GB
Loaded size reported by Ollama: 3.2 GB
Context: 4096
```

### Prompt

```text
Explain what DNA is in approximately 100 words.
```

The same prompt should be reused in later benchmarks where possible to make runtime comparisons more meaningful.

### Ollama API Results

```text
prompt_eval_count: 23
prompt_eval_duration: 99,700,000 ns

eval_count: 423
eval_duration: 37,962,959,000 ns

load_duration: 3,892,600 ns
total_duration: 38,088,365,600 ns
```

Converted:

```text
Generated tokens: 423
Generation duration: ~37.96 s
Generation speed: ~11.14 tokens/s
Total request duration: ~38.09 s
Load duration: ~0.004 s
```

The extremely short load duration suggests that the model was already warm/loaded when this measurement was taken.

Therefore, this benchmark primarily represents **generation performance**, rather than cold-start loading performance.

### Execution Device

After generation:

```powershell
ollama ps
```

returned:

```text
NAME        SIZE      PROCESSOR    CONTEXT
qwen3:4b    3.2 GB    100% CPU     4096
```

### Key Finding

The model was executing **100% on the CPU**.

The system's detected Adreno GPU and Hexagon NPU were not being used by this Ollama execution path.

This provides direct evidence supporting one of the original motivations behind SnapLM:

> A model may fit within system memory and run successfully while still failing to take advantage of available hardware acceleration.

### Interpretation

The original hypothesis was that poor local inference performance resulted from the Snapdragon system's shared/unified memory architecture not being properly utilized.

The current evidence suggests a more precise explanation:

- The model can be loaded into system memory successfully.
- The machine exposes both GPU and NPU acceleration hardware.
- Ollama nevertheless reports this workload as executing entirely on the CPU.
- Therefore, accelerator utilization—not simply the ability to access RAM—is an important part of the performance problem.

### Next Experiment

Benchmark `qwen3:8b` using the same:

- machine
- Ollama version
- prompt
- context configuration

This will establish how CPU inference performance scales as model size increases.

After the CPU baselines are established, equivalent or comparable models will be tested through accelerated execution paths where possible.