import re
from typing import Optional

from spacy.language import Language
from spacy.pipeline import Pipe
from spacy.tokens import Token
from spacy.tokens.doc import Doc


class HunSentencizer(Pipe):
    """Sentencizer component which uses simple rules to split the text to sentences."""

    @staticmethod
    @Language.factory("hun_sentencizer")
    def create_sentencizer(nlp: Language, name: str) -> "HunSentencizer":
        return HunSentencizer()

    # noinspection PyUnusedLocal
    def __init__(self):
        self._boundary_punct_pattern = re.compile(r"^([.?!]+)$")
        self._quote_or_bracket = {'"', ")"}
        self._mdash = "—"

    def __call__(self, doc: Doc) -> Doc:
        doc[0].is_sent_start = True

        token: Token
        for token in doc[:-1]:
            next_token: Token = doc[token.i + 1]
            has_next2: bool = len(doc) > token.i + 2
            next2_token: Optional[Token]
            if has_next2:
                next2_token = doc[token.i + 2]
            else:
                next2_token = None

            if self._boundary_punct_pattern.match(token.text) is not None:
                if next_token.text == self._mdash:
                    if has_next2 and next2_token.text[0].isupper():
                        next_token.is_sent_start = True
                elif next_token.text[0].islower() and not next_token.is_punct:
                    pass
                elif next_token.text not in self._quote_or_bracket:
                    next_token.is_sent_start = True
                elif (
                    next_token.text in self._quote_or_bracket
                    and has_next2
                    and next2_token.text[0].isupper()
                    and len(next_token.whitespace_) > 0
                ):
                    next2_token.is_sent_start = True
                elif len(token.whitespace_) > 0:
                    next_token.is_sent_start = True

        return doc
