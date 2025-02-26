""" letter.py
=============
Letter class. """

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, TypedDict
from datetime import date
from benchmarks.metadata_extraction.person import Person


@dataclass
class Letter:
    """Representation of a letter."""
    document_number: str
    send_date: Optional[date] = None
    letter_title: Optional[str] = None
    sender_persons: Optional[List[Person]] = field(default_factory=list)
    receiver_persons: Optional[List[Person]] = field(default_factory=list)

    def __post_init__(self):
        # Convert sender and receiver strings to lists if necessary:
        self.sender_persons = self._split_and_process(self.sender_persons)
        self.receiver_persons = self._split_and_process(self.receiver_persons)

        # Normalize the date:
        if type(self.send_date) is list:
            self.send_date = self.send_date[0]

    @staticmethod
    def _split_and_process(persons):
        if persons is None:
            return None
        if isinstance(persons, str):
            persons = [p.strip() for p in persons.split('|')]
        return [Person.from_string(p) for p in persons]
