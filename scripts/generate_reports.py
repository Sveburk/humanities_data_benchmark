import os
import csv
import json
from collections import defaultdict

from scripts.data_loader import write_file, read_file
from scripts.run_benchmarks import BENCHMARKS_DIR, CONFIG_FILE

RESULTS_DIR = "results"
REPORTS_DIR = "../docs"
ARCHIVE_DIR = "archive"

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
        for date_folder in os.listdir(os.path.join(BENCHMARKS_DIR, benchmark, "results")):
            if date_folder not in dates:
                dates.append(date_folder)
    return sorted(dates, reverse=True)


def create_overview(dates, benchmark_names):
    """Generate an overview of all tests."""
    overview_path = os.path.join(REPORTS_DIR, "overview.md")
    report_pages = []

    md_string = ("# Benchmark Overview\n\n"
                 "This page provides an overview of all benchmark tests."
                 "Click on the test name to see the detailed results.\n\n")

    md_string += "| Date |"
    for benchmark in benchmark_names:
        md_string += f" {benchmark} |"
    md_string += "\n"
    md_string += "| --- |"
    for _ in benchmark_names:
        md_string += " --- |"
    md_string += "\n"

    for date in dates:
        md_string += f"| {date} |"
        for benchmark in benchmark_names:
            result_path = os.path.join(BENCHMARKS_DIR, benchmark, "results", date)
            if os.path.exists(result_path):
                for test in os.listdir(result_path):
                    if os.path.isdir(os.path.join(result_path, test)):
                        report = f"tests/{date}/{test}.md"
                        md_string += f' [{test}]({report})'
                        report_pages.append({
                            "name": benchmark,
                            "date": date,
                            "test": test,
                            "report": report
                        })
                md_string += "|"
            else:
                md_string += " |"
        md_string += "\n"

    with open(overview_path, "w") as f:
        f.write(md_string)

    return report_pages

def create_individual_reports(results):
    """Generate detailed reports for each test."""

    for report in results:
        test = report["test"]

        config = load_test_configuration(test)
        date = report["date"]
        renders_directory = os.path.join(BENCHMARKS_DIR, report["name"], "renders", date, test)

        test_report_path = os.path.join(REPORTS_DIR, "tests", date, f"{test}.md")
        os.makedirs(os.path.dirname(test_report_path), exist_ok=True)

        with open(test_report_path, "w", encoding="utf-8") as f:
            f.write(f"# Test Report: {test}\n")
            f.write(f"![Provider](https://img.shields.io/badge/provider-{config['provider']}-brightgreen) ")
            f.write(f"![Model](https://img.shields.io/badge/model-{config['model'].replace("-", "--")}-blue)\n\n")
            f.write(f"**Date:** {date}\n")

            f.write("## Test Results\n")
            f.write("TODO: Add test results here\n\n")

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
    return "INDEX"

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
  - Overview: overview.md
  - Benchmarks:"""

    for filename in os.listdir(BENCHMARKS_DIR):
        if not os.path.isdir(os.path.join(BENCHMARKS_DIR, filename)):
            continue
        mkdocs_yml += f"\n    - {filename}: benchmarks/{filename}.md"

    mkdocs_yml += """\n  - Tests:"""

    for date in os.listdir(os.path.join(REPORTS_DIR, "tests")):
        mkdocs_yml += f"\n    - {date}:"
        for test in os.listdir(os.path.join(REPORTS_DIR, "tests", date)):
            mkdocs_yml += f"\n        - {test.replace('.md', '')}: tests/{date}/{test}"

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

    benchmarks = load_all_benchmarks()
    for benchmark in benchmarks:
        create_benchmark_overview(benchmark)

    generate_site_navigation()  # Generate mkdocs.yml
    test_dates = load_test_dates()  # Load all test dates
    create_index()
    referenced_tests = create_overview(test_dates, benchmarks)
    create_individual_reports(referenced_tests)

    print("Reports generated successfully!")
