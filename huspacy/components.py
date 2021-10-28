import re

from spacy.language import Language
from spacy.tokens import Token
from spacy.tokens.doc import Doc

# noinspection PyUnresolvedReferences
import lemmy


class HunSentencizer:
    # noinspection PyUnusedLocal
    @staticmethod
    @Language.factory("hun_sentencizer")
    def create(nlp: Language, name: str) -> "HunSentencizer":
        return HunSentencizer()

    def __init__(self):
        self._boundary_punct_pattern = re.compile(r"^((\.)|[\?!]+)$")
        self._quote_or_bracket = {'"', ")"}

    def __call__(self, doc: Doc) -> Doc:
        doc[0].is_sent_start = True

        for token in doc[:-1]:
            if self._boundary_punct_pattern.match(token.text):
                next_token: Token = doc[token.i + 1]
                if next_token.text[0].islower():
                    pass
                elif next_token.text not in self._quote_or_bracket:
                    next_token.is_sent_start = True
                elif len(token.whitespace_) > 0:
                    next_token.is_sent_start = True
        return doc
