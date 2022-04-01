import traceback
from pathlib import Path

import spacy
import typer
# noinspection PyUnresolvedReferences
import spacy_conll

app = typer.Typer()


@app.command()
def main(path: Path):
    try:
        nlp = spacy.load(path)
        nlp.add_pipe("conll_formatter")
        doc = nlp("Csiribiri csiribiri Zabszalma - Négy csillag közt alszom ma.")
        print(doc._.conll_str)
    except Exception:
        print(traceback.format_exc())

        exit(1)


if __name__ == '__main__':
    app()
