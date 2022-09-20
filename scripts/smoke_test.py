import traceback
from pathlib import Path

import spacy
# noinspection PyUnresolvedReferences
import spacy_conll
import typer

# TODO: remove this workaround w/ lemmy
import sys
sys.path.append("../huspacy")
# noinspection PyUnresolvedReferences
import tools.custom_code

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
