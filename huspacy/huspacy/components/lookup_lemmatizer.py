import re
from collections import defaultdict
from operator import itemgetter
from pathlib import Path
from re import Pattern
from typing import Optional, Callable, Iterable, Dict, Tuple

from spacy.lang.hu import Hungarian
from spacy.language import Language
from spacy.lookups import Lookups, Table
from spacy.pipeline import Pipe
from spacy.pipeline.lemmatizer import lemmatizer_score
from spacy.tokens import Token
from spacy.tokens.doc import Doc

# noinspection PyUnresolvedReferences
from spacy.training.example import Example
from spacy.util import ensure_path


class LookupLemmatizer(Pipe):
    """
    LookupLemmatizer learn `(token, pos, morph. feat) -> lemma` mappings during training, and applies them at prediction
    time.
    """

    _number_pattern: Pattern = re.compile(r"\d")

    # noinspection PyUnusedLocal
    @staticmethod
    @Hungarian.factory(
        "lookup_lemmatizer",
        assigns=["token.lemma"],
        requires=["token.pos"],
        default_config={"scorer": {"@scorers": "spacy.lemmatizer_scorer.v1"}, "source": ""},
    )
    def create(nlp: Language, name: str, scorer: Optional[Callable], source: str) -> "LookupLemmatizer":
        return LookupLemmatizer(None, source, scorer)

    def train(self, sentences: Iterable[Iterable[Tuple[str, str, str, str]]], min_occurrences: int = 1) -> None:
        """

        Args:
            sentences (Iterable[Iterable[Tuple[str, str, str, str]]]): Sentences to learn the mappings from
            min_occurrences (int): mapping occurring less than this threshold are not learned

        """

        # Lookup table which maps (upos, form) to (lemma -> frequency),
        # e.g. `{ ("NOUN", "alma"): { "alma" : 99, "alom": 1} }`
        lemma_lookup_table: Dict[Tuple[str, str], Dict[str, int]] = defaultdict(lambda: defaultdict(int))

        for sentence in sentences:
            for token, pos, feats, lemma in sentence:
                token = self.__mask_numbers(token)
                lemma = self.__mask_numbers(lemma)
                feats_str = ("|" + feats) if feats else ""
                key = (token, pos + feats_str)
                lemma_lookup_table[key][lemma] += 1
        lemma_lookup_table = dict(lemma_lookup_table)

        self._lookups = Lookups()
        table = Table(name="lemma_lookups")

        lemma_freq: Dict[str, int]
        for (form, pos), lemma_freq in dict(lemma_lookup_table).items():
            most_freq_lemma, freq = sorted(lemma_freq.items(), key=itemgetter(1), reverse=True)[0]
            if freq >= min_occurrences:
                if form not in table:
                    # lemma by pos
                    table[form]: Dict[str, str] = dict()
                table[form][pos] = most_freq_lemma

        self._lookups.set_table(name=f"lemma_lookups", table=table)

    def __init__(
        self,
        lookups: Optional[Lookups] = None,
        source: Optional[str] = None,
        scorer: Optional[Callable] = lemmatizer_score,
    ):
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

    def initialize(self, get_examples: Callable[[], Iterable[Example]], *, nlp: Language = None) -> None:
        lookups = Lookups()
        self._lookups = lookups.from_disk(path=self.source)

    @classmethod
    def __mask_numbers(cls, token: str) -> str:
        return cls._number_pattern.sub("0", token)

    @classmethod
    def __replace_numbers(cls, lemma: str, token: str) -> str:
        return cls._number_pattern.sub(lambda match: token[match.start()], lemma)
