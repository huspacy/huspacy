"""
Analyse corpus by Hungarian spacy.
"""

import sys

import huspacy
#huspacy.download() # once at the beginning

from print_doc import print_doc


def main():
    """Main."""

    nlp = huspacy.load() # ~ spacy.load("hu_core_news_lg")

    for line in sys.stdin:
        analysed = nlp(line.rstrip())
        print_doc(analysed)
        print()


if __name__ == '__main__':
    main()

