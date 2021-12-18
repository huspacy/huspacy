"""
Pretty print spaCy doc.
"""

from typing import Union, List
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

