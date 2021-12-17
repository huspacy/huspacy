"""
HunNPChunker basics.
"""

from more_itertools import windowed

import huspacy
#huspacy.download() # once at the beginning

from typing import Union, List, Optional
from spacy.language import Language
from spacy.tokens import Token
from spacy.tokens.doc import Doc

def print_doc(doc, add_attr: Union[List, None]=None, omit_attr: Union[List, None]=None):

    NOVALUE = '?'

    attrs = [
        "idx",
        "text",
        "whitespace_",
        "lemma_",
        "pos_",
        "morph",
        "dep_",
        "head.idx", # multilevel
        "ent_id",
        "ent_type_",
    ]

    if add_attr is not None:
        for a in add_attr:
            attrs.append(a)

    if omit_attr is not None:
        for a in omit_attr:
            if a in attrs:
                attrs.remove(a)

    # handles multilevel attribs :)
    def getattr_recursive(obj, attr, novalue):
        levels = attr.split('.')
        res = obj
        for level in levels:
            res = getattr(res, level, novalue)
        return res

    print('\t'.join(attrs))
    for tok in doc:
        print('\t'.join([
            str(getattr_recursive(tok, attr, NOVALUE))
            for attr in attrs
        ]))


# -----

class HunNPChunker:
    # noinspection PyUnusedLocal
    @staticmethod
    @Language.factory("hun_npchunker")
    def create(nlp: Language, name: str) -> "HunNPChunker":
        return HunNPChunker()

    def __init__(self):
        pass

    def __call__(self, doc: Doc) -> Doc:
        Token.set_extension("np", default='O') # XXX should I use some default attrib instead of custom 'np'?

        for left, center, right in windowed(doc, 3):
            if left.pos_ == 'DET' and center.pos_ == 'ADJ' and right.pos_ == 'NOUN':
                left._.np = 'B'
                center._.np = 'I'
                right._.np = 'I'

        return doc

# -----

TEXT = """Te Jancsi, de szépen süt Budapesten a nap! Az aranyos gyerek elolvas egy szép könyvet."""

nlp = huspacy.load() # ~ spacy.load("hu_core_news_lg")

# print(nlp.pipeline)

doc = nlp(TEXT)
print_doc(doc)
print()

np_chunker = HunNPChunker()

np_chunked_doc = np_chunker(doc)
print_doc(np_chunked_doc,
    add_attr=['_.np'],
    omit_attr=['morph', 'ent_id', 'ent_type_']
)

