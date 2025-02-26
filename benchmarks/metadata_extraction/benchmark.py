from __future__ import annotations
from scripts.benchmark_base import Benchmark

import pandas as pd
import csv
import json
import os
import logging


class MetadataExtraction(Benchmark):

    @property
    def resize_images(self):
        """If images are too large, resize them before sending to the model."""
        return False

    @property
    def update_required(self) -> bool:
        """ If an update of the ground truth is required before running the benchmark. """
        return True

    def update_ground_truth(self) -> None:
        """ Update the ground truth. """
        ground_truth_path = os.path.join(self.benchmark_dir, "ground_truths")
        try:
            self.update_persons(persons_csv=f"{ground_truth_path}/persons.csv",
                                persons_json=f"{ground_truth_path}/persons.json")
        except FileNotFoundError:
            logging.error(
                f"Ground truth not found: {ground_truth_path}/persons.csv")
        try:
            self.update_letters(letters_csv=f"{ground_truth_path}/letters.csv",
                                letters_json_dir=ground_truth_path)
        except FileNotFoundError:
            logging.error(
                f"Ground truth not found: {ground_truth_path}/letters.csv")

    @staticmethod
    def update_persons(persons_csv: str,
                       persons_json: str) -> None:
        """ Convert persons ground truth from a GoogleSheets export CSV to JSON file.

        :param persons_csv: file path of CSV file containing persons ground truth exported from Google Sheets
        :param persons_json: file path of JSON file to save the converted ground truth to
        """

        persons_df = pd.read_csv(persons_csv)
        grouped_persons = persons_df.groupby("identifier_value")
        persons = []

        for identifier, rows in grouped_persons:
            first_row = rows.iloc[0]
            logging.info(f"Added person {first_row["identifier_value"]}...")
            person = {
                "@context": "http://schema.org",
                "@type": "Person",
                "identifier": [
                    {
                        "@type": "PropertyValue",
                        "propertyID": first_row["identifier_propertyID"],
                        "value": str(first_row["identifier_value"]) if pd.notna(first_row["identifier_value"]) else None
                    }
                ],
                "name": first_row["name"],
                "alternateName":  [name.strip() for name in first_row["alternateName"].split(",")] if pd.notna(first_row["alternateName"]) else [],
                "birthDate": str(first_row["birthDate"]) if pd.notna(first_row["birthDate"]) else None,
                "deathDate": str(first_row["deathDate"]) if pd.notna(first_row["deathDate"]) else None,
                "description": first_row["description"] if pd.notna(first_row["description"]) else "",
                "hasOccupation": [],
                "citation": []
            }

            for _, row in rows.iterrows():
                job = {
                    "@type": "Occupation",
                    "name": row["job_name"],
                    "startDate": str(row["job_startDate"]) if pd.notna(row["job_startDate"]) else None,
                    "endDate": str(row["job_endDate"]) if pd.notna(row["job_endDate"]) else None,
                    "employer": {
                        "@type": "Organization",
                        "name": row["employer_name"],
                        "identifier": [
                            {
                                "@type": "PropertyValue",
                                "propertyID": row["employer_identifier_propertyID"],
                                "value": str(row["employer_identifier_value"]) if pd.notna(row["employer_identifier_value"]) else None # int(row["employer_identifier_value"])
                            }
                        ]
                    }
                }
                person["hasOccupation"].append(job)

                citation = {
                    "@type": "CreativeWork",
                    "name": row["citation_name"],
                    "url": row["citation_url"]
                }
                if citation not in person["citation"]:
                    person["citation"].append(citation)

            persons.append(person)

        with open(persons_json, "w", encoding="utf-8") as jsonfile:
            json.dump(persons, jsonfile, indent=4)

    def update_letters(self,
                       letters_csv: str,
                       letters_json_dir: str) -> None:
        """ Convert letters ground truth from a CSV to JSON files.

        :param letters_csv: file path of CSV file containing letters ground truth
        :param letters_json_dir: directory to save the converted ground truth to
        """

        with open(letters_csv, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data = {
                    "letter_title": self.split_by_pipe(row["letter_title"]),
                    "send_date": self.split_by_pipe(row["send_date"]),
                    "sender_persons": self.split_by_pipe(row["sender_persons"]),
                    "receiver_persons": self.split_by_pipe(row["receiver_persons"])
                }

                doc_num = row["document_number"]
                filename = os.path.join(letters_json_dir, f"letter{doc_num}.json")

                with open(filename, "w", encoding="utf-8") as jsonfile:
                    json.dump(data, jsonfile, indent=4)

    @staticmethod
    def split_by_pipe(cell) -> list[str]:
        """ Splits a CSV cell by the pipe '|' character and strips whitespace. """

        return [s.strip() for s in cell.split('|') if s.strip()]
