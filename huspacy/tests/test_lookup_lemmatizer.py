import pytest
from spacy.lang.hu import Hungarian
from spacy.tokens import Doc

TRAINING_DATA = [
    [
        ("2-nek", "NUM", "Case=Dat|Number=Sing", "2"),
        ("A", "DET", "", "a"),
        ("kiflim", "NOUN", "Case=Nom|Number=Sing|Person=3|PronType=Int", "kifli"),
    ]
]


@pytest.fixture(scope="module")
def nlp():
    from huspacy.components.lookup_lemmatizer import LookupLemmatizer

    nlp = Hungarian()
    nlp.add_pipe("lookup_lemmatizer")

    # noinspection PyTypeChecker
    lookup_lemmatizer: LookupLemmatizer = nlp.pipeline[0][1]
    lookup_lemmatizer.train(TRAINING_DATA)

    return nlp


@pytest.mark.parametrize(
    "token,pos,morphs,expected_lemma",
    [
        ["A", "DET", "", "a"],
        ["kiflim", "NOUN", "Case=Nom|Number=Sing|Person=3|PronType=Int", "kifli"],
        ["2-nek", "NUM", "Case=Dat|Number=Sing", "2"],
        # Number masking works well
        ["5-nek", "NUM", "Case=Dat|Number=Sing", "5"],
        # Unknown tokens left untouched
        ["Az", "DET", "", ""],
    ],
)
def test_lookup_lemmatizer(nlp, token, pos, morphs, expected_lemma):
    doc: Doc = Doc(nlp.vocab, words=[token], pos=[pos], morphs=[morphs])
    processed: Doc = nlp(doc)
    assert processed[0].lemma_ == expected_lemma


@pytest.mark.skip(reason="Test needs a trained model")
def test_issue62():
    from huspacy.components.lookup_lemmatizer import LookupLemmatizer

    nlp = Hungarian()
    lookup_lemmatizer: LookupLemmatizer = nlp.add_pipe("lookup_lemmatizer")
    lookup_lemmatizer.from_disk(
        "/home/gorosz/workspace/huspacy/hu_core_news_md/models/hu_core_news_md-3.6.1/lookup_lemmatizer/")


    doc: Doc = Doc(nlp.vocab, words=["800¥600"], pos=["X"])
    processed: Doc = nlp(doc)
