import glob
import pathlib
from pathlib import Path

import typer

from tqdm import tqdm
from conllu import parse_sentences, parse
import random

from typing import List, Tuple

app = typer.Typer()


@app.command()
def main(input_file_pattern: str, ud_hungarian_szeged_pattern: str, output_path: Path, random_seed: int = 42,
         train: float = 0.8, dev_test: float = 0.5):
    sentences = list()
    ud_hungarian_szeged_sentences = list()

    for input_file in tqdm(glob.glob(input_file_pattern), desc="Reading files"):
        with open(input_file) as inp:
            for sentence in parse_sentences(inp):
                sentences.append(sentence)

    for input_file in tqdm(glob.glob(ud_hungarian_szeged_pattern), desc="Reading UD files"):
        with open(input_file) as inp:
            for sentence in parse_sentences(inp):
                ud_hungarian_szeged_sentences.append(process_sentence(sentence))

    sentences = [x for x in tqdm(sentences, desc="Removing occurrings")
                 if process_sentence(x) not in ud_hungarian_szeged_sentences]

    random.seed(random_seed)
    random.shuffle(sentences)

    train_sentences = sentences[:int((len(sentences) + 1) * train)]
    not_train_sentences = sentences[int((len(sentences) + 1) * train):]

    dev_sentences = not_train_sentences[:int((len(not_train_sentences) + 1) * dev_test)]
    test_sentences = not_train_sentences[int((len(not_train_sentences) + 1) * dev_test):]

    with open(pathlib.Path(output_path, "train.conllu"), "w+") as out:
        for sentence in tqdm(train_sentences, desc="Writing train.conllu"):
            print(sentence, file=out, end='\n\n')

    with open(pathlib.Path(output_path, "dev.conllu"), "w+") as out:
        for sentence in tqdm(dev_sentences, desc="Writing dev.conllu"):
            print(sentence, file=out, end='\n\n')

    with open(pathlib.Path(output_path, "test.conllu"), "w+") as out:
        for sentence in tqdm(test_sentences, desc="Writing test.conllu"):
            print(sentence, file=out, end='\n\n')


def process_sentence(sentence: str) -> List[Tuple[int, str, str]]:
    parsed = parse(sentence)[0]
    lines = list()

    for i in parsed:
        lines.append((i["id"], i["form"], i["lemma"]))

    return lines


if __name__ == "__main__":
    app()
