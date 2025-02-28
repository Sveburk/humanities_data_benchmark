from __future__ import annotations

from scripts.benchmark_base import Benchmark
from benchmarks.metadata_extraction.letter import Letter
from benchmarks.metadata_extraction.person import Person
import pandas as pd
import csv
import json
import os
import logging
from typing import Literal


class MetadataExtraction(Benchmark):


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
            logging.debug(f"Added person {first_row["identifier_value"]}...")
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
                "alternateName": [name.strip() for name in first_row["alternateName"].split(",")] if pd.notna(
                    first_row["alternateName"]) else [],
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
                                "value": str(row["employer_identifier_value"]) if pd.notna(
                                    row["employer_identifier_value"]) else None  # int(row["employer_identifier_value"])
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
    def split_by_pipe(cell: str) -> list[str]:
        """ Splits a CSV cell by the pipe '|' character and strips whitespace. """

        return [s.strip() for s in cell.split('|') if s.strip()]

    def score_request_answer(self,
                     image_name: str,
                     response: dict,
                     ground_truth: dict) -> dict:
        """ Score the answer.

        :param image_name: the name of the image
        :param response: the response
        :param ground_truth: the ground truth
        """

        logging.debug(f"image_name: {image_name}")
        logging.debug(f"response: {response}")
        logging.debug(f"ground_truth: {ground_truth}")

        try:
            raw_response_letter = response["response_text"]["metadata"]
            raw_response_letter["document_number"] = image_name
            response_letter = Letter(**raw_response_letter)
        except ValueError:
            logging.error(f"Error parsing response for {image_name}")

        try:
            ground_truth["document_number"] = image_name
            ground_truth_letter = Letter(**ground_truth)
        except ValueError:
            logging.error(f"ValueError parsing ground_truth for {image_name}")
        except TypeError:
            logging.error(f"TypeError parsing ground_truth for {image_name}")

        logging.debug(f"response_letter: {response_letter}")
        logging.debug(f"ground_truth_letter: {ground_truth_letter}")

        score = self.score_send_date(ground_truth_letter=ground_truth_letter,
                                     predicted_letter=response_letter)

        try:
            persons = json.load(open(os.path.join(self.benchmark_dir, "ground_truths", "persons.json")))
        except FileNotFoundError:
            logging.error("Persons ground truth not found.")

        score = score | self.score_persons(sender_or_receiver="sender",
                                           ground_truth_letter=ground_truth_letter,
                                           predicted_letter=response_letter,
                                           persons=persons,
                                           inferred_from_function=False,
                                           inferred_from_correspondence=False)

        score = score | self.score_persons(sender_or_receiver="receiver",
                                           ground_truth_letter=ground_truth_letter,
                                           predicted_letter=response_letter,
                                           persons=persons,
                                           inferred_from_function=False,
                                           inferred_from_correspondence=False)
        return score

    @staticmethod
    def score_send_date(ground_truth_letter: Letter,
                        predicted_letter: Letter) -> dict[str, int]:
        """ Score 'send_date'. """

        predicted_date = predicted_letter.send_date
        ground_truth_date = ground_truth_letter.send_date

        # remove name artifacts and duplicates:
        ground_truth_date = {ground_truth_date}
        predicted_date = {predicted_date}
        try:
            predicted_date.remove("null")
        except KeyError:
            pass
        try:
            predicted_date.remove(None)
        except KeyError:
            pass

        logging.debug(f"ground_truth_date: {ground_truth_date}")
        logging.debug(f"predicted_date: {predicted_date}")

        return {"send_date_tp": len(ground_truth_date & predicted_date),
                "send_date_fp": len(predicted_date - ground_truth_date),
                "send_date_fn": len(ground_truth_date - predicted_date)}

    def score_persons(self,
                      sender_or_receiver: Literal["sender", "receiver"],
                      ground_truth_letter: Letter,
                      predicted_letter: Letter,
                      persons: dict,
                      inferred_from_function: bool = False,
                      inferred_from_correspondence: bool = False) -> dict[str, int]:
        """ Score 'sender_persons' or 'receiver_persons'.

        :param sender_or_receiver: whether to score by sender or receiver persons
        :param ground_truth_letter: the ground truth letter
        :param predicted_letter: the predicted letter
        :param persons: the persons ground_truth
        :param inferred_from_function: whether sender person was inferred from function, defaults to False
        :param inferred_from_correspondence: whether sender person was inferred from correspondence, defaults to False
        """

        # select ground truth persons:
        ground_truth_persons = []
        for person in ground_truth_letter.__getattribute__(f"{sender_or_receiver}_persons"):
            if inferred_from_function is False and person.inferred_from_function is True:
                continue
            elif inferred_from_correspondence is False and person.inferred_from_correspondence is True:
                continue
            else:
                ground_truth_persons.append(person)

        # select predicted persons:
        predicted_persons = []
        if predicted_letter.__getattribute__(f"{sender_or_receiver}_persons") is not None:
            predicted_persons = predicted_letter.__getattribute__(f"{sender_or_receiver}_persons")
        predicted_persons = [predicted_person.name for predicted_person in predicted_persons]

        # match predicted persons to their preferred name variant:
        matched_predicted_persons = []
        for predicted_person in predicted_persons:
            matched = False
            for ground_truth_person in ground_truth_persons:
                if ground_truth_person.name == predicted_person:
                    matched_predicted_persons.append(predicted_person)
                    matched = True
                    break
                else:
                    match = self._match_person(persons=persons,
                                               ground_truth_person=ground_truth_person,
                                               predicted_person=predicted_person)
                    if match is not None:
                        matched_predicted_persons.append(match)
                        matched = True
                        break
            if not matched:
                matched_predicted_persons.append(predicted_person)

        # normalize persons:
        ground_truth_persons = set([person.name for person in ground_truth_persons if person.name != "None"])
        predicted_persons = set()
        for predicted_person in matched_predicted_persons:
            if predicted_person == "null":
                continue
            elif predicted_person is None:
                continue
            else:
                predicted_persons.add(predicted_person)

        return {f"{sender_or_receiver}_persons_tp": len(ground_truth_persons & predicted_persons),
                f"{sender_or_receiver}_persons_fp": len(predicted_persons - ground_truth_persons),
                f"{sender_or_receiver}_persons_fn": len(ground_truth_persons - predicted_persons)}

    @staticmethod
    def _match_person(persons: dict,
                      ground_truth_person: Person,
                      predicted_person: str) -> str | None:
        """ Match predicted person to ground truth person name variant. """

        for person in persons:
            if ground_truth_person.name == person["name"]:
                if predicted_person in person["alternateName"]:
                    return ground_truth_person.name

        return None
