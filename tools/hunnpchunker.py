"""
Own naive NP chunker which creates IOB annotation in `_.np`.
"""

from more_itertools import windowed

from spacy.language import Language
from spacy.tokens import Token
from spacy.tokens.doc import Doc

class HunNPChunker:
    # noinspection PyUnusedLocal
    @staticmethod
    @Language.factory("hun_npchunker")
    def create(nlp: Language, name: str) -> "HunNPChunker":
        return HunNPChunker()

    def __init__(self):
        Token.set_extension("np", default='O') # XXX should I use some default attrib instead of custom 'np'?

    def __call__(self, doc: Doc) -> Doc:
        for left, center, right in windowed(doc, 3):
            if left.pos_ == 'DET' and center.pos_ == 'ADJ' and right.pos_ == 'NOUN':
                left._.np = 'B'
                center._.np = 'I'
                right._.np = 'I'

        return doc

