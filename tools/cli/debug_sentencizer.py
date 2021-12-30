import re
import sys
from difflib import unified_diff, context_diff, SequenceMatcher
from pathlib import Path

import typer
from spacy.lang.hu import Hungarian
from spacy.tokens import Doc

app = typer.Typer()

SENT_PATTERN = re.compile(r"# *text *= *")


@app.command()
def main(iob_file: Path):
    sentences = []
    with iob_file.open() as f:
        for line in f:
            match = SENT_PATTERN.match(line)
            if match is not None:
                sentence: str = line[match.end():].strip()
                sentences.append(sentence)

    nlp = Hungarian()

    # noinspection PyUnresolvedReferences
    from huspacy.components import HunSentencizer
    nlp.add_pipe("hun_sentencizer")

    doc: Doc = nlp(" ".join(sentences))
    predicted_sents = [str(s) + "\n" for s in doc.sents]
    sentences = [s + "\n" for s in sentences]

    seqmatcher = SequenceMatcher(None, sentences, predicted_sents)
    accuracy = sum(mb.size for mb in seqmatcher.get_matching_blocks()) / len(sentences)
    print(f"Accuracy: {accuracy:.2%}\n\n")

    diffs = list(context_diff(sentences, predicted_sents, fromfile="gold", tofile="predicted", n=0))
    sys.stdout.writelines(diffs)


if __name__ == "__main__":
    app()
