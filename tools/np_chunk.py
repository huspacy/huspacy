"""
Do Hungarian NP chunking using various approaches.
"""

import huspacy
#huspacy.download() # once at the beginning

from hunnpchunker import HunNPChunker
from hu_noun_chunks import noun_chunks
from print_doc import print_doc

import sys

# -----

def main():
    """Main."""

    nlp = huspacy.load() # ~ spacy.load("hu_core_news_lg")

    np_chunker = HunNPChunker()

    for line in sys.stdin:
        doc = nlp(line.rstrip())

        # using own naive NP chunker which creates IOB annotation in `_.np`
        np_chunked_doc = np_chunker(doc)

        print_doc(doc,
            add_attr=['_.np'],
            omit_attr=['ent_id', 'ent_type_']
        )
        print()

        # using spacy's noun_chunk syntax iterator
        #
        # add noun_chunks syntax iterator based on
        # https://github.com/explosion/spaCy/blob/master/spacy/tests/pipeline/test_pipe_methods.py
        doc.noun_chunks_iterator = noun_chunks
        # iterate chunks
        for chunk in doc.noun_chunks:
            print(f' --> {chunk}')
        print()


if __name__ == '__main__':
    main()

