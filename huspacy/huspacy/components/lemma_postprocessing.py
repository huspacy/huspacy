"""
This module contains various rule-based components aiming to improve on baseline lemmatization tools.
"""

import re
from typing import List, Callable

from spacy.lang.hu import Hungarian
from spacy.pipeline import Pipe
from spacy.tokens import Token
from spacy.tokens.doc import Doc


@Hungarian.component(
    "lemma_case_smoother",
    assigns=["token.lemma"],
    requires=["token.lemma", "token.pos"],
)
def lemma_case_smoother(doc: Doc) -> Doc:
    """Smooth lemma casing by POS.

    DEPRECATED: This is not needed anymore, as the lemmatizer is now case-insensitive.

    Args:
        doc (Doc): Input document.

    Returns:
        Doc: Output document.
    """
    for token in doc:
        if token.is_sent_start and token.tag_ != "PROPN":
            token.lemma_ = token.lemma_.lower()

    return doc


class LemmaSmoother(Pipe):
    """Smooths lemma by fixing common errors of the edit-tree lemmatizer."""

    _DATE_PATTERN = re.compile(r"(\d+)-j?[éá]?n?a?(t[őó]l)?")
    _NUMBER_PATTERN = re.compile(r"(\d+([-,/_.:]?(._)?\d+)*%?)")

    # noinspection PyUnusedLocal
    @staticmethod
    @Hungarian.factory("lemma_smoother", assigns=["token.lemma"], requires=["token.lemma", "token.pos"])
    def create_lemma_smoother(nlp: Hungarian, name: str) -> "LemmaSmoother":
        return LemmaSmoother()

    def __call__(self, doc: Doc) -> Doc:
        rules: List[Callable] = [
            self._remove_exclamation_marks,
            self._remove_question_marks,
            self._remove_date_suffixes,
            self._remove_suffix_after_numbers,
        ]

        for token in doc:
            for rule in rules:
                rule(token)

        return doc

    @classmethod
    def _remove_exclamation_marks(cls, token: Token) -> None:
        """Removes exclamation marks from the lemma.

        Args:
            token (Token): The original token.
        """

        if "!" != token.lemma_:
            exclamation_mark_index = token.lemma_.find("!")
            if exclamation_mark_index != -1:
                token.lemma_ = token.lemma_[:exclamation_mark_index]

    @classmethod
    def _remove_question_marks(cls, token: Token) -> None:
        """Removes question marks from the lemma.

        Args:
            token (Token): The original token.
        """

        if "?" != token.lemma_:
            question_mark_index = token.lemma_.find("?")
            if question_mark_index != -1:
                token.lemma_ = token.lemma_[:question_mark_index]

    @classmethod
    def _remove_date_suffixes(cls, token: Token) -> None:
        """Fixes the suffixes of dates.

        Args:
            token (Token): The original token.
        """

        if token.pos_ == "NOUN":
            match = cls._DATE_PATTERN.match(token.lemma_)
            if match is not None:
                token.lemma_ = match.group(1) + "."

    @classmethod
    def _remove_suffix_after_numbers(cls, token: Token) -> None:
        """Removes suffixes after numbers.

        Args:
            token (str): The original token.
        """

        if token.pos_ == "NUM":
            match = cls._NUMBER_PATTERN.match(token.text)
            if match is not None:
                token.lemma_ = match.group(0)
