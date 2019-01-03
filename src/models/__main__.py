import glob
import importlib
import json
import logging
from io import StringIO
from os import path
from pprint import pprint

import click
import conllu
import pandas as pd
import spacy
from gensim.models.keyedvectors import KeyedVectors
from lemmy import Lemmatizer
from tqdm import tqdm

from src import conll17_ud_eval

logging.basicConfig(level=logging.INFO)

RESOURCES_ROOT = path.abspath(path.join(path.dirname(__file__), "..", "resources"))

TAG_MAP = {"CONJ": "CCONJ", "Y": "X", "VAN": "X"}


def parse_szk_morph(path):
    with open(path) as f:
        tok_id = 1
        sentence = []
        for line in f:
            line = line.strip()
            if len(line) == 0 or line.startswith("#"):
                yield "\n".join("\t".join(tok) for tok in sentence)
                sentence = []
                tok_id = 1
            else:
                parts = line.split("\t")
                sentence.append(
                    (
                        str(tok_id),
                        parts[0],
                        parts[1],
                        parts[2],
                        "_",
                        parts[3],
                        "0",
                        "_",
                        "_",
                        "_",
                    )
                )
                tok_id += 1
        if len(sentence):
            yield "\n".join("\t".join(tok) for tok in sentence)


def parse_szk_dep(path):
    with open(path) as f:
        sentence = []
        for line in f:
            line = line.strip()
            if len(line) == 0 or line.startswith("#"):
                yield "\n".join("\t".join(tok) for tok in sentence)
                sentence = []
            else:
                parts = line.split("\t")
                if parts[3] in {"ELL", "VAN"}:
                    continue
                sentence.append(
                    (
                        parts[0],
                        parts[1],
                        TAG_MAP.get(parts[3], parts[3]),
                        parts[4],
                        parts[5],
                        parts[7],
                        "0",  # parts[9],
                        "_",  # parts[11],
                        parts[13],
                        "_",
                    )
                )
        if len(sentence):
            yield "\n".join("\t".join(tok) for tok in sentence)


def sentence_repr(s):
    return "".join([t["form"] for t in s])


@click.group()
def cli():
    pass


@cli.command()
@click.argument("from_path")
@click.argument("to_path")
def convert_vectors_to_txt(from_path, to_path):
    model = KeyedVectors.load_word2vec_format(
        from_path, binary=True, unicode_errors="replace"
    )
    model.save_word2vec_format(to_path, binary=False)


@cli.command()
@click.argument("vectors_path")
def eval_vectors(vectors_path):
    model = KeyedVectors.load_word2vec_format(
        vectors_path, binary=not vectors_path.endswith(".txt"), unicode_errors="replace"
    )
    analogies_result = model.wv.evaluate_word_analogies(
        path.join(RESOURCES_ROOT, "questions-words-hu.txt"),
        dummy4unknown=True,
        restrict_vocab=None,
        case_insensitive=False,
    )
    pprint(analogies_result[0])


@cli.command()
@click.argument("model_path")
def test_model(model_path):
    nlp = spacy.load(model_path)
    doc = nlp("Ez egy ház.")
    print(nlp)
    print(doc, type(doc))
    pprint(
        [
            dict(
                text=t.text,
                lemma=t.lemma_,
                pos=t.pos_,
                tag=t.tag_,
                dep=t.dep_,
                head=t.head,
                is_stop=t.is_stop,
                has_vector=t.has_vector,
                brown_cluser=t.cluster,
                prob=t.prob,
            )
            for t in doc
        ]
    )


@cli.command()
@click.argument("from_glob")
@click.argument("to_path")
@click.argument("dev_path")
@click.argument("test_path")
@click.option("--morph/--dep", default=False)
def convert_szk_to_conllu(from_glob, to_path, dev_path, test_path, morph):
    ignored = []
    for fpath in [dev_path, test_path]:
        with open(fpath) as f:
            ignored.extend(map(sentence_repr, conllu.parse(f.read())))

    parser = parse_szk_morph if morph else parse_szk_dep

    ignored = set(ignored)
    parsed = []
    for fpath in glob.glob(from_glob):
        for sent in conllu.parse("\n\n".join(parser(fpath))):
            if sentence_repr(sent) not in ignored:
                parsed.append(sent)

    print(len(parsed))
    with open(to_path, "w") as outf:
        out = "".join(sent.serialize() for sent in parsed)
        outf.write(out)


def calculate_accuracy(lemmatizer, X, y):
    total = 0
    correct = 0
    ambiguous = 0

    for index in range(len(y)):
        word_class, full_form = X[index]
        target = y[index]
        predicted = lemmatizer.lemmatize(word_class, full_form)
        total += 1
        if len(predicted) > 1:
            #             print(word_class, full_form, predicted, target)
            ambiguous += 1
        elif predicted[0] == target:
            correct += 1
        # else:
        #     print(word_class, full_form, predicted, target)

    print("correct:", correct)
    print("ambiguous:", ambiguous)
    print("total:", total)
    print("accuracy:", correct / total)
    print("ambiguous%:", ambiguous / total)
    print("ambiguous + accuracy:", (ambiguous + correct) / total)


def read_lemmatization_data(path):
    with open(path) as f:
        df = pd.DataFrame(tok for sent in tqdm(conllu.parse(f.read())) for tok in sent)
        X = [
            (word_class, full_form)
            for _, (word_class, full_form) in df[["upostag", "form"]].iterrows()
        ]
        y = [lemma for _, (lemma,) in df[["lemma"]].iterrows()]
        return X, y


@cli.command()
@click.argument("train_path")
@click.argument("test_path")
@click.argument("model_path")
def train_lemmy(train_path, test_path, model_path):
    X_train, y_train = read_lemmatization_data(train_path)
    X_test, y_test = read_lemmatization_data(test_path)
    lemmatizer = Lemmatizer()
    lemmatizer.fit(X_train, y_train)
    calculate_accuracy(lemmatizer, X_test, y_test)
    with open(model_path, "w") as f:
        json.dump(lemmatizer.rules, f)


@cli.command()
@click.argument("model_path")
@click.argument("model_name")
@click.argument("test_data_path")
def benchmark_model(model_path, model_name, test_data_path):
    import sys
    sys.path.append((model_path))

    def sentences_to_conllu(doc, sent_id, prefix=""):
        res = []
        for sent in list(doc.sents):
            #         res.append("# sent_id = %s"%(prefix+str(sent_id)))
            #         res.append("# text = %s"%sent.sent)

            for i, word in enumerate(sent):
                if word.dep_.lower().strip() == "root":
                    head_idx = 0
                else:
                    head_idx = word.head.i - sent[0].i + 1

                linetuple = (
                    str(i + 1),  # ID
                    word.text,  # FORM
                    word.lemma_,  # LEMMA
                    word.pos_,  # UPOSTAG
                    "_",  # XPOSTAG
                    "_",  # FEATS
                    str(head_idx),  # HEAD
                    word.dep_,  # DEPREL
                    "_",  # DEPS
                    "_",  # MISC
                )
                res.append("\t".join(linetuple))

            sent_id += 1
            res.append("")
        return "\n".join(res) + "\n"

    with open(test_data_path) as f:
        data = conllu.parse(f.read())
        text = " ".join(d.metadata["text"] for d in data)

    load_model = getattr(importlib.import_module(model_name), "load")
    nlp = load_model()

    _parsed = StringIO(sentences_to_conllu(nlp(text), 1))
    parsed = conll17_ud_eval.load_conllu(_parsed)
    gold = conll17_ud_eval.load_conllu_file(test_data_path)

    results = pd.DataFrame(
        {k: v.__dict__ for k, v in conll17_ud_eval.evaluate(gold, parsed).items()}
    ).T

    print(results)


if __name__ == "__main__":
    cli()
