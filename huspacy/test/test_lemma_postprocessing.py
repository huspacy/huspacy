import pytest
from spacy import Language
from spacy.lang.hu import Hungarian
from spacy.tokens import Doc


@pytest.fixture(scope="module")
def nlp_lemma_smoother():
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
def test_lemma_smoother(nlp_lemma_smoother: Language, token: str, pos: str, lemma: str, expected_lemma: str):
    doc: Doc = Doc(nlp_lemma_smoother.vocab, words=[token], pos=[pos], lemmas=[lemma])
    processed: Doc = nlp_lemma_smoother(doc)
    assert processed[0].lemma_ == expected_lemma


@pytest.fixture(scope="module")
def nlp_roman_to_arabic():
    # noinspection PyUnresolvedReferences
    from huspacy.components import lemma_postprocessing

    nlp = Hungarian()
    nlp.add_pipe("roman_to_arabic")
    return nlp


@pytest.mark.parametrize(
    "token,expected_lemma",
    [
        ["I.", "1."],
        ["II.", "2."],
        ["III.", "3."],
        ["IV", "4"],
        ["DCCLVI", "756"],
        ["C-D.", "100-500."],
    ],
)
def test_roman_to_arabic(nlp_roman_to_arabic: Language, token: str, expected_lemma: str):
    doc: Doc = Doc(nlp_roman_to_arabic.vocab, words=[token], pos=["ADJ"])
    processed: Doc = nlp_roman_to_arabic(doc)
    assert processed[0].lemma_ == expected_lemma
