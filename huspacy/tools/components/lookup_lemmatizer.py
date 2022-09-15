from pathlib import Path
from re import Pattern
import re
from typing import Optional, Callable, Iterable, Dict

from spacy.lang.hu import Hungarian
from spacy.language import Language
from spacy.pipeline import Pipe
from spacy.pipeline.lemmatizer import lemmatizer_score
from spacy.tokens import Token
from spacy.tokens.doc import Doc
# noinspection PyUnresolvedReferences
from spacy.training.example import Example
from spacy.util import ensure_path
from spacy.lookups import Lookups


class LookupLemmatizer(Pipe):
    _number_pattern: Pattern = re.compile(r"\d")

    # noinspection PyUnusedLocal
    @staticmethod
    @Hungarian.factory(
        "lookup_lemmatizer",
        assigns=["token.lemma"],
        requires=["token.pos"],
        default_config={
            "scorer": {"@scorers": "spacy.lemmatizer_scorer.v1"},
            "source": ""
        },
    )
    def create(nlp: Language, name: str, scorer: Optional[Callable], source: str) -> "LookupLemmatizer":
        return LookupLemmatizer(None, source, scorer)

    def __init__(self, lookups: Optional[Lookups], source: str, scorer: Optional[Callable] = lemmatizer_score):
        self._lookups: Optional[Lookups] = lookups
        self.scorer = scorer
        self.source = source

    def __call__(self, doc: Doc) -> Doc:
        assert self._lookups is not None, "Lookup table should be initialized first"

        token: Token
        for token in doc:
            lemma_lookup_table = self._lookups.get_table(f"lemma_lookups")
            masked_token = self.__mask_numbers(token.text)

            if masked_token in lemma_lookup_table:
                lemma_by_pos: Dict[str, str] = lemma_lookup_table[masked_token]
                feats_str = ("|" + str(token.morph)) if str(token.morph) else ""
                key = token.pos_ + feats_str
                if key in lemma_by_pos:
                    if masked_token != token.text:
                        # If the token contains numbers, we need to replace the numbers in the lemma as well
                        token.lemma_ = self.__replace_numbers(lemma_by_pos[key], token.text)
                        pass
                    else:
                        token.lemma_ = lemma_by_pos[key]
        return doc

    # noinspection PyUnusedLocal
    def to_disk(self, path, exclude=tuple()):
        assert self._lookups is not None, "Lookup table should be initialized first"

        path: Path = ensure_path(path)
        path.mkdir(exist_ok=True)
        self._lookups.to_disk(path)

    # noinspection PyUnusedLocal
    def from_disk(self, path, exclude=tuple()) -> "LookupLemmatizer":
        path: Path = ensure_path(path)
        lookups = Lookups()
        self._lookups = lookups.from_disk(path=path)
        return self

    def initialize(
            self,
            get_examples: Callable[[], Iterable[Example]],
            *,
            nlp: Language = None
    ) -> None:
        lookups = Lookups()
        self._lookups = lookups.from_disk(path=self.source)

    @classmethod
    def __mask_numbers(cls, token: str) -> str:
        return cls._number_pattern.sub("0", token)

    @classmethod
    def __replace_numbers(cls, lemma: str, token: str) -> str:
        return cls._number_pattern.sub(lambda match: token[match.start()], lemma)
