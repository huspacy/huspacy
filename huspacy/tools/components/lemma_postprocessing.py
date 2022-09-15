from spacy.lang.hu import Hungarian
import re


@Hungarian.component("lemma_smoother", assigns=["token.lemma"], requires=["token.lemma"])
def smooth_lemma(doc):
    for token in doc:
        if token.is_sent_start and token.tag_ != 'PROPN':
            token.lemma_ = token.lemma_.lower()

    return doc


@Hungarian.component("lemma_fixer", assigns=["token.lemma"], requires=["token.lemma"])
def fix_lemma(doc):
    rules = [remove_exclamation_marks, remove_question_marks, fix_date_suffixes, remove_suffix_after_numbers, roman_to_arabic]

    for token in doc:
        for rule in rules:
            modified = rule(token.text, token.lemma_, token.pos_)
            token.lemma_ = modified if modified != None else token.lemma_

    return doc


# Remove exclamation marks from lemmas
def remove_exclamation_marks(token: str, lemma: str, pos: str):
    if "!" != lemma and "!" in lemma:
        return lemma.split("!")[0]


# Remove question marks from lemmas
def remove_question_marks(token: str, lemma: str, pos: str):
    if "?" != lemma and "?" in lemma:
        return lemma.split("?")[0]


# Fix dates
def fix_date_suffixes(token: str, lemma: str, pos: str):
    r = re.compile(r'(\d+)-[j]?[éá]n?a?(t[őó]l)?')

    if pos == "NOUN" and re.match(r, lemma):
        return re.search(r, lemma).group(0) + "."


# Remove anything after numbers
def remove_suffix_after_numbers(token: str, lemma: str, pos: str):
    r = re.compile(r'(\d+([-,/_.:]?(._)?\d+)*[%]?(_km/h)?)')

    if pos == "NUM" and re.match(r, token):
        return re.search(r, token).group(0)


# Convert roman numbers to arabic
def roman_to_arabic(token: str, lemma: str, pos: str):
    r = re.compile(r'^([IVXLCDM]+(-[IVXLCDM]+)*)[.]?$')

    if pos == "ADJ" and re.match(r, token):
        roman = re.search(r, token).group(0)
        romans = roman.split("-")
        values = []

        for r in romans:
            dot = "." if "." == r[-1] else ""
            r = r[:-1] if dot else r

            rom_val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
            int_val = 0
            for i in range(len(r)):
                if i > 0 and rom_val[r[i]] > rom_val[r[i - 1]]:
                    int_val += rom_val[r[i]] - 2 * rom_val[r[i - 1]]
                else:
                    int_val += rom_val[r[i]]

            values.append(str(int_val) + dot)
        
        return "-".join(values)