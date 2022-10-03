from spacy.lang.hu import Hungarian
from spacy.pipeline import Pipe
from spacy import Language
from spacy.tokens.doc import Doc
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


class LemmaSmoother(Pipe):
    """Smooths lemma by applying rules.

    Args:
        Pipe (Pipe): spaCy Pipe
    """

    @staticmethod
    @Hungarian.factory(
        "lemma_smoother", assigns=["token.lemma"], requires=["token.lemma", "token.pos"]
    )
    def create_lemma_smoother(nlp: Hungarian, name: str) -> "LemmaSmoother":
        return LemmaSmoother()

    def __init__(self):
        self._date_regex = re.compile(r"(\d+)-[j]?[éá]n?a?(t[őó]l)?")
        self._number_regex = re.compile(r"(\d+([-,/_.:]?(._)?\d+)*[%]?(_km/h)?)")

    def __call__(self, doc: Doc) -> Doc:
        rules = [
            self.remove_exclamation_marks,
            self.remove_question_marks,
            self.fix_date_suffixes,
            self.remove_suffix_after_numbers,
        ]

        for token in doc:
            for rule in rules:
                modified = rule(token.text, token.lemma_, token.pos_)
                token.lemma_ = modified if modified != None else token.lemma_

        return doc

    def remove_exclamation_marks(self, token: str, lemma: str, pos: str) -> str:
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

    def remove_question_marks(self, token: str, lemma: str, pos: str) -> str:
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

    def fix_date_suffixes(self, token: str, lemma: str, pos: str) -> str:
        """Fixes the suffixes of dates.

        Args:
            token (str): The original token.
            lemma (str): The original lemma.
            pos (str): The part-of-speech tag of the token.

        Returns:
            str: The modified lemma.
        """

        if pos == "NOUN" and re.match(self._date_regex, lemma):
            return re.search(self._date_regex, lemma).group(0) + "."

    def remove_suffix_after_numbers(self, token: str, lemma: str, pos: str) -> str:
        """Removes suffixes after numbers.

        Args:
            token (str): The original token.
            lemma (str): The original lemma.
            pos (str): The part-of-speech tag of the token.

        Returns:
            str: The modified lemma.
        """

        if pos == "NUM" and re.match(self._number_regex, token):
            return re.search(self._number_regex, token).group(0)


class RomanToArabic(Pipe):
    """Converts roman numerals to arabic numerals.

    Args:
        Pipe (Pipe): spaCy Pipe
    """

    @staticmethod
    @Language.factory(
        "roman_to_arabic", assigns=["token.lemma"], requires=["token.text"]
    )
    def create_component(nlp: Language, name: str):
        return RomanToArabic()

    def __init__(self):
        self._regex = re.compile(r"^([IVXLCDM]+(-[IVXLCDM]+)*)[.]?$")
        self._rom_val = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000,
        }

    def __call__(self, doc: Doc) -> Doc:
        for token in doc:
            if token.pos_ == "ADJ" and re.match(self._regex, token.text):
                roman = re.search(self._regex, token.text).group(0)
                romans = roman.split("-")
                values = []

                for r in romans:
                    dot = "." if "." == r[-1] else ""
                    r = r[:-1] if dot else r

                    int_val = 0
                    for i in range(len(r)):
                        if i > 0 and self._rom_val[r[i]] > self._rom_val[r[i - 1]]:
                            int_val += self._rom_val[r[i]] - 2 * self._rom_val[r[i - 1]]
                        else:
                            int_val += self._rom_val[r[i]]

                    values.append(str(int_val) + dot)

                token.lemma_ = "-".join(values)
        return doc
