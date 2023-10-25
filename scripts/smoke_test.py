import traceback
import random

import spacy

# noinspection PyUnresolvedReferences
import spacy_conll
import typer

app = typer.Typer()

try:
    import huspacy.components
except ImportError as e:
    print("Could not load the components")


def get_random_text(nlp, length: int) -> str:
    words = [lexeme.text for lexeme in nlp.vocab]
    random.seed(42)
    chosen_words = random.choices(words, k=length)
    return " ".join(chosen_words)


@app.command()
def main(path: str, with_random_text: bool = False):
    try:
        nlp = spacy.load(path)
        nlp.add_pipe("conll_formatter")
        doc = nlp("Csiribiri csiribiri Zabszalma - Négy csillag közt alszom ma.")
        print(doc._.conll_str)
        if with_random_text is not None:
            doc = nlp(get_random_text(nlp, 1024))
            print("CONLL format length:", len(doc._.conll_str))
    except Exception:
        print(traceback.format_exc())
        exit(1)


if __name__ == "__main__":
    app()
