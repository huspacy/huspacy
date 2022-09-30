from spacy.lang.hu import Hungarian
from spacy import Doc
import re


@Hungarian.component(
    "lemma_case_smoother",
    assigns=["token.lemma"],
    requires=["token.lemma", "token.pos"],
)
def lemma_case_smoother(doc: Doc) -> Doc:
    """Smooth lemma casing by POS.

    DEPRECATED: This is not needed anymore, as the lemmatizer is now case-insensitive.

    Args:
        doc (Doc): Input document.

    Returns:
        Doc: Output document.
    """
    for token in doc:
        if token.is_sent_start and token.tag_ != "PROPN":
            token.lemma_ = token.lemma_.lower()

    return doc


@Hungarian.component(
    "lemma_smoother", assigns=["token.lemma"], requires=["token.lemma", "token.pos"]
)
def lemma_smoother(doc: Doc) -> Doc:
    """Fix lemma by regexes.

    Args:
        doc (Doc): Input document.

    Returns:
        Doc: Output document.
    """
    lemma_pp = LemmaPostprocessor()
    rules = [
        lemma_pp.remove_exclamation_marks,
        lemma_pp.remove_question_marks,
        lemma_pp.fix_date_suffixes,
        lemma_pp.remove_suffix_after_numbers,
    ]

    for token in doc:
        for rule in rules:
            modified = rule(token.text, token.lemma_, token.pos_)
            token.lemma_ = modified if modified != None else token.lemma_

    return doc


class LemmaPostprocessor:
    """Class for lemma postprocessing rules."""

    DATE_REGEX = re.compile(r"(\d+)-[j]?[éá]n?a?(t[őó]l)?")
    NUMBER_REGEX = re.compile(r"(\d+([-,/_.:]?(._)?\d+)*[%]?(_km/h)?)")

    @classmethod
    def remove_exclamation_marks(cls, token: str, lemma: str, pos: str) -> str:
        """Removes exclamation marks from the lemma.

        Args:
            token (str): The original token.
            lemma (str): The original lemma.
            pos (str): The part-of-speech tag of the token.

        Returns:
            str: The modified lemma.
        """

        if "!" != lemma and "!" in lemma:
            return lemma.split("!")[0]

    @classmethod
    def remove_question_marks(cls, token: str, lemma: str, pos: str) -> str:
        """Removes question marks from the lemma.

        Args:
            token (str): The original token.
            lemma (str): The original lemma.
            pos (str): The part-of-speech tag of the token.

        Returns:
            str: The modified lemma.
        """

        if "?" != lemma and "?" in lemma:
            return lemma.split("?")[0]

    @classmethod
    def fix_date_suffixes(cls, token: str, lemma: str, pos: str) -> str:
        """Fixes the suffixes of dates.

        Args:
            token (str): The original token.
            lemma (str): The original lemma.
            pos (str): The part-of-speech tag of the token.

        Returns:
            str: The modified lemma.
        """

        if pos == "NOUN" and re.match(cls.DATE_REGEX, lemma):
            return re.search(cls.DATE_REGEX, lemma).group(0) + "."

    @classmethod
    def remove_suffix_after_numbers(cls, token: str, lemma: str, pos: str) -> str:
        """Removes suffixes after numbers.

        Args:
            token (str): The original token.
            lemma (str): The original lemma.
            pos (str): The part-of-speech tag of the token.

        Returns:
            str: The modified lemma.
        """

        if pos == "NUM" and re.match(cls.NUMBER_REGEX, token):
            return re.search(cls.NUMBER_REGEX, token).group(0)


@Hungarian.component(
    "roman_to_arabic", assigns=["token.lemma"], requires=["token.text"]
)
def roman_to_arabic(doc: Doc) -> Doc:
    """Converts roman numerals to arabic numerals.

    Args:
        doc (Doc): The document to process.
    """
    r = re.compile(r"^([IVXLCDM]+(-[IVXLCDM]+)*)[.]?$")

    for token in doc:
        if token.pos_ == "ADJ" and re.match(r, token.text):
            roman = re.search(r, token.text).group(0)
            romans = roman.split("-")
            values = []

            for r in romans:
                dot = "." if "." == r[-1] else ""
                r = r[:-1] if dot else r

                rom_val = {
                    "I": 1,
                    "V": 5,
                    "X": 10,
                    "L": 50,
                    "C": 100,
                    "D": 500,
                    "M": 1000,
                }
                int_val = 0
                for i in range(len(r)):
                    if i > 0 and rom_val[r[i]] > rom_val[r[i - 1]]:
                        int_val += rom_val[r[i]] - 2 * rom_val[r[i - 1]]
                    else:
                        int_val += rom_val[r[i]]

                values.append(str(int_val) + dot)

            token.lemma_ = "-".join(values)
