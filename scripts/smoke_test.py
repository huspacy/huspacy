import traceback

import spacy

# noinspection PyUnresolvedReferences
import spacy_conll
import typer

app = typer.Typer()

import huspacy.components


@app.command()
def main(path: str):
    try:
        nlp = spacy.load(path)
        nlp.add_pipe("conll_formatter")
        doc = nlp("Csiribiri csiribiri Zabszalma - Négy csillag közt alszom ma.")
        print(doc._.conll_str)
    except Exception:
        print(traceback.format_exc())
        exit(1)


if __name__ == "__main__":
    app()
