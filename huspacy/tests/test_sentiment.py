from typing import List

import pytest
from spacy import Language
from spacy.lang.hu import Hungarian
from spacy.tokens import Doc


@pytest.fixture(scope="module")
def nlp():
    # noinspection PyUnresolvedReferences
    import huspacy.integrations

    nlp = Hungarian()
    nlp.add_pipe("sentiment_lexicon")
    return nlp


@pytest.mark.parametrize("sentence,sentiment_values", [("Ez szuper jó!", [None, "POS", "POS", None])])
def test_sentiment_lexicons(nlp: Language, sentence: str, sentiment_values: List[int]):
    doc: Doc = nlp(sentence)
    actual: List = [tok._.sentiment for tok in doc]
    assert actual == sentiment_values

    senti_spans = doc.spans["sentiment"]
    assert len(senti_spans) == 2
    assert str(senti_spans[0]) == "szuper"
    assert str(senti_spans[1]) == "jó"
