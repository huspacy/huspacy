import logging
from typing import List

from spacy import Language
from spacy.lang.hu import Hungarian
from spacy.pipeline import Pipe
from spacy.tokens import Doc
from spacy.training import biluo_tags_to_spans, iob_to_biluo

try:
    from transformers import AutoTokenizer, BertTokenizerFast, BertForTokenClassification
    from transformers.models.auto.modeling_auto import AutoModelForTokenClassification
    from spacy_alignments import get_alignments
except ImportError:
    logging.warning("The nerpp component won't be available until dependencies are installed.")


@Hungarian.factory(
    "nerpp",
    assigns=["doc.spans"],
    requires=["token.text"],
)
def create(nlp: Language, name: str) -> "EntityRecognizerONPP":
    """
    Creates an entity recognizer using a model which supports 30+ entity types.
    (https://huggingface.co/novakat/nerkor-cars-onpp-hubert)
    """
    return EntityRecognizerONPP(nlp, name)


class EntityRecognizerONPP(Pipe):
    """
    spaCy pipeline component for wrapping the ONPP NER model: https://huggingface.co/novakat/nerkor-cars-onpp-hubert
    """

    MODEL_HF_PATH = "novakat/nerkor-cars-onpp-hubert"

    def __init__(self, nlp: Language, name: str):
        """

        Args:
            nlp (Language): spaCy pipeline to use
            name (str): pipeline component name
        """

        self._name = name
        self._nlp = nlp
        self._tokenizer: BertTokenizerFast = AutoTokenizer.from_pretrained(self.MODEL_HF_PATH)
        self._model: BertForTokenClassification = AutoModelForTokenClassification.from_pretrained(self.MODEL_HF_PATH)

    def __call__(self, doc: Doc) -> Doc:
        tokens: List[str] = [tok.text for tok in doc]
        tf_tokens = self._tokenizer(tokens, return_tensors="pt", is_split_into_words=True)
        # noinspection PyCallingNonCallable
        res = self._model(**tf_tokens)
        predicted_class_ids = res.logits.argmax(dim=2)[0].tolist()

        wordpieces: List[str] = self._tokenizer.convert_ids_to_tokens(tf_tokens["input_ids"][0])[1:-1]
        alignments: List[List[int]] = get_alignments(tokens, wordpieces)[0]

        wp_labels: [List[str]] = [self._model.config.id2label[cls_id] for cls_id in predicted_class_ids[1:-1]]
        labels: List[str] = [wp_labels[wp_indices[0]] for wp_indices in alignments]

        doc.spans["ents"] = biluo_tags_to_spans(doc, iob_to_biluo(labels))
        return doc
