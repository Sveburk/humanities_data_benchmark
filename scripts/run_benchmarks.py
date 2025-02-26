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
CONFIG_FILE = os.path.join(BENCHMARKS_DIR, 'benchmarks_tests.csv')

def get_api_key(provider):
    """Get the API key for the provider."""
    api_key = os.getenv(f'{provider.upper()}_API_KEY')
    if not api_key:
        raise ValueError(f"No API key found for {provider.upper()}")
    return api_key


def load_benchmark(test_config):
    """Load the benchmark class from the benchmark folder."""
    benchmark_name = test_config['name']
    api_key = get_api_key(test_config['provider'])
    benchmark_path = os.path.join(BENCHMARKS_DIR, benchmark_name)
    benchmark_file = os.path.join(benchmark_path, 'benchmark.py')

    if os.path.isfile(benchmark_file):
        spec = importlib.util.spec_from_file_location("benchmark_module", benchmark_file)
        benchmark_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(benchmark_module)
        # Class must have the same name as the benchmark folder but in CamelCase
        class_name = ''.join(part.capitalize() for part in benchmark_name.split('_'))
        benchmark_class = getattr(benchmark_module, class_name)
        logger.info(f"Loaded {benchmark_name} from {benchmark_file}")
        return benchmark_class(test_config, api_key, benchmark_path)
    else:
        logger.info(f"Loaded {benchmark_name} from Benchmark class")
        return Benchmark(test_config, api_key, benchmark_path)


def create_result_table(results):
    # First, gather all possible scores to handle missing data
    scores = set()
    for val in results.values():
        scores.update(val.keys())

    scores = sorted(scores)

    # Create header
    header = "key | " + " | ".join(scores)
    separator = " | ".join(['---'] * (len(scores) + 1))

    # Build rows
    rows = []
    for key, val in results.items():
        row = [key]
        for score in scores:
            row.append(str(val.get(score, '-')))
        rows.append(" | ".join(row))

    # Combine everything
    md_table = f"{header}\n{separator}\n" + "\n".join(rows)

    table_path = os.path.join("..", "benchmarks", 'result_table.md')
    with open(table_path, 'w', encoding='utf-8') as f:
        f.write(md_table)


def run_single_test(test_config):
    """Run a single test."""
    benchmark = load_benchmark(test_config)
    logger.info(f"Running {benchmark.title}...")
    return benchmark.run()


def main():
    # Open Config File and run each test in it
    with open(CONFIG_FILE, newline='', encoding='utf-8') as csvfile:
        tests = csv.DictReader(csvfile)
        all_results = {}
        for test in tests:
            if test.get('legacy_test', 'false').lower() == 'false':
                results = run_single_test(test)
                all_results.update(results)
        create_result_table(all_results)

    ### Single Test
    # test_config = {
    #     'name': 'folder_name',
    #     'provider': 'openai',
    #     'model': 'gpt-40',
    #     '
    #     'role_description': 'A useful assistant that can help you with a variety of tasks.',
    #     'prompt_file': 'prompt.txt'
    # }
    # run_single_test(test_config)

if __name__ == "__main__":
    main()