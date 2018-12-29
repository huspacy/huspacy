import glob
import json
import logging
from os import path
from pprint import pprint

import click
import conllu
import pandas as pd
import spacy
from gensim.models.keyedvectors import KeyedVectors
from lemmy import Lemmatizer
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)

RESOURCES_ROOT = path.abspath(path.join(path.dirname(__file__), "..", "resources"))

TAG_MAP = {
    "CONJ": "CCONJ",
    "Y": "X",
    "VAN": "X"
}


def parse_szk(path):
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
                sentence.append((
                    parts[0],
                    parts[1],
                    TAG_MAP.get(parts[3], parts[3]),
                    parts[4],
                    parts[5],
                    parts[7],
                    parts[9],
                    parts[11],
                    parts[13],
                    "_"
                ))
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
        case_insensitive=False
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
def convert_szk_to_conllu(from_glob, to_path, dev_path, test_path):
    ignored = []
    for fpath in [dev_path, test_path]:
        with open(fpath) as f:
            ignored.extend(map(sentence_repr, conllu.parse(f.read())))

    ignored = set(ignored)
    parsed = []
    for fpath in glob.glob(from_glob):
        for sent in conllu.parse("\n\n".join(parse_szk(fpath))):
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
        X = [(word_class, full_form) for _, (word_class, full_form) in df[["upostag", "form"]].iterrows()]
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


if __name__ == "__main__":
    cli()
