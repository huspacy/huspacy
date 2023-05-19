import sys
import unicodedata
from statsmodels.stats.contingency_tables import mcnemar
import typer

app = typer.Typer()


@app.command()
def main(gold_file: str, model1_file: str, model2_file: str):
    gold_file = open(gold_file, "r", encoding="utf-8")
    model1_file = open(model1_file, "r", encoding="utf-8")
    model2_file = open(model2_file, "r", encoding="utf-8")

    gold_ud = load_conllu(gold_file)
    model1_ud = load_conllu(model1_file)
    model2_ud = load_conllu(model2_file)

    model1_alignments = align_words(gold_ud.words, model1_ud.words)
    model2_alignments = align_words(gold_ud.words, model2_ud.words)

    print(
        f"""model1 alignment: gold: {len(model1_alignments.gold_words)}, 
        system: {len(model1_alignments.system_words)}, 
        matched: {len(model1_alignments.matched_words)}"""
    )
    print(
        f"""model2 alignment: gold: {len(model2_alignments.gold_words)}, 
        system: {len(model2_alignments.system_words)}, 
        matched: {len(model2_alignments.matched_words)}"""
    )

    # print(model1_alignments.matched_words[0].gold_word.columns[LEMMA], model1_alignments.matched_words[0].system_word.columns[LEMMA])

    a = 0  # both models predicted correctly
    b = 0  # model1 predicted correctly, model2 predicted incorrectly
    c = 0  # model1 predicted incorrectly, model2 predicted correctly
    d = 0  # both models predicted incorrectly

    for m1, m2 in zip(model1_alignments.matched_words, model2_alignments.matched_words):
        # print(m1.gold_word.columns[LEMMA], m1.system_word.columns[LEMMA], m2.system_word.columns[LEMMA])

        gold_lemma = m1.gold_word.columns[LEMMA]
        model1_lemma = m1.system_word.columns[LEMMA]
        model2_lemma = m2.system_word.columns[LEMMA]

        if gold_lemma == model1_lemma and gold_lemma == model2_lemma:
            a += 1
        elif gold_lemma == model1_lemma and gold_lemma != model2_lemma:
            b += 1
        elif gold_lemma != model1_lemma and gold_lemma == model2_lemma:
            c += 1
        elif gold_lemma != model1_lemma and gold_lemma != model2_lemma:
            d += 1

    contingency_table = [[a, b], [c, d]]
    print(f"contingency table: {contingency_table}")

    result = mcnemar(contingency_table, exact=True, correction=True)
    print(f"p-value: {result.pvalue:.8f}")
    print(f"statistic: {result.statistic:.2f}")

    gold_file.close()
    model1_file.close()
    model2_file.close()


### Source conll18_ud_eval.py

ID, FORM, LEMMA, UPOS, XPOS, FEATS, HEAD, DEPREL, DEPS, MISC = range(10)

CONTENT_DEPRELS = {
    "nsubj",
    "obj",
    "iobj",
    "csubj",
    "ccomp",
    "xcomp",
    "obl",
    "vocative",
    "expl",
    "dislocated",
    "advcl",
    "advmod",
    "discourse",
    "nmod",
    "appos",
    "nummod",
    "acl",
    "amod",
    "conj",
    "fixed",
    "flat",
    "compound",
    "list",
    "parataxis",
    "orphan",
    "goeswith",
    "reparandum",
    "root",
    "dep",
}

FUNCTIONAL_DEPRELS = {"aux", "cop", "mark", "det", "clf", "case", "cc"}

UNIVERSAL_FEATURES = {
    "PronType",
    "NumType",
    "Poss",
    "Reflex",
    "Foreign",
    "Abbr",
    "Gender",
    "Animacy",
    "Number",
    "Case",
    "Definite",
    "Degree",
    "VerbForm",
    "Mood",
    "Tense",
    "Aspect",
    "Voice",
    "Evident",
    "Polarity",
    "Person",
    "Polite",
}


def load_conllu_file(path):
    _file = open(
        path, mode="r", **({"encoding": "utf-8"} if sys.version_info >= (3, 0) else {})
    )
    return load_conllu(_file)


# UD Error is used when raising exceptions in this module
class UDError(Exception):
    pass


# Conversion methods handling `str` <-> `unicode` conversions in Python2
def _decode(text):
    return (
        text
        if sys.version_info[0] >= 3 or not isinstance(text, str)
        else text.decode("utf-8")
    )


def _encode(text):
    return (
        text
        if sys.version_info[0] >= 3 or not isinstance(text, unicode)
        else text.encode("utf-8")
    )


def load_conllu(file):
    # Internal representation classes
    class UDRepresentation:
        def __init__(self):
            # Characters of all the tokens in the whole file.
            # Whitespace between tokens is not included.
            self.characters = []
            # List of UDSpan instances with start&end indices into `characters`.
            self.tokens = []
            # List of UDWord instances.
            self.words = []
            # List of UDSpan instances with start&end indices into `characters`.
            self.sentences = []

    class UDSpan:
        def __init__(self, start, end):
            self.start = start
            # Note that self.end marks the first position **after the end** of span,
            # so we can use characters[start:end] or range(start, end).
            self.end = end

    class UDWord:
        def __init__(self, span, columns, is_multiword):
            # Span of this word (or MWT, see below) within ud_representation.characters.
            self.span = span
            # 10 columns of the CoNLL-U file: ID, FORM, LEMMA,...
            self.columns = columns
            # is_multiword==True means that this word is part of a multi-word token.
            # In that case, self.span marks the span of the whole multi-word token.
            self.is_multiword = is_multiword
            # Reference to the UDWord instance representing the HEAD (or None if root).
            self.parent = None
            # List of references to UDWord instances representing functional-deprel children.
            self.functional_children = []
            # Only consider universal FEATS.
            self.columns[FEATS] = "|".join(
                sorted(
                    feat
                    for feat in columns[FEATS].split("|")
                    if feat.split("=", 1)[0] in UNIVERSAL_FEATURES
                )
            )
            # Let's ignore language-specific deprel subtypes.
            self.columns[DEPREL] = columns[DEPREL].split(":")[0]
            # Precompute which deprels are CONTENT_DEPRELS and which FUNCTIONAL_DEPRELS
            self.is_content_deprel = self.columns[DEPREL] in CONTENT_DEPRELS
            self.is_functional_deprel = self.columns[DEPREL] in FUNCTIONAL_DEPRELS

    ud = UDRepresentation()

    # Load the CoNLL-U file
    index, sentence_start = 0, None
    while True:
        line = file.readline()
        if not line:
            break
        line = _decode(line.rstrip("\r\n"))

        # Handle sentence start boundaries
        if sentence_start is None:
            # Skip comments
            if line.startswith("#"):
                continue
            # Start a new sentence
            ud.sentences.append(UDSpan(index, 0))
            sentence_start = len(ud.words)
        if not line:
            # Add parent and children UDWord links and check there are no cycles
            def process_word(word):
                if word.parent == "remapping":
                    raise UDError("There is a cycle in a sentence")
                if word.parent is None:
                    head = int(word.columns[HEAD])
                    if head < 0 or head > len(ud.words) - sentence_start:
                        raise UDError(
                            "HEAD '{}' points outside of the sentence".format(
                                _encode(word.columns[HEAD])
                            )
                        )
                    if head:
                        parent = ud.words[sentence_start + head - 1]
                        word.parent = "remapping"
                        process_word(parent)
                        word.parent = parent

            for word in ud.words[sentence_start:]:
                process_word(word)
            # func_children cannot be assigned within process_word
            # because it is called recursively and may result in adding one child twice.
            for word in ud.words[sentence_start:]:
                if word.parent and word.is_functional_deprel:
                    word.parent.functional_children.append(word)

            # Check there is a single root node
            if (
                len([word for word in ud.words[sentence_start:] if word.parent is None])
                != 1
            ):
                raise UDError("There are multiple roots in a sentence")

            # End the sentence
            ud.sentences[-1].end = index
            sentence_start = None
            continue

        # Read next token/word
        columns = line.split("\t")
        if len(columns) != 10:
            raise UDError(
                "The CoNLL-U line does not contain 10 tab-separated columns: '{}'".format(
                    _encode(line)
                )
            )

        # Skip empty nodes
        if "." in columns[ID]:
            continue

        # Delete spaces from FORM, so gold.characters == system.characters
        # even if one of them tokenizes the space. Use any Unicode character
        # with category Zs.
        columns[FORM] = "".join(
            filter(lambda c: unicodedata.category(c) != "Zs", columns[FORM])
        )
        if not columns[FORM]:
            raise UDError("There is an empty FORM in the CoNLL-U file")

        # Save token
        ud.characters.extend(columns[FORM])
        ud.tokens.append(UDSpan(index, index + len(columns[FORM])))
        index += len(columns[FORM])

        # Handle multi-word tokens to save word(s)
        if "-" in columns[ID]:
            try:
                start, end = map(int, columns[ID].split("-"))
            except:
                raise UDError(
                    "Cannot parse multi-word token ID '{}'".format(_encode(columns[ID]))
                )

            for _ in range(start, end + 1):
                word_line = _decode(file.readline().rstrip("\r\n"))
                word_columns = word_line.split("\t")
                if len(word_columns) != 10:
                    raise UDError(
                        "The CoNLL-U line does not contain 10 tab-separated columns: '{}'".format(
                            _encode(word_line)
                        )
                    )
                ud.words.append(UDWord(ud.tokens[-1], word_columns, is_multiword=True))
        # Basic tokens/words
        else:
            try:
                word_id = int(columns[ID])
            except:
                raise UDError("Cannot parse word ID '{}'".format(_encode(columns[ID])))
            if word_id != len(ud.words) - sentence_start + 1:
                raise UDError(
                    "Incorrect word ID '{}' for word '{}', expected '{}'".format(
                        _encode(columns[ID]),
                        _encode(columns[FORM]),
                        len(ud.words) - sentence_start + 1,
                    )
                )

            try:
                head_id = int(columns[HEAD])
            except:
                raise UDError("Cannot parse HEAD '{}'".format(_encode(columns[HEAD])))
            if head_id < 0:
                raise UDError("HEAD cannot be negative")

            ud.words.append(UDWord(ud.tokens[-1], columns, is_multiword=False))

    if sentence_start is not None:
        raise UDError("The CoNLL-U file does not end with empty line")

    return ud


class AlignmentWord:
    def __init__(self, gold_word, system_word):
        self.gold_word = gold_word
        self.system_word = system_word


class Alignment:
    def __init__(self, gold_words, system_words):
        self.gold_words = gold_words
        self.system_words = system_words
        self.matched_words = []
        self.matched_words_map = {}

    def append_aligned_words(self, gold_word, system_word):
        self.matched_words.append(AlignmentWord(gold_word, system_word))
        self.matched_words_map[system_word] = gold_word


def beyond_end(words, i, multiword_span_end):
    if i >= len(words):
        return True
    if words[i].is_multiword:
        return words[i].span.start >= multiword_span_end
    return words[i].span.end > multiword_span_end


def extend_end(word, multiword_span_end):
    if word.is_multiword and word.span.end > multiword_span_end:
        return word.span.end
    return multiword_span_end


def find_multiword_span(gold_words, system_words, gi, si):
    # We know gold_words[gi].is_multiword or system_words[si].is_multiword.
    # Find the start of the multiword span (gs, ss), so the multiword span is minimal.
    # Initialize multiword_span_end characters index.
    if gold_words[gi].is_multiword:
        multiword_span_end = gold_words[gi].span.end
        if (
            not system_words[si].is_multiword
            and system_words[si].span.start < gold_words[gi].span.start
        ):
            si += 1
    else:  # if system_words[si].is_multiword
        multiword_span_end = system_words[si].span.end
        if (
            not gold_words[gi].is_multiword
            and gold_words[gi].span.start < system_words[si].span.start
        ):
            gi += 1
    gs, ss = gi, si

    # Find the end of the multiword span
    # (so both gi and si are pointing to the word following the multiword span end).
    while not beyond_end(gold_words, gi, multiword_span_end) or not beyond_end(
        system_words, si, multiword_span_end
    ):
        if gi < len(gold_words) and (
            si >= len(system_words)
            or gold_words[gi].span.start <= system_words[si].span.start
        ):
            multiword_span_end = extend_end(gold_words[gi], multiword_span_end)
            gi += 1
        else:
            multiword_span_end = extend_end(system_words[si], multiword_span_end)
            si += 1
    return gs, ss, gi, si


def compute_lcs(gold_words, system_words, gi, si, gs, ss):
    lcs = [[0] * (si - ss) for i in range(gi - gs)]
    for g in reversed(range(gi - gs)):
        for s in reversed(range(si - ss)):
            if (
                gold_words[gs + g].columns[FORM].lower()
                == system_words[ss + s].columns[FORM].lower()
            ):
                lcs[g][s] = 1 + (
                    lcs[g + 1][s + 1] if g + 1 < gi - gs and s + 1 < si - ss else 0
                )
            lcs[g][s] = max(lcs[g][s], lcs[g + 1][s] if g + 1 < gi - gs else 0)
            lcs[g][s] = max(lcs[g][s], lcs[g][s + 1] if s + 1 < si - ss else 0)
    return lcs


def align_words(gold_words, system_words):
    alignment = Alignment(gold_words, system_words)

    gi, si = 0, 0
    while gi < len(gold_words) and si < len(system_words):
        if gold_words[gi].is_multiword or system_words[si].is_multiword:
            # A: Multi-word tokens => align via LCS within the whole "multiword span".
            gs, ss, gi, si = find_multiword_span(gold_words, system_words, gi, si)

            if si > ss and gi > gs:
                lcs = compute_lcs(gold_words, system_words, gi, si, gs, ss)

                # Store aligned words
                s, g = 0, 0
                while g < gi - gs and s < si - ss:
                    if (
                        gold_words[gs + g].columns[FORM].lower()
                        == system_words[ss + s].columns[FORM].lower()
                    ):
                        alignment.append_aligned_words(
                            gold_words[gs + g], system_words[ss + s]
                        )
                        g += 1
                        s += 1
                    elif lcs[g][s] == (lcs[g + 1][s] if g + 1 < gi - gs else 0):
                        g += 1
                    else:
                        s += 1
        else:
            # B: No multi-word token => align according to spans.
            if (gold_words[gi].span.start, gold_words[gi].span.end) == (
                system_words[si].span.start,
                system_words[si].span.end,
            ):
                alignment.append_aligned_words(gold_words[gi], system_words[si])
                gi += 1
                si += 1
            elif gold_words[gi].span.start <= system_words[si].span.start:
                gi += 1
            else:
                si += 1

    return alignment


### Source end

if __name__ == "__main__":
    app()
