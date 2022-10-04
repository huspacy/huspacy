from typing import List

import pytest
from spacy import Language
from spacy.lang.hu import Hungarian
from spacy.tokens import Doc

import sys


@pytest.fixture(scope="module")
def nlp():
    # noinspection PyUnresolvedReferences
    from tools.components import lemma_postprocessing

    nlp = Hungarian()
    nlp.add_pipe("lemma_smoother")
    return nlp


@pytest.mark.parametrize("tokens_lemmas", [
    # token, pos, lemma, expected lemma
    ["Magyarország!-gal", "NOUN", "Magyarország!", "Magyarország"],
    ["Magyarország?-gal", "NOUN", "Magyarország?", "Magyarország"],
    ["2-án", "NOUN", "2-án", "2"],
    ["2-től", "NOUN", "2-től", "2"],
    ["110_km/h-ra", "NUM", "110_km/h-ra", "110_km/h"],
    ["35,50%", "NUM", "35,50%", "35,50%"],
])
def test_sentencizer(nlp: Language, tokens_lemmas: List[str]):
    doc: Doc = Doc(nlp.vocab, words=[tokens_lemmas[0]], pos=[tokens_lemmas[1]], lemmas=[tokens_lemmas[2]])
    actual: str = doc[0].lemma_
    assert tokens_lemmas[3] == actual
