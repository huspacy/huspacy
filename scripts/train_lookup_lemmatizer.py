from collections import defaultdict
from operator import itemgetter
from pathlib import Path
from typing import Tuple, Dict, Iterator

import typer
from conllu import parse_incr, TokenList
from conllu.models import Token
from conllu.parser import parse_nullable_value
from spacy.lookups import Lookups, Table
from tqdm import tqdm

app = typer.Typer()


@app.command()
def main(input_file: str, output_path: Path, min_occurrences: int = 1):
    # Lookup table which maps (upos, form) to (lemma -> frequency),
    # e.g. `{ ("NOUN", "alma"): { "alma" : 99, "alom": 1} }`
    lemma_lookup_table: Dict[Tuple[str, str], Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    with open(input_file) as inp:
        parse_it: Iterator[TokenList] = parse_incr(
            inp,
            field_parsers={"feats": lambda line, i: parse_nullable_value(line[i])}
        )
        for sentence in tqdm(parse_it, desc="Computing lemmata frequencies"):
            token: Token
            for token in sentence:
                feats_str = ("|" + token["feats"]) if token["feats"] else ""
                key = (token["form"], token["upos"] + feats_str)
                lemma_lookup_table[key][token["lemma"]] += 1
    lemma_lookup_table = dict(lemma_lookup_table)

    lookups = Lookups()
    table = Table(name="lemma_lookups")

    lemma_freq: Dict[str, int]
    for (form, pos), lemma_freq in dict(lemma_lookup_table).items():
        most_freq_lemma, freq = sorted(lemma_freq.items(), key=itemgetter(1), reverse=True)[0]
        if freq >= min_occurrences:
            if form not in table:
                # lemma by pos
                table[form]: Dict[str, str] = dict()
            table[form][pos] = most_freq_lemma

    lookups.set_table(name=f"lemma_lookups", table=table)
    lookups.to_disk(output_path)


if __name__ == "__main__":
    app()
