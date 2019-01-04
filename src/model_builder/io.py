from os import path

import conllu
import pandas as pd
from tqdm import tqdm

TAG_MAP = {"CONJ": "CCONJ", "Y": "X", "VAN": "X"}
RESOURCES_ROOT = path.abspath(path.join(path.dirname(__file__), "..", "resources"))


def parse_szk_morph(path):
    with open(path) as f:
        tok_id = 1
        sentence = []
        for line in f:
            line = line.strip()
            if len(line) == 0 or line.startswith("#"):
                yield "\n".join("\t".join(tok) for tok in sentence)
                sentence = []
                tok_id = 1
            else:
                parts = line.split("\t")
                sentence.append(
                    (
                        str(tok_id),
                        parts[0],
                        parts[1],
                        parts[2],
                        "_",
                        parts[3],
                        "0",
                        "_",
                        "_",
                        "_",
                    )
                )
                tok_id += 1
        if len(sentence):
            yield "\n".join("\t".join(tok) for tok in sentence)


def parse_szk_dep(path):
    with open(path) as f:
        sentence = []
        for line in f:
            line = line.strip()
            if len(line) == 0 or line.startswith("#"):
                yield "\n".join("\t".join(tok) for tok in sentence)
                sentence = []
            else:
                parts = line.split("\t")
                if parts[3] in {"ELL", "VAN"}:
                    continue
                sentence.append(
                    (
                        parts[0],
                        parts[1],
                        TAG_MAP.get(parts[3], parts[3]),
                        parts[4],
                        parts[5],
                        parts[7],
                        "0",  # parts[9],
                        "_",  # parts[11],
                        parts[13],
                        "_",
                    )
                )
        if len(sentence):
            yield "\n".join("\t".join(tok) for tok in sentence)


def sentence_repr(s):
    return "".join([t["form"] for t in s])


def read_conllu_data_for_lemmy(path):
    with open(path) as f:
        df = pd.DataFrame(tok for sent in tqdm(conllu.parse(f.read())) for tok in sent)
        X = [
            (word_class, full_form)
            for _, (word_class, full_form) in df[["upostag", "form"]].iterrows()
        ]
        y = [lemma for _, (lemma,) in df[["lemma"]].iterrows()]
        return X, y


def format_as_conllu(doc, sent_id, prefix=""):
    res = []
    for sent in list(doc.sents):
        #         res.append("# sent_id = %s"%(prefix+str(sent_id)))
        #         res.append("# text = %s"%sent.sent)

        for i, word in enumerate(sent):
            if word.dep_.lower().strip() == "root":
                head_idx = 0
            else:
                head_idx = word.head.i - sent[0].i + 1

            linetuple = (
                str(i + 1),  # ID
                word.text,  # FORM
                word.lemma_,  # LEMMA
                word.pos_,  # UPOSTAG
                "_",  # XPOSTAG
                "_",  # FEATS
                str(head_idx),  # HEAD
                word.dep_,  # DEPREL
                "_",  # DEPS
                "_",  # MISC
            )
            res.append("\t".join(linetuple))

        sent_id += 1
        res.append("")
    return "\n".join(res) + "\n"
