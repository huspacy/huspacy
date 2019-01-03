# coding: utf8
from __future__ import unicode_literals

import json
import re
from pathlib import Path

from lemmy import Lemmatizer
from spacy.util import load_model_from_init_py, get_model_meta

__version__ = get_model_meta(Path(__file__).parent)["version"]


class HunLemmatizer(object):
    def __init__(self, rules_path):
        self._lemmatizer = Lemmatizer(rules=json.load(open(rules_path)))

    def lemmatize(self, tok, with_lower=False):
        predicted = self._lemmatizer.lemmatize(tok.pos_, tok.text)
        if with_lower:
            predicted += list(map(str.lower, predicted))
        if len(predicted) == 0:
            return tok.text
        elif len(predicted) == 1:
            return predicted[0]
        elif len(predicted) > 1:
            best_lemma = predicted[0]
            max_prob = tok.vocab[predicted[0]].prob
            for lemma in predicted[1:]:
                act_prob = tok.vocab[lemma].prob
                if act_prob > max_prob:
                    max_prob = act_prob
                    best_lemma = lemma
            return best_lemma

    def __call__(self, doc):
        for token in doc:
            if token.is_sent_start:
                token.lemma_ = self.lemmatize(token, with_lower=True)
            else:
                token.lemma_ = self.lemmatize(token)

        return doc

    def add_hook(self, nlp):
        nlp.add_pipe(self, after="tagger", name="lemmatizer")


class HunSentencizer(object):
    def __init__(self):
        self.boundary_punct_pattern = re.compile("^((\.)|[\?!]+)$")

    def __call__(self, doc):
        for token in doc[:-1]:
            if self.boundary_punct_pattern.match(token.text):
                doc[token.i + 1].is_sent_start = True
        return doc

    def add_hook(self, nlp):
        nlp.add_pipe(self, first=True, name="sentencizer")


def load(**overrides):
    nlp = load_model_from_init_py(__file__, **overrides)

    init_path = Path(__file__)
    model_path = init_path.parent
    meta = get_model_meta(model_path)
    data_dir = "%s_%s-%s" % (meta["lang"], meta["name"], meta["version"])
    data_path = model_path / data_dir
    lemmatizer = HunLemmatizer(data_path / "lemmy" / "rules.json")
    lemmatizer.add_hook(nlp)

    sentencizer = HunSentencizer()
    sentencizer.add_hook(nlp)
    return nlp
