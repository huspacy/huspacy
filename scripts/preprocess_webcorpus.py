#!/usr/bin/env python3

import sys
import ftfy
from typing import Iterable
from spacy.lang.hu import Hungarian


MIN_CHAR_RATIO = .8
MIN_CHARS = 10
MIN_TOKENS = 4
TOKENIZER = Hungarian().tokenizer


def clean(lines: Iterable[str]) -> Iterable[str]:
    line: str
    for line in lines:
        line = ftfy.fix_text(line.strip())
        n_chars: int = sum(not ch.isspace() for ch in line)
        n_lower: int = sum(ch.islower() for ch in line)
        char_ratio: float = float(n_lower) / n_chars if n_chars >= MIN_CHARS else 0.0
        if char_ratio >= MIN_CHAR_RATIO:
            yield line


def tokenize(lines: Iterable[str]) -> Iterable[str]:
    for line in lines:
        doc = TOKENIZER(line)
        n_tokens = sum(not tok.is_punct for tok in doc)
        if len(doc) >= MIN_TOKENS:
            yield " ".join(token.text for token in doc).strip()


if __name__ == "__main__":
    cleaned: Iterable[str] = clean(sys.stdin)
    tokenized: Iterable[str] = tokenize(cleaned)
    for sentence in tokenized:
        print(sentence)
