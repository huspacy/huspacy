import logging
import random
from pathlib import Path
from typing import Tuple, List, Iterable

import mlflow
import spacy
from spacy.gold import iob_to_biluo, offsets_from_biluo_tags, GoldParse
from spacy.scorer import Scorer
from spacy.tokens import Doc
from spacy.util import compounding, minibatch, fix_random_seed, load_model_from_path
from tqdm import tqdm

spacy.prefer_gpu()

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

    def _sentence_to_spacy_annotations(self, tokens, tags) -> Tuple[str, Tuple]:
        sentence = " ".join(tokens)
        tags = iob_to_biluo(tags)

        doc = self.nlp(sentence)
        annotations = offsets_from_biluo_tags(doc, tags)
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

    def tagged_sentences(self, path: str) -> Iterable[TaggedSentence]:
        for toks, tags in self.sentences_with_tags(path):
            sent, annotations = self._sentence_to_spacy_annotations(toks, tags)
            if len(sent) > 0 and len(annotations) > 0:
                yield sent, annotations


def get_position_label(i, words, tags, heads, labels, ents):
    """Return labels indicating the position of the word in the document.
    """
    if len(words) < 20:
        return "short-doc"
    elif i == 0:
        return "first-word"
    elif i < 10:
        return "early-word"
    elif i < 20:
        return "mid-word"
    elif i == len(words) - 1:
        return "last-word"
    else:
        return "late-word"


class SpacyNerTrainer:
    def __init__(self, model_path, output_dir):
        self.model = model_path
        if self.model:
            logging.info("Loading HuSpacy")
            self.nlp = spacy.load(
                self.model, disable=["hun_sentencizer", "hun_lemmatizer"]
            )
            # self.nlp = nlp = Hungarian().from_disk(model_path,  disable=["hun_sentencizer", "hun_lemmatizer"])
        else:
            logging.info("Creating a blank model")
            self.nlp = spacy.blank("hu")

        self._orig_tokenizer = self.nlp.tokenizer
        self.nlp.tokenizer = WhitespaceTokenizer(self.nlp.vocab)

        self.output_dir = output_dir

    def __call__(self, train_data, dev_data, test_data, n_iter, dropout, patience=10):

        if "ner" in self.nlp.pipe_names:
            logging.warning("Pipeline already has NER, removing...")
            self.nlp.remove_pipe("ner")
        ner = self.nlp.create_pipe("ner")
        # ner.add_multitask_objective(get_position_label)
        self.nlp.add_pipe(ner, last=True)

        for sent, ann in train_data + dev_data + test_data:
            for _, _, label in ann:
                ner.add_label(label)

            # get names of other pipes to disable them during training
        other_pipes = [pipe for pipe in self.nlp.pipe_names if pipe != "ner"]
        logging.info("Starting the training with {} iterations".format(n_iter))
        fix_random_seed(42)

        best_dev_score = 0
        best_dev_itn = -1
        with self.nlp.disable_pipes(*other_pipes):  # only train NER
            # if not self.model:
            # FIXME: pre-train the model
            mlflow.log_param("base_model", Path(self.model).name)
            mlflow.log_param("n_iter", n_iter)
            mlflow.log_param("dropout", dropout)
            self.nlp.begin_training()
            for itn in tqdm(list(range(n_iter)), desc="iterations"):
                random.shuffle(train_data)
                losses = {}
                # batch up the examples using spaCy's minibatch
                batches = list(
                    minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
                )
                for batch in tqdm(batches, desc="batches"):
                    texts, annotations = zip(*batch)
                    self.nlp.update(
                        docs=texts,  # batch of texts
                        golds=[
                            self._sent_to_goldparse(t, a) for t, a in batch
                        ],  # batch of annotations
                        drop=dropout,  # dropout - make it harder to memorise data
                        losses=losses,
                    )

                # logging.info("Losses: {}".format(losses))
                mlflow.log_metric("loss", losses["ner"], step=itn)
                train_scores = self.evaluate(train_data)
                mlflow.log_metrics(
                    {"train_" + k: v for k, v in train_scores.items()}, step=itn
                )
                dev_scores = self.evaluate(dev_data)
                mlflow.log_metrics(
                    {"dev_" + k: v for k, v in dev_scores.items()}, step=itn
                )
                self.store_model(Path(self.output_dir) / "model_{}".format(itn))

                act_score = dev_scores["f1"]
                if best_dev_score < act_score:
                    best_dev_score = act_score
                    best_dev_itn = itn
                else:
                    if itn - best_dev_itn >= patience:
                        break

            load_model_from_path(Path(self.output_dir) / "model_{}".format(best_dev_itn))
            scores = self.evaluate(test_data)
            logging.info("Test scores {}".format(scores))
            mlflow.log_metrics(scores, step=itn)
            self.store_model(Path(self.output_dir) / "model-final")

    def store_model(self, path):
        self.nlp.tokenizer = self._orig_tokenizer
        output_dir = Path(path)
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
        scores_per_type = scorer.scores.get("ents_per_type", {})
        scores_per_type = {
            "{}_{}".format(ent, metric): score
            for ent, scores in scores_per_type.items()
            for metric, score in scores.items()
        }
        result = dict(
            prec=scorer.scores["ents_p"],
            rec=scorer.scores["ents_r"],
            f1=scorer.scores["ents_f"],
        )
        result.update(scores_per_type)
        return result

    def _sent_to_goldparse(self, sentence, entity_annotations):
        doc_gold_text = self.nlp.make_doc(sentence)
        gold = GoldParse(doc_gold_text, entities=entity_annotations)
        return gold
