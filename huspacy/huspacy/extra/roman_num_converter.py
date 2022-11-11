"""
Facilities for converting roman numbers to arabic
"""
import re
from typing import List

from spacy import Language
from spacy.pipeline import Pipe
from spacy.tokens import Doc


class RomanToArabic(Pipe):
    """Converts roman numerals to arabic numerals."""

    # noinspection PyMissingOrEmptyDocstring,PyUnusedLocal
    @staticmethod
    @Language.factory("roman_to_arabic", assigns=["token.lemma"], requires=["token.text"])
    def create_component(nlp: Language, name: str):
        return RomanToArabic()

    def __init__(self):
        self._regex = re.compile(r"^([IVXLCDM]+(-[IVXLCDM]+)*)[.]?$")
        self._rom_val = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000,
        }

    def __call__(self, doc: Doc) -> Doc:
        for token in doc:
            match = self._regex.search(token.text)
            if match is None:
                continue

            roman: str = match.group(0)
            romans: List[str] = roman.split("-")
            values = []

            for r in romans:
                dot = "." if "." == r[-1] else ""
                r = r[:-1] if dot else r

                int_val = 0
                for i in range(len(r)):
                    if i > 0 and self._rom_val[r[i]] > self._rom_val[r[i - 1]]:
                        int_val += self._rom_val[r[i]] - 2 * self._rom_val[r[i - 1]]
                    else:
                        int_val += self._rom_val[r[i]]

                values.append(str(int_val) + dot)

            token.lemma_ = "-".join(values)
        return doc
