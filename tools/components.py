import re
from pathlib import Path
from typing import Optional, Callable

from spacy.lang.hu import Hungarian
from spacy.language import Language
from spacy.pipeline.lemmatizer import lemmatizer_score
from spacy.tokens import Token
from spacy.tokens.doc import Doc
# noinspection PyUnresolvedReferences
from spacy.training.example import Example
from spacy.util import ensure_path

from lemmy import Lemmatizer


# noinspection PyUnusedLocal
@Hungarian.factory(
    "lemmatizer",
    assigns=["token.lemma"],
    requires=["token.pos"],
    default_config={
        "model_path": None,
        "scorer": {"@scorers": "spacy.lemmatizer_scorer.v1"},
    },
    # default_score_weights={"lemma_acc": 1.0},
)
def make_lemmatizer(nlp: Language, name: str, model_path: Path, scorer: Optional[Callable] ) -> "HunLemmatizer":
    # FIXME: this is a warkaround, `assemble` always passes the configured model_path,
    #  which becomes invalid when the model is assembled / packaged
    model = None
    if model_path.exists():
        model = Lemmatizer.from_disk(model_path)

    return HunLemmatizer(model, scorer)


class HunLemmatizer:

    def __init__(self, model: Lemmatizer, scorer: Optional[Callable] = lemmatizer_score):
        self._lemmy: Lemmatizer = model
        self.scorer = scorer

    def __call__(self, doc: Doc) -> Doc:
        token: Token
        for token in doc:
            token.lemma_ = self._lemmy.lemmatize(token.tag_, token.text, token.is_sent_start)
        return doc

    # noinspection PyUnusedLocal
    def to_disk(self, path, exclude=tuple()):
        path: Path = ensure_path(path)
        path.mkdir(exist_ok=True)
        self._lemmy.to_disk(path / "model")

    # noinspection PyUnusedLocal
    def from_disk(self, path, exclude=tuple()) -> "HunLemmatizer":
        path: Path = ensure_path(path)
        self._lemmy = Lemmatizer.from_disk(path / "model")
        return self


class HunSentencizer:
    # noinspection PyUnusedLocal
    @staticmethod
    @Language.factory("hun_sentencizer")
    def create(nlp: Language, name: str) -> "HunSentencizer":
        return HunSentencizer()

    def __init__(self):
        self._boundary_punct_pattern = re.compile(r"^([.\?!]+)$")
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
