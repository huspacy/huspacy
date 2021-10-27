import re
from pathlib import Path
from typing import Union

from lemmy import Lemmatizer
from spacy.language import Language
from spacy.tokens import Token
from spacy.tokens.doc import Doc


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


class HunLemmatizer:
    # noinspection PyUnusedLocal
    @staticmethod
    @Language.factory("hun_lemmy")
    def create(nlp: Language, name: str, model_path: Union[str, Path]) -> "HunLemmatizer":
        return HunLemmatizer(model_path)

    def __init__(self, model_path: Union[str, Path]):
        self._lemmy: Lemmatizer = Lemmatizer.from_disk(model_path)

    def __call__(self, doc: Doc) -> Doc:
        token: Token
        for token in doc:
            token.lemma_ = self._lemmy.lemmatize(token.tag_, token.text)
        return doc

    # noinspection PyUnusedLocal
    def to_disk(self, path, exclude=tuple()):
        self._lemmy.to_disk(path)

    # noinspection PyUnusedLocal
    def from_disk(self, path, exclude=tuple()):
        self._lemmy.from_disk(path)
