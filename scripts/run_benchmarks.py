import csv
import importlib
import os
import sys
import logging
from benchmark_base import Benchmark
from dotenv import load_dotenv

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()

log_level = os.getenv('LOG_LEVEL', 'INFO').upper()

logging.basicConfig(
    level=log_level,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


BENCHMARKS_DIR = '../benchmarks'
CONFIG_FILE = os.path.join(BENCHMARKS_DIR, 'benchmarks.csv')

def get_api_key(provider):
    api_key = os.getenv(f'{provider.upper()}_API_KEY')
    if not api_key:
        raise ValueError(f"No API key found for {provider.upper()}")
    return api_key

def load_benchmark(test_config):
    benchmark_name = test_config['name']
    provider = test_config['provider']
    model = test_config['model']
    role_description = test_config.get('role_description', "A useful assistant that can help you with a variety of tasks.")
    prompt_file = test_config.get('prompt_file', 'prompt.txt')
    api_key = get_api_key(provider)
    benchmark_path = os.path.join(BENCHMARKS_DIR, benchmark_name)

    benchmark_file = os.path.join(benchmark_path, 'benchmark.py')

    if os.path.isfile(benchmark_file):
        spec = importlib.util.spec_from_file_location("benchmark_module", benchmark_file)
        benchmark_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(benchmark_module)
        # Class must have the same name as the benchmark folder but in CamelCase
        class_name = ''.join(part.capitalize() for part in benchmark_name.split('_'))
        benchmark_class = getattr(benchmark_module, class_name)
        return benchmark_class(benchmark_name, benchmark_path, provider, model, api_key, role_description, prompt_file)
    else:
        return Benchmark(benchmark_name, benchmark_path, provider, model, api_key, role_description, prompt_file)

def run_single_test(test_config):
    benchmark = load_benchmark(test_config)
    logger.info(f"Running {benchmark.title}...")
    benchmark.run()


def main():
    all_results = []

    # Open Config File and run each test in it
    with open(CONFIG_FILE, newline='', encoding='utf-8') as csvfile:
        tests = csv.DictReader(csvfile)
        for test in tests:
            if test.get('legacy_test', 'false').lower() == 'false':
                run_single_test(test)

    with open('../README.md', 'w') as readme:
        readme.write("# Benchmark Results\n\n")
        readme.write("\n".join(all_results))

if __name__ == "__main__":
    main()