"""
Sandbox.
"""

from more_itertools import windowed

import huspacy
#huspacy.download() # once at the beginning

from typing import Union, List, Optional
from spacy.language import Language
from spacy.tokens import Token
from spacy.tokens.doc import Doc

from print_doc import print_doc

# -----

TEXT = """Te Jancsi, de szépen süt Budapesten a nap! Az aranyos gyerek elolvas egy szép könyvet."""

nlp = huspacy.load() # ~ spacy.load("hu_core_news_lg")

# print(nlp.pipeline)

doc = nlp(TEXT)
print_doc(doc)
print()

# XXX NotImplemented
#for chunk in doc.noun_chunks:
#    print(chunk.text, chunk.root.text, chunk.root.dep_,
#            chunk.root.head.text)

print('*** dep')
for tok in doc:
    print(f'{tok.text} -{tok.dep_}-> {tok.head.text} {tok.head.pos_} {[child for child in tok.children]}')

print('*** verb + subject')
from spacy.symbols import nsubj, VERB
verbs = set()
for possible_subject in doc:
    if possible_subject.dep == nsubj and possible_subject.head.pos == VERB:
        verbs.add(possible_subject.head)
print(verbs)

print('*** subtree')
root = [tok for tok in doc if tok.head == tok][0]
subject = list(root.rights)[0]
for descendant in subject.subtree:
    assert subject is descendant or subject.is_ancestor(descendant)
    print(descendant.text, descendant.dep_, descendant.n_lefts,
            descendant.n_rights,
            [ancestor.text for ancestor in descendant.ancestors])

print('*** edges + merge')
span = doc[doc[12].left_edge.i : doc[12].right_edge.i+1]
with doc.retokenize() as retokenizer:
    retokenizer.merge(span)
for tok in doc:
    print(tok.text, '||', tok.pos_, tok.dep_, tok.head.text)

