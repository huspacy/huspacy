import pytest
from spacy.lang.hu import Hungarian
from spacy.tokens import Doc


@pytest.fixture(scope="module")
def nlp():
    # noinspection PyUnresolvedReferences
    from huspacy.components import lemma_postprocessing

    nlp = Hungarian()
    nlp.add_pipe("lemma_smoother")
    return nlp


@pytest.mark.parametrize(
    "token,pos,lemma,expected_lemma",
    [
        ["Magyarország!-gal", "NOUN", "Magyarország!", "Magyarország"],
        ["Magyarország?-gal", "NOUN", "Magyarország?", "Magyarország"],
        ["2-án", "NOUN", "2-án", "2."],
        ["2-től", "NUM", "2-től", "2"],
        ["35,50%", "NUM", "35,50%", "35,50%"],
    ],
)
def test_lemma_smoother(nlp, token: str, pos: str, lemma: str, expected_lemma: str):
    doc: Doc = Doc(nlp.vocab, words=[token], pos=[pos], lemmas=[lemma])
    processed: Doc = nlp(doc)
    assert processed[0].lemma_ == expected_lemma
