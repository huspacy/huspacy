from pathlib import Path
from typing import Iterator

import typer
from conllu import parse_incr, TokenList
from conllu.parser import parse_nullable_value
from tqdm import tqdm

from huspacy.components.lookup_lemmatizer import LookupLemmatizer

app = typer.Typer()


@app.command()
def main(input_file: str, output_path: Path, min_occurrences: int = 1):
    with open(input_file) as inp:
        parse_it: Iterator[TokenList] = parse_incr(
            inp, field_parsers={"feats": lambda line, i: parse_nullable_value(line[i])}
        )
        training_data = (
            ((token["form"], token["upos"], token["feats"], token["lemma"]) for token in sentence)
            for sentence in tqdm(parse_it, desc="Computing lemmata frequencies")
        )

        lookup_lemmatizer = LookupLemmatizer()
        lookup_lemmatizer.train(training_data, min_occurrences)
        lookup_lemmatizer.to_disk(output_path)


if __name__ == "__main__":
    app()
