# humanities_data_benchmark

## Introduction

This repository contains benchmarks designed to evaluate the performance of large language models (LLMs) on various tasks relevant to humanities data, including transcription, metadata extraction, entity recognition, and other specialized text-based tasks. Each benchmark provides a clear and structured way to test and compare different models, facilitating systematic assessments and transparent reporting of results.

The benchmarks are structured to offer flexibility: generic workflows can be used directly, or customized workflows can be implemented to address unique benchmarking requirements.

## Result Overview

The table below summarizes the current benchmarks and their overall scores:

| Benchmark Name | Accuracy (%) | Detailed Results |
|----------------|--------------|------------------|


## Create New Benchmark

To add a new benchmark to the repository, follow these steps:

1. **Create a benchmark folder** in the `benchmarks/` directory:

```bash
mkdir benchmarks/your_benchmark_name
```

2. **Organize your files** within the benchmark folder as follows:

```
your_benchmark_name/
├── images/
│   └── image1.png
│   └── image2.png
├── truths/
│   └── image1.txt
│   └── image2.txt
└── prompt.txt
```

- Place your benchmark images in the `images/` directory.
- Add corresponding ground-truth text files in the `truths/` directory.
- Write a clear prompt for the LLM in the `prompt.txt` file.

3. **Optional: Add custom behavior**:

If your benchmark requires custom handling, scoring, or specific processing, create a file named `benchmark.py` inside your benchmark folder:

```python
from benchmarks_base import Benchmark

class YourBenchmarkName(Benchmark):

    def ask_llm(self, image):
        # Custom LLM interaction code
        pass

    def score_answer(self, image_name, answer):
        # Custom scoring logic
        pass
```

4. **Run the benchmarks** from the `scripts/` directory to test and integrate your new benchmark:

```bash
python scripts/run_benchmarks.py
```

This will generate results, update tables, and automatically include your benchmark in the overview table above.

