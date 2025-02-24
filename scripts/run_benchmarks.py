import os
import importlib.util
from benchmark_base import Benchmark

BENCHMARKS_DIR = '../benchmarks'

def load_benchmark(benchmark_name, benchmark_path, provider, model, api_key, role_description):
    benchmark_file = os.path.join(benchmark_path, 'benchmark.py')
    if os.path.isfile(benchmark_file):
        spec = importlib.util.spec_from_file_location("benchmark_module", benchmark_file)
        benchmark_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(benchmark_module)
        class_name = ''.join(part.capitalize() for part in benchmark_name.split('_'))
        benchmark_class = getattr(benchmark_module, class_name)
        return benchmark_class(benchmark_name, benchmark_path, provider, model, api_key, role_description)
    else:
        return Benchmark(benchmark_name, benchmark_path, provider, model, api_key, role_description)

def main():
    benchmarks = [d for d in os.listdir(BENCHMARKS_DIR)
                  if os.path.isdir(os.path.join(BENCHMARKS_DIR, d))]

    provider = os.getenv('LLM_PROVIDER', 'openai')
    model = os.getenv('LLM_MODEL', 'gpt-4')
    api_key = os.getenv(f'{provider.upper()}_API_KEY')
    role_description = "You are an assistant"

    if not api_key:
        raise ValueError(f"API key for provider '{provider}' not found in environment variables.")

    all_results = []

    for benchmark_name in benchmarks:
        benchmark_path = os.path.join(BENCHMARKS_DIR, benchmark_name)
        benchmark_instance = load_benchmark(benchmark_name, benchmark_path, provider, model, api_key, role_description)
        print(f"Running {benchmark_name}...")
        benchmark_instance.run()
        all_results.append(f"- [{benchmark_name} results](benchmarks/{benchmark_name}/result_table.md)")

    with open('../README.md', 'w') as readme:
        readme.write("# Benchmark Results\n\n")
        readme.write("\n".join(all_results))

if __name__ == "__main__":
    main()
