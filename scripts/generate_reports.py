import os
import csv
import json
import datetime
from collections import defaultdict

RESULTS_DIR = "results"
REPORTS_DIR = "reports"
ARCHIVE_DIR = "archive"


def load_test_results():
    """Load all test results from the results directory."""
    results = {}
    for filename in os.listdir(RESULTS_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(RESULTS_DIR, filename), "r") as f:
                results[filename] = json.load(f)
    return results


def create_overview(results):
    """Generate an overview of all tests."""
    overview_path = os.path.join(REPORTS_DIR, "overview.md")
    with open(overview_path, "w") as f:
        f.write("# Benchmark Overview\n\n")
        f.write("| Test Name | Provider | Model | Date | Score |\n")
        f.write("|---|---|---|---|---|\n")
        for test_name, result in results.items():
            f.write(
                f"| {test_name} | {result['provider']} | {result['model']} | {result['execution_time']} | {result['scores'].get('total', '-')} |\n")


def create_individual_reports(results):
    """Generate detailed reports for each test."""
    for test_name, result in results.items():
        test_report_path = os.path.join(REPORTS_DIR, f"tests/{test_name}.md")
        os.makedirs(os.path.dirname(test_report_path), exist_ok=True)
        with open(test_report_path, "w") as f:
            f.write(f"# Test Report: {test_name}\n\n")
            f.write(f"**Provider:** {result['provider']}\n\n")
            f.write(f"**Model:** {result['model']}\n\n")
            f.write(f"**Execution Time:** {result['execution_time']}\n\n")
            f.write("## Response:\n\n")
            f.write(f"```\n{json.dumps(result['response_text'], indent=4)}\n```\n")


def create_best_results(results):
    """Generate a summary of the best runs."""
    best_results_path = os.path.join(REPORTS_DIR, "best_results.md")
    best_scores = defaultdict(list)

    for test_name, result in results.items():
        total_score = result['scores'].get("total", 0)
        best_scores[result["model"]].append((total_score, test_name))

    with open(best_results_path, "w") as f:
        f.write("# Best Benchmark Results\n\n")
        f.write("| Model | Best Score | Test |\n")
        f.write("|---|---|---|\n")
        for model, runs in best_scores.items():
            runs.sort(reverse=True)  # Sort by score
            best_run = runs[0]
            f.write(f"| {model} | {best_run[0]} | {best_run[1]} |\n")


if __name__ == "__main__":
    os.makedirs(REPORTS_DIR, exist_ok=True)

    test_results = load_test_results()
    create_overview(test_results)
    create_individual_reports(test_results)
    create_best_results(test_results)

    print("Reports generated successfully!")
