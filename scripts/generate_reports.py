import json
import os
import csv
import hashlib
from collections import defaultdict

from scripts.data_loader import write_file, read_file
from scripts.report_helper import get_square, create_html_table, get_rectangle
from scripts.run_benchmarks import BENCHMARKS_DIR, CONFIG_FILE, REPORTS_DIR

def load_test_configuration(test_id):
    """Load the test configuration from the configuration file."""
    with open(CONFIG_FILE, newline='', encoding='utf-8') as csvfile:
        tests = csv.DictReader(csvfile)
        for test in tests:
            if test['id'] == test_id:
                return test

def load_all_benchmarks():
    """Load all benchmark results from the results directory."""
    results = []
    for benchmark in os.listdir(BENCHMARKS_DIR):
        if not os.path.isdir(os.path.join(BENCHMARKS_DIR, benchmark)):
            continue
        results.append(benchmark)
    return sorted(results)

def load_test_dates():
    """Load all test results from the results directory."""
    dates = []
    for benchmark in os.listdir(BENCHMARKS_DIR):
        if not os.path.isdir(os.path.join(BENCHMARKS_DIR, benchmark)):
            continue

        if os.path.isdir(os.path.join(BENCHMARKS_DIR, benchmark, "results")):
            for date_folder in os.listdir(os.path.join(BENCHMARKS_DIR, benchmark, "results")):
                if date_folder not in dates:
                    dates.append(date_folder)
    return sorted(dates, reverse=True)

def create_archive_overview(dates, benchmark_names):
    """Generate an overview of all tests."""
    overview_path = os.path.join(REPORTS_DIR, "archive", "overview.md")
    os.makedirs(os.path.dirname(overview_path), exist_ok=True)
    report_pages = []

    md_string =  ("# Benchmark Overview\n\n"
                 "This page provides an overview of all benchmark tests."
                 "Click on the test name to see the detailed results.\n\n")

    table_headers = ["Date"]
    for benchmark in benchmark_names:
        table_headers.append(benchmark)

    table_data = []

    for date in dates:
        row_data = [date]
        for benchmark in benchmark_names:
            result_path = os.path.join(BENCHMARKS_DIR, benchmark, "results", date)
            if os.path.exists(result_path):
                cell = ""
                for test in os.listdir(result_path):
                    if os.path.isdir(os.path.join(result_path, test)):
                        cell += get_square(test, href=f"/archive/{date}/{test}") + "&nbsp;"
            else:
                cell = ""
            row_data.append(cell)
        table_data.append(row_data)

    md_string += create_html_table(table_headers, table_data)
    write_file(overview_path, md_string)

def create_individual_reports():
    """Generate detailed reports for each test."""
    results = []

    for report in results:
        test = report["test"]

        config = load_test_configuration(test)
        date = report["date"]
        renders_directory = os.path.join(BENCHMARKS_DIR, report["name"], "renders", date, test)

        test_report_path = os.path.join(REPORTS_DIR, "archive", date, f"{test}.md")
        os.makedirs(os.path.dirname(test_report_path), exist_ok=True)

        test_score_path = os.path.join(BENCHMARKS_DIR, report["name"], "results", date, test, "scoring.json")
        if os.path.exists(test_score_path):
            with open(test_score_path, "r", encoding="utf-8") as f:
                score_data = json.load(f)

        with open(test_report_path, "w", encoding="utf-8") as f:
            f.write(f"# Test Report: {test}\n")
            f.write(f"![Provider](https://img.shields.io/badge/provider-{config['provider']}-brightgreen) ")
            f.write(f"![Model](https://img.shields.io/badge/model-{config['model'].replace("-", "--")}-blue)\n\n")
            f.write(f"**Date:** {date}\n")

            f.write("## Test Results\n")
            f.write(f"{score_data}\n")

            f.write("## Detailed Results\n")
            if os.path.exists(renders_directory):
                for render in os.listdir(renders_directory):
                    render_path = os.path.join(renders_directory, render)
                    with open(render_path, "r", encoding="utf-8") as r:
                        f.write(r.read())
                        f.write("\n\n")
            else:
                f.write("No renders available\n\n")


def create_index():
    """Generate the index page."""

    latest_results = defaultdict(list)

    with open(CONFIG_FILE, newline='', encoding='utf-8') as csvfile:
        tests = csv.DictReader(csvfile)

        for test in tests:
            test_name = test["name"]  # Get the test name
            latest_results[test_name].append(test["id"])  # Group by name

    latest_scores = {}
    RESULTS_DIR = "../benchmarks/test_benchmark2/results"

    # Get all available date folders (sorted by date descending)
    table_headers = ["Benchmark", "Latest Results"]
    table_data = []
    date_folders = []

    # Find the latest available date for each test
    if date_folders:
        latest_date = date_folders[0]  # Latest date (first after sorting)
        latest_date_path = os.path.join(RESULTS_DIR, latest_date)

        # Iterate over test folders within the latest date folder
        for test in os.listdir(latest_date_path):
            test_path = os.path.join(latest_date_path, test)
            scoring_file = os.path.join(test_path, "scoring.json")

            # Check if scoring.json exists
            if os.path.isfile(scoring_file):
                with open(scoring_file, "r", encoding="utf-8") as f:
                    try:
                        latest_scores[test] = json.load(f)
                    except json.JSONDecodeError:
                        latest_scores[test] = {}

        for test_name, test_ids in latest_results.items():
            table_row = [test_name]
            cell = ""
            for test_id in test_ids:
                cell += f"<a href='/archive/{latest_date}/{test_id}'>{test_id}</a> {latest_date}<br/>"
            table_row.append(cell)


    index_md = f"""
# Humanities Data Benchmark
Welcome to the **Humanities Data Benchmark** report page. This page provides an overview of all benchmark tests, 
results, and comparisons.

## Latest Benchmark Results
{create_html_table(table_headers, table_data)}

{latest_results}

{latest_scores}


## About This Page
This benchmark suite is designed to test **AI models** on humanities data tasks. The tests run **weekly** and 
results are automatically updated.

For more details, visit the [GitHub repository](https://github.com/RISE-UNIBAS/humanities_data_benchmark)."""

    write_file(os.path.join(REPORTS_DIR, "index.md"), index_md)

def create_tests_overview():
    """Generate an overview of all tests."""
    overview_path = os.path.join(REPORTS_DIR, "tests.md")

    # Markdown Header
    md_string = ("# Test Overview\n\n"
                 "This page provides an overview of all tests. "
                 "Click on the test name to see the detailed results.\n\n")

    table_headers = ["Test", "Name", "Provider", "Model", "Dataclass", "Temperature", "Role Description", "Prompt File", "Legacy Test"]
    table_data = []

    # Read CSV and populate table rows
    with open(CONFIG_FILE, newline='', encoding='utf-8') as csvfile:
        tests = csv.DictReader(csvfile)
        for test_config in tests:

            test_id = test_config['id']
            row_data = [
                get_square(test_id),
                f'<a href="/benchmarks/{test_config["name"]}/">{test_config["name"]}</a>',
                get_rectangle(test_config['provider']),
                get_rectangle(test_config['model']),
                test_config['dataclass'],
                test_config['temperature'],
                test_config['role_description'],
                test_config['prompt_file'],
                test_config['legacy_test']
            ]
            table_data.append(row_data)

    # Close table and add DataTables script
    md_string += create_html_table(table_headers, table_data)

    # Write to Markdown file
    with open(overview_path, "w", encoding="utf-8") as f:
        f.write(md_string)


def create_benchmark_overview(benchmark_name):
    readme_path = os.path.join(BENCHMARKS_DIR, benchmark_name, "README.md")
    readme_text = read_file(readme_path)

    benchmark_overview_path = os.path.join(REPORTS_DIR, "benchmarks", f"{benchmark_name}.md")
    os.makedirs(os.path.dirname(benchmark_overview_path), exist_ok=True)
    result_overview = f"## Test Results\n\n"

    overview = f"{readme_text}\n\n{result_overview}"
    write_file(benchmark_overview_path, overview)


def generate_site_navigation():
    """Generate site navigation."""
    mkdocs_yml = """
site_name: Humanities Data Benchmark

theme:
  name: material
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.expand
    - toc.integrate
    - search.suggest
    - search.highlight

nav:
  - Home: index.md
  - Tests: tests.md"""

    mkdocs_yml += """\n
  - Benchmarks:"""

    for filename in os.listdir(BENCHMARKS_DIR):
        if not os.path.isdir(os.path.join(BENCHMARKS_DIR, filename)):
            continue
        mkdocs_yml += f"\n    - {filename}: benchmarks/{filename}.md"

    mkdocs_yml += """\n  - Archive:
    - Overview: archive/overview.md"""

    for date in os.listdir(os.path.join(REPORTS_DIR, "archive")):
        if os.path.isdir(os.path.join(REPORTS_DIR, "archive", date)):
            mkdocs_yml += f"\n    - {date}:"
            for test in os.listdir(os.path.join(REPORTS_DIR, "archive", date)):
                mkdocs_yml += f"\n        - {test.replace('.md', '')}: archive/{date}/{test}"

    mkdocs_yml += """

markdown_extensions:
  - toc:
      permalink: true
  - admonition
  - pymdownx.details
  - pymdownx.superfences
"""
    write_file("../mkdocs.yml", mkdocs_yml)


if __name__ == "__main__":
    os.makedirs(REPORTS_DIR, exist_ok=True)

    test_dates = load_test_dates()
    benchmarks = load_all_benchmarks()

    create_index()  # Creates the base file for the reports

    for benchmark in benchmarks:
        create_benchmark_overview(benchmark)   # Generate benchmark overview:
                                               # -> Copies Readme and adds test results

    create_archive_overview(test_dates, benchmarks)
    create_individual_reports()
    create_tests_overview()


    generate_site_navigation()  # Generate mkdocs.yml
    create_index()


    print("Reports generated successfully!")
