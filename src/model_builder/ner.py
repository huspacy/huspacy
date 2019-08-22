import logging
import random
from pathlib import Path
from typing import Tuple, List, Iterable

import spacy
from spacy.gold import iob_to_biluo, offsets_from_biluo_tags, GoldParse
from spacy.scorer import Scorer
from spacy.tokens import Doc
from spacy.util import compounding, minibatch
from tqdm import tqdm

spacy.prefer_gpu()

TaggedSentence = Tuple[List[str], List[str]]


class WhitespaceTokenizer(object):
    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self, text):
        words = text.split(" ")
        # All tokens 'own' a subsequent space character in this tokenizer
        spaces = [True] * len(words)
        # try:
        return Doc(self.vocab, words=words, spaces=spaces)
        # except Exception as e:
        #     print(text)
        #     print(words)
        #     raise e


class DataIterator:
    def __init__(self):
        self.nlp = spacy.blank("hu")
        self.nlp.tokenizer = WhitespaceTokenizer(self.nlp.vocab)

    def _sentence_to_spacy_annotations(self, tokens, tags) -> Tuple[str, Tuple]:
        sentence = " ".join(tokens)
        tags = iob_to_biluo(tags)

        doc = self.nlp(sentence)
        annotations = offsets_from_biluo_tags(doc, tags)
        # print(sentence)
        # print(tags)
        # print(annotations)

        return sentence, annotations

    def tagged_sentences(self, path: str) -> Iterable[TaggedSentence]:
        with open(path) as f:
            toks, tags = [], []
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) >= 2:
                    tok = parts[0].strip()
                    tag = parts[-1]
                    if tag == 0:
                        tag = "O"
                    if len(tok) > 0:
                        toks.append(tok)
                        tags.append(tag)
                else:
                    sent, annotations = self._sentence_to_spacy_annotations(toks, tags)
                    if len(sent) > 0 and len(annotations) > 0:
                        yield sent, annotations
                    toks, tags = [], []
            if len(toks) > 0:
                sent, annotations = self._sentence_to_spacy_annotations(toks, tags)
                if len(sent) > 0 and len(annotations) > 0:
                    yield sent, annotations


class SpacyNerTrainer:
    def __init__(self, model, output_dir):
        self.model = model
        if model:
            logging.info("Loading HuSpacy")
            self.nlp = spacy.load(model, disable=["hun_sentencizer", "hun_lemmatizer"])
        else:
            logging.info("Creating a blank model")
            self.nlp = spacy.blank("hu")

        self._orig_tokenizer = self.nlp.tokenizer
        self.nlp.tokenizer = WhitespaceTokenizer(self.nlp.vocab)

        self.output_dir = output_dir

    def __call__(
            self,
            train_data,
            test_data,
            n_iter,
    ):

        if "ner" in self.nlp.pipe_names:
            logging.warning("Pipeline already has NER, removing...")
            self.nlp.remove_pipe("ner")
        ner = self.nlp.create_pipe("ner")
        self.nlp.add_pipe(ner, last=True)

        for sent, ann in (train_data + test_data):
            for _, _, label in ann:
                ner.add_label(label)

            # get names of other pipes to disable them during training
        other_pipes = [pipe for pipe in self.nlp.pipe_names if pipe != "ner"]
        logging.info("Starting the training with {} iterations".format(n_iter))
        with self.nlp.disable_pipes(*other_pipes):  # only train NER
            # if not self.model:
            # FIXME: pre-train the model
            self.nlp.begin_training()
            for itn in range(n_iter):
                random.shuffle(train_data)
                losses = {}
                # batch up the examples using spaCy's minibatch
                batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
                for batch in tqdm(batches):
                    texts, annotations = zip(*batch)
                    self.nlp.update(
                        docs=texts,  # batch of texts
                        golds=[
                            self._sent_to_goldparse(t, a) for t, a in batch
                        ],  # batch of annotations
                        drop=0.5,  # dropout - make it harder to memorise data
                        losses=losses,
                    )

                logging.info("Losses: {}".format(losses))

            scores = self.evaluate(test_data)
            logging.info("Test scores {}".format(scores))

    def store_model(self):
        self.nlp.tokenizer = self._orig_tokenizer
        output_dir = Path(self.output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        self.nlp.to_disk(output_dir)
        logging.info("Saved model to {}".format(output_dir))

    def evaluate(self, test_data):
        scorer = Scorer()
        for input_, annot in test_data:
            gold = self._sent_to_goldparse(input_, annot)
            predicted = self.nlp(input_)
            scorer.score(predicted, gold)
        return scorer.scores

    def _sent_to_goldparse(self, sentence, entity_annotations):
        doc_gold_text = self.nlp.make_doc(sentence)
        gold = GoldParse(doc_gold_text, entities=entity_annotations)
        # print(gold)
        return gold
