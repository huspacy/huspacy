#!/usr/bin/env python3

import sys
import ftfy
from typing import Iterable


MIN_CHAR_RATIO = .8
MIN_CHARS = 10
MIN_TOKENS = 4


def clean(lines: Iterable[str]) -> Iterable[str]:
    line: str
    for line in lines:
        line = ftfy.fix_text(line.strip())
        n_chars: int = sum(not ch.isspace() for ch in line)
        n_lower: int = sum(ch.islower() for ch in line)
        char_ratio: float = float(n_lower) / n_chars if n_chars >= MIN_CHARS else 0.0
        if char_ratio >= MIN_CHAR_RATIO:
            yield line


def get_sentences(lines: Iterable[str]) -> Iterable[str]:
    sentence = []
    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            continue
        elif line == "":
            if len(sentence) > 0:
                yield " ".join(sentence)
                sentence = []
        else:
            sentence.append(line.split("\t")[0])

    if len(sentence) > 0:
        yield " ".join(sentence)


if __name__ == "__main__":
    _ = next(sys.stdin)
    sentences: Iterable[str] = get_sentences(sys.stdin)
    cleaned: Iterable[str] = clean(sentences)
    for sentence in cleaned:
        print(sentence)
