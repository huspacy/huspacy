import json
from collections import defaultdict, Counter
from pathlib import Path
from typing import Tuple, List, Dict

import conllu
import pandas as pd
import typer
from conllu import TokenList
from lemmy import Lemmatizer
from tqdm import tqdm

app = typer.Typer()

TaggedWords = List[Tuple[str, str]]
Lemmata = List[str]


def read_conllu_data_for_lemmy(path: Path) -> Tuple[TaggedWords, Lemmata]:
    with path.open() as f:
        sentences: List[TokenList] = conllu.parse(f.read().strip())
        df = pd.DataFrame(tok for sent in tqdm(sentences, desc=str(path.name), total=len(sentences)) for tok in sent)
        X = [
            (word_class, full_form)
            for _, (word_class, full_form) in df[["upos", "form"]].iterrows()
        ]
        y = [lemma for _, (lemma,) in df[["lemma"]].iterrows()]
        return X, y


def evaluate(lemmatizer: Lemmatizer, X: TaggedWords, y: Lemmata):
    total = 0
    correct = 0
    ambiguous = 0

    ambiguous_words: List = []
    for index, target in enumerate(y):
        word_class, full_form = X[index]
        predicted = lemmatizer.lemmatize(word_class, full_form)
        total += 1
        if len(predicted) > 1:
            ambiguous_words.append((full_form, word_class, predicted))
            ambiguous += 1
        elif predicted[0] == target:
            correct += 1

    print("correct:", correct)
    print("ambiguous:", ambiguous)
    print("total:", total)
    print("accuracy:", correct / total)
    print("ambiguous%:", ambiguous / total)
    print("ambiguous + accuracy:", (ambiguous + correct) / total)

    for k,v in Counter(ambiguous_words).most_common(50):
        print(k,v)

@app.command()
def main(train_path: Path, test_path: Path, model_path: Path):
    model_path.parent.mkdir(parents=True, exist_ok=True)

    X_train, y_train = read_conllu_data_for_lemmy(train_path)
    X_test, y_test = read_conllu_data_for_lemmy(test_path)
    lemmatizer = Lemmatizer()
    lemmatizer.fit(X_train, y_train)
    evaluate(lemmatizer, X_test, y_test)
    with open(model_path, "w") as f:
        json.dump(lemmatizer.rules, f)


if __name__ == "__main__":
    app()
