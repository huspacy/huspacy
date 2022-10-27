import json

try:
    from importlib.resources import files
except:
    from importlib_resources import files
from io import BytesIO
from typing import List, Dict
from urllib.request import urlopen
from zipfile import ZipFile

from spacy import Language
from spacy.lang.hu import Hungarian
from spacy.pipeline import SpanRuler, Pipe
from spacy.tokens import Token, Doc


def create_pattern(words: List[str], label: str):
    return {"label": label, "pattern": [{"LOWER": word} for word in words]}


class PrecoSentiLoader:
    def load(self) -> List[Dict]:
        resp = urlopen("https://www.opendata.hu/storage/f/2016-06-06T11%3A27%3A11.366Z/precosenti.zip")
        zipfile = ZipFile(BytesIO(resp.read()))
        lexicon = []
        for line in zipfile.open("PrecoSenti/PrecoNeg.txt").readlines():
            words = line.decode("utf-8").strip().split()
            lexicon.append(create_pattern(words, label="NEG"))

        for line in zipfile.open("PrecoSenti/PrecoPos.txt").readlines():
            words = line.decode("utf-8").strip().split()
            lexicon.append(create_pattern(words, label="NEG"))

        return lexicon


class PolTextLexiconLoader:
    def load(self) -> List[Dict]:
        lexicon = []
        pos_resp = urlopen("https://raw.githubusercontent.com/poltextlab/sentiment_hun/main/PolPos_final.txt")
        for line in pos_resp.readlines():
            words = line.decode("utf-8").strip().split()
            lexicon.append(create_pattern(words, label="POS"))
        pos_resp = urlopen("https://raw.githubusercontent.com/poltextlab/sentiment_hun/main/PolNeg_final.txt")
        for line in pos_resp.readlines():
            words = line.decode("utf-8").strip().split()
            lexicon.append(create_pattern(words, label="NEG"))
        return lexicon


@Hungarian.factory(
    "sentiment_lexicon",
    assigns=["token._.sentiment"],
    requires=["token.text"],
    default_config={"lexicon_id": "poltext"},
)
def create(nlp: Language, name: str, lexicon_id: str) -> "HunSentimentLexiconAnnotator":
    return HunSentimentLexiconAnnotator(nlp, lexicon_id)


class HunSentimentLexiconAnnotator(Pipe):
    def __init__(self, nlp: Language, lexicon_id: str):
        assert lexicon_id in {"poltext", "precognox"}
        lexicon_file = files("huspacy").joinpath(f"resources/{lexicon_id}_sentiment.json").open()
        patterns: List[Dict] = json.load(lexicon_file)

        self._span_ruler = SpanRuler(nlp, spans_key="sentiment", overwrite=True)
        self._span_ruler.add_patterns(patterns)

        Token.set_extension("sentiment", default=0)
        self._lexicon = lexicon_id

    def __call__(self, doc: Doc) -> Doc:
        token: Token
        self._span_ruler(doc)

        for token in doc:
            # noinspection PyProtectedMember
            token._.sentiment = None

        for span in doc.spans["sentiment"]:
            for token in span:
                # noinspection PyProtectedMember
                token._.sentiment = span.label_

        return doc


def update_lexicons():
    with files("huspacy").joinpath("resources/poltext_sentiment.json").open("w") as f:
        data = PolTextLexiconLoader().load()
        json.dump(data, f, indent=2)
    with files("huspacy").joinpath("resources/precognox_sentiment.json").open("w") as f:
        data = PrecoSentiLoader().load()
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    update_lexicons()
