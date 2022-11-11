import pytest
from spacy.lang.hu import Hungarian
from spacy.tokens import Doc


@pytest.fixture(scope="module")
def nlp():
    # noinspection PyUnresolvedReferences
    import huspacy.extra

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
def test_roman_to_arabic(nlp, token: str, expected_lemma: str):
    doc: Doc = Doc(nlp.vocab, words=[token])
    processed: Doc = nlp(doc)
    assert processed[0].lemma_ == expected_lemma
