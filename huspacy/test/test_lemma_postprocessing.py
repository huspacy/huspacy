import pytest
import pytest
from spacy import Language
from spacy.lang.hu import Hungarian
from spacy.tokens import Doc


@pytest.fixture(scope="module")
def nlp():
    # noinspection PyUnresolvedReferences
    from tools.components import lemma_postprocessing

    nlp = Hungarian()
    nlp.add_pipe("lemma_smoother")
    return nlp


@pytest.mark.parametrize(
    "token,pos,lemma,expected_lemma",
    [
        ["Magyarország!-gal", "NOUN", "Magyarország!", "Magyarország"],
        ["Magyarország?-gal", "NOUN", "Magyarország?", "Magyarország"],
        ["2-án", "NOUN", "2-án", "2"],
        ["2-től", "NOUN", "2-től", "2"],
        # FIXME: is this a realistic test case?!
        ["110_km/h-ra", "NUM", "110_km/h-ra", "110_km/h"],
        ["35,50%", "NUM", "35,50%", "35,50%"],
    ],
)
def test_lemma_smoother(nlp: Language, token: str, pos: str, lemma: str, expected_lemma: str):
    doc: Doc = Doc(nlp.vocab, words=[token], pos=[pos], lemmas=[lemma])
    processed: Doc = nlp(doc)
    assert processed[0].lemma_ == expected_lemma
