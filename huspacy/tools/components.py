import re
from pathlib import Path
from typing import Optional, Callable, Iterable, Dict

from spacy.lang.hu import Hungarian
from spacy.language import Language
from spacy.lookups import Lookups
from spacy.pipeline import Pipe
from spacy.pipeline.lemmatizer import lemmatizer_score
from spacy.tokens import Token
from spacy.tokens.doc import Doc
from spacy.training import Example
from spacy.util import ensure_path


class LookupLemmatizer(Pipe):
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
            if token.text in lemma_lookup_table:
                lemma_by_pos: Dict[str, str] = lemma_lookup_table[token.text]
                feats_str = ("|" + str(token.morph)) if str(token.morph) else ""
                key = token.pos_ + feats_str
                if key in lemma_by_pos:
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


@Hungarian.component("lemma_smoother", assigns=["token.lemma"], requires=["token.lemma"])
def smooth_lemma(doc):
    for token in doc:
        if token.is_sent_start and token.tag_ != 'PROPN':
            token.lemma_ = token.lemma_.lower()

    return doc


# TODO: move to separate files
class HunSentencizer(Pipe):
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
                elif next_token.text in self._quote_or_bracket \
                        and has_next2 and next2_token.text[0].isupper() and len(next_token.whitespace_) > 0:
                    next2_token.is_sent_start = True
                elif len(token.whitespace_) > 0:
                    next_token.is_sent_start = True

        return doc
