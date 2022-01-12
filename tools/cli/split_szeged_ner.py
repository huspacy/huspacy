import itertools
import logging
from typing import Tuple, List, Iterable, Union

import spacy
import typer
from sklearn.model_selection import train_test_split
from spacy.tokens import Doc
from spacy.training import iob_to_biluo
from spacy.training.iob_utils import offsets_from_biluo_tags
from tqdm import tqdm

app = typer.Typer()

SentenceWithTags = Tuple[List[str], List[str]]
TaggedSentence = Tuple[str, List[Tuple[int, int, str]]]


def sentence_to_str(sent: SentenceWithTags) -> str:
    return "\n".join(["{}\t{}".format(tok, tag) for tok, tag in zip(*sent)])


class WhitespaceTokenizer(object):
    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self, text):
        words = text.split()

        spaces = [True] * len(words)
        return Doc(self.vocab, words=words, spaces=spaces)


class DataIterator:
    def __init__(self):
        self.nlp = spacy.blank("hu")
        self.nlp.tokenizer = WhitespaceTokenizer(self.nlp.vocab)

    def _sentence_to_spacy_annotations(self, tokens, tags) -> TaggedSentence:
        sentence = " ".join(tokens)
        tags = iob_to_biluo(tags)

        doc = self.nlp(sentence)
        annotations: List[Tuple[int, int, Union[str, int]]] = offsets_from_biluo_tags(doc, tags)
        annotations = [
            (begin, end, tag) for begin, end, tag in annotations if len(tag) > 0
        ]

        return sentence, annotations

    def sentences_with_tags(self, path: str) -> Iterable[SentenceWithTags]:
        with open(path) as f:
            toks, tags = [], []
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    tok = parts[0].strip()
                    tag = parts[-1]
                    if tag == 0:
                        tag = "O"
                    if len(tok) > 0 and tok != "-DOCSTART-":
                        toks.append(tok)
                        tags.append(tag)
                else:
                    yield toks, tags
                    toks, tags = [], []

            if len(toks) > 0:
                yield toks, tags


@app.command()
def split_ner_data(szegedner_data, train_data, dev_data, test_data):
    diterator = DataIterator()
    logging.info("Reading gold data")
    gold_sents = list(tqdm(itertools.islice(diterator.sentences_with_tags(szegedner_data), None)))
    train_sents, all_test_sents = train_test_split(gold_sents, test_size=.2, random_state=42)
    dev_sents, test_sents = train_test_split(all_test_sents, test_size=.5, random_state=42)

    logging.info("Storing training data")
    with open(train_data, "w") as f:
        for i, s in tqdm(enumerate(train_sents)):
            f.write(sentence_to_str(s))
            f.write("\n")
            f.write("\n")

    logging.info("Storing test data")
    with open(dev_data, "w") as f:
        for i, s in tqdm(enumerate(dev_sents)):
            f.write(sentence_to_str(s))
            f.write("\n")
            f.write("\n")

    logging.info("Storing test data")
    with open(test_data, "w") as f:
        for i, s in tqdm(enumerate(test_sents)):
            f.write(sentence_to_str(s))
            f.write("\n")
            f.write("\n")


if __name__ == "__main__":
    app()
