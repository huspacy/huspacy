import glob
import importlib
import itertools
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

import conll17_ud_eval
from model_builder.eval import lemmy_accuracy
from model_builder.io import (
    parse_szk_morph,
    parse_szk_dep,
    sentence_repr,
    read_conllu_data_for_lemmy,
    RESOURCES_ROOT,
    format_as_conllu,
)
from model_builder.ner import SpacyNerTrainer, DataIterator

logging.basicConfig(level=logging.INFO)


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
        vectors_path, binary=False, unicode_errors="replace"
    )
    analogies_result = model.wv.evaluate_word_analogies(
        path.join(RESOURCES_ROOT, "questions-words-hu.txt"),
        dummy4unknown=True,
        restrict_vocab=None,
        case_insensitive=False,
    )
    pprint(analogies_result[0])


@cli.command()
@click.argument("model_name")
def smoke_test(model_name):
    nlp = spacy.load(model_name)
    doc = nlp(
        "Csiribiri csiribiri zabszalma - négy csillag közt alszom ma. "
        "Csiribiri csiribiri bojtorján lélek lép a lajtorján."
    )
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

    logging.info("Read {} sentences".format(len(parsed)))
    with open(to_path, "w") as outf:
        out = "".join(sent.serialize() for sent in parsed)
        outf.write(out)


@cli.command()
@click.argument("train_path")
@click.argument("test_path")
@click.argument("model_path")
def train_lemmy(train_path, test_path, model_path):
    X_train, y_train = read_conllu_data_for_lemmy(train_path)
    X_test, y_test = read_conllu_data_for_lemmy(test_path)
    lemmatizer = Lemmatizer()
    lemmatizer.fit(X_train, y_train)
    lemmy_accuracy(lemmatizer, X_test, y_test)
    with open(model_path, "w") as f:
        json.dump(lemmatizer.rules, f)


@cli.command()
@click.argument("model_name")
@click.argument("test_data_path")
def benchmark_model(model_name, test_data_path):
    with open(test_data_path) as f:
        data = conllu.parse(f.read())
        text = " ".join(d.metadata["text"] for d in data)

    load_model = getattr(importlib.import_module(model_name), "load")
    nlp = load_model()

    _parsed = StringIO(format_as_conllu(nlp(text), 1))
    parsed = conll17_ud_eval.load_conllu(_parsed)
    gold = conll17_ud_eval.load_conllu_file(test_data_path)

    results = pd.DataFrame(
        {k: v.__dict__ for k, v in conll17_ud_eval.evaluate(gold, parsed).items()}
    ).T

    print(results)


@cli.command()
@click.argument("model_name")
@click.argument("output_path")
@click.argument("train_data")
@click.argument("test_data")
@click.argument("n_iter")
def train_ner(model_name, output_path, train_data, test_data, n_iter):
    if model_name in ["None", "False", "", "blank"]:
        model_name = None

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logging.info("Reading train data")
    diterator = DataIterator()
    train_sentences = list(tqdm(itertools.islice(diterator.tagged_sentences(train_data), None)))
    logging.info("Got {} sentences with at least one entity".format(len(train_sentences)))

    logging.info("Reading test data")
    test_sentences = list(tqdm(diterator.tagged_sentences(test_data)))
    logging.info("Got {} sentences with at least one entity".format(len(test_sentences)))

    trainer = SpacyNerTrainer(model_name, output_path)
    trainer(train_sentences, test_sentences, int(n_iter))
    trainer.store_model()


if __name__ == "__main__":
    cli()
