import re
from pathlib import Path
from typing import Tuple, List, Iterable

import conllu
import typer
from conllu import TokenList
from conllu.models import Token
from tqdm import tqdm

app = typer.Typer()

TaggedWords = List[Tuple[str, str]]
Lemmata = List[str]


def read_conllu_data(path: Path) -> Iterable[TokenList]:
    with path.open() as f:
        sentences: List[TokenList] = conllu.parse(f.read().strip())
        yield from sentences


@app.command()
def pattern(data_path: Path, column: str, pattern: str):
    tokens: List[Token]
    files = list(data_path.glob("**/*.conllup"))
    for fpath in tqdm(files):
        for tokens in read_conllu_data(fpath):
            for token in tokens:
                if re.findall(pattern, token[column]):
                    print(str(fpath) + ":", "\t".join([token["form"], token[column]]))


@app.command()
def pos_like(data_path: Path, column: str = "lemma"):
    pattern(data_path, column, pattern=r"\[[^\]]+\]")


@app.command()
def long_lemmata(data_path: Path):
    tokens: List[Token]
    files = list(data_path.glob("**/*.conllup"))
    for fpath in tqdm(files):
        for tokens in read_conllu_data(fpath):
            for token in tokens:
                form = token["form"]
                lemma = token["lemma"]
                if len(form) < len(lemma) and lemma[-2:] != "ik":
                    print(str(fpath) + ":", "\t".join([form, lemma]))


if __name__ == "__main__":
    app()
