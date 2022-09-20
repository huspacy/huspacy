from typing import List

import pytest
from spacy import Language
from spacy.lang.hu import Hungarian
from spacy.tokens import Doc

import sys


@pytest.fixture(scope="module")
def nlp():
    # noinspection PyUnresolvedReferences
    from tools.components import hun_sentencizer
    nlp = Hungarian()
    nlp.add_pipe("hun_sentencizer")
    return nlp


@pytest.mark.parametrize("sentences", [
    ["Szia!", "Hogy vagy?"],
    ["Mizujs?", "Hogy vagy?"],
    ["Szia.", "Hogy vagy?"],
    ["\"Szia!\" - mondta.", "Hogy vagy?"],
    ["Szia!", "\"Hogy vagy?\""],
    ["(Szia!) - mondta.", "Hogy vagy?"],
    ["Szinte hihetetlen sebességgel robog az idő.", "A nemrég"],
    ["Szia!", "Jó estét, Magyarország! című műsor."],
    ["A most megjelent Sport '99 évkönyv címlapjának legnagyobb képén ön feszít ...", "— Hát ez egy külön sztori!"],
    # ["Vajon önmagában sikernek tekinthető -e? — tette fel a kérdést a napokban a térség befolyásos gazdasági"],
    ["Minden eszközzel megpróbálnak lejáratni. \"", "Helmeczy szerint ez az oka annak"],
    ["a közoktatásban dolgozók keresetének felzárkóztatása.", "\"Nem csináltam semmit"],
    ["A jövőben szigorúan betartják a termelési kvótákat.)", "Egyes hazai szakértők szerint"]
])
def test_sentencizer(nlp: Language, sentences: List[str]):
    doc: Doc = nlp(" ".join(sentences))
    actual: List[str] = [str(sent).strip() for sent in doc.sents]
    assert sentences == actual
