from collections import defaultdict
from pathlib import Path

import typer

from tqdm import tqdm
from conllu import parse_incr

from spacy.lookups import Lookups, Table

app = typer.Typer()


@app.command()
def main(input_file: str, output_path: Path, min_occurrences: int = 1):
    token_lemma_occurrences = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    with open(input_file) as inp:
        for sentence in tqdm(list(parse_incr(inp))):
            for token in sentence:
                token_lemma_occurrences[token["upos"]][token["form"]]["lemma"] = token["lemma"]
                token_lemma_occurrences[token["upos"]][token["form"]]["occurrences"] += 1

    lookups = Lookups()

    for pos in token_lemma_occurrences:
        table = Table(name=f"lemma_lookups_{pos}")
        for token in token_lemma_occurrences[pos]:
            if token_lemma_occurrences[pos][token]["occurrences"] >= min_occurrences:
                table[token] = token_lemma_occurrences[pos][token]["lemma"]

        lookups.set_table(name=f"lemma_lookups_{pos}", table=table)

    lookups.to_disk(output_path)


if __name__ == "__main__":
    app()
