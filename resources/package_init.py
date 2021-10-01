# coding: utf8
from __future__ import unicode_literals

import re

from spacy.language import Language


@Language.component("hun_sentencizer")
class HunSentencizer(object):
    def __init__(self):
        self._boundary_punct_pattern = re.compile(r"^((\.)|[\?!]+)$")
        self._quote_or_bracket = {'"', ")"}

    def __call__(self, doc):
        for token in doc[:-1]:
            if self._boundary_punct_pattern.match(token.text):
                next_token = doc[token.i + 1]
                if next_token.text not in self._quote_or_bracket:
                    next_token.is_sent_start = True
        return doc
