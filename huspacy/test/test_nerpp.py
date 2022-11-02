from typing import List, Tuple

import pytest
from spacy import Language
from spacy.lang.hu import Hungarian
from spacy.tokens import Doc, Span


@pytest.fixture(scope="module")
def nlp():
    # noinspection PyUnresolvedReferences
    from huspacy.components import nerpp

    nlp = Hungarian()
    nlp.add_pipe("nerpp")
    return nlp


@pytest.mark.parametrize(
    "tokens,entities",
    [("A Ford Focus egy alsó-középkategóriás családi autó".split(), [("Ford Focus", "CAR")])],
)
@pytest.mark.slow
def test_sentencizer(nlp: Language, tokens: List[str], entities: List[Tuple[str, str]]):
    doc: Doc = Doc(nlp.vocab, words=tokens)
    processed: Doc = nlp(doc)
    actual_ents: List[Span] = [ent for ent in processed.spans["ents"]]
    for act, expected in zip(actual_ents, entities):
        assert str(act) == expected[0]
        assert act.label_ == expected[1]
