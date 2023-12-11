# `emMorph` integration

HuSpaCy doesn't employ an integrated morphological analyzer, however it might be useful to include one in the pipeline in some cases. `emMorph` is one of the most popular morph. analyzers available having a Python interface. 

## Install dependencies

`emMorph` depends on `hfst`, which must be installed by the package manager of your OS. In Debian/Ubuntu: `apt install hfst`. Further on, one must also install the tool's python wrapper and the UD converter:

- `pip install https://github.com/nytud/emmorphpy/releases/download/v1.1.0/emmorphpy-1.1.0-py3-none-any.whl`
- `pip install https://github.com/vadno/emmorph2ud2/releases/download/v1.0.1/emmorph2ud2-1.0.1-py3-none-any.whl`

## Usage

First we need to create a wrapper for `emMorph`:

```python
from spacy.tokens import Doc, Token, MorphAnalysis
from spacy.language import Language
from spacy.lang.hu import Hungarian 
from spacy.morphology import Morphology
from typing import List, Tuple, Dict
from emmorph2ud2 import EmMorph2UD2
from emmorphpy import EmMorphPy


@Hungarian.factory(
    "emmorph",
    requires=["token.text"],
)
def create_emmorph(nlp: Language, name: str) -> "EmMorphPyComponent":
    return EmMorphPyComponent(nlp, name)

class EmMorphPyComponent:
    def __init__(self, nlp: Language, name: str):
        self._nlp = nlp
        self._name = name
        self._em = EmMorphPy()
        self._converter = EmMorph2UD2()
        Token.set_extension("em_anas", default=[], force=True)
        Token.set_extension("em_tag", default=None, force=True)
        Token.set_extension("em_lemma", default=None, force=True)
        Token.set_extension("ud_tag", default=[], force=True)
        Token.set_extension("ud_anas", default=[], force=True)
        Token.set_extension("ud_morph", default=None, force=True)

    def __call__(self, doc: Doc) -> Doc:
        tok: Token
        for tok in doc:
            analyses: List[Tuple[str, str]] = self._em.stem(tok)
            ud_analyses: List[Tuple[str, str]] = [self._converter.parse(tok, ana[0], ana[1]) for ana in analyses]

            tok._.em_anas = analyses
            tok._.ud_anas = ud_analyses

            morph_dict: Dict[str, str] = tok.morph.to_dict()
            best_sim_score = 0
            for (em_lemma, em_tag), (ud_tag, ud_morph) in zip(analyses, ud_analyses):
                if ud_tag == tok.pos_:
                    emmorph_dict: Dict[str, str] = Morphology.feats_to_dict(ud_morph)
                    sim_score: float = sum(
                        emmorph_dict.get(key) == value
                        for key, value in morph_dict.items()
                    ) / (len(
                        set(morph_dict.keys()) | set(emmorph_dict.keys())
                    ) or 1 )
                    if sim_score > best_sim_score or str(tok.morph) == "" and ud_morph == "_":
                        tok._.em_tag = em_tag
                        tok._.ud_tag = ud_tag
                        tok._.em_lemma = em_lemma
                        tok._.ud_morph = MorphAnalysis(self._nlp.vocab, ud_morph)

        return doc
```

<!--
```python
try:
    import hu_core_news_lg
except ImportError:
    import huspacy
    huspacy.download("hu_core_news_lg")
    import hu_core_news_lg

nlp = hu_core_news_lg.load()
```
-->

Assuming that you've already loaded a HuSpaCy pipeline as `nlp`, the morph. analyzer can be added by issuing:

<!--pytest-codeblocks:cont-->
```python
nlp.add_pipe("emmorph")
```

Then, morph. analysis can be accessed in custom attributes of tokens. For example this simple script access all attributes

<!--pytest-codeblocks:cont-->
```python
doc = nlp("A rendőrök csak könnygázzal és gumibottal tudták megakadályozni.")

print(doc[1]._.em_lemma)
print(doc[1]._.ud_tag)
print(doc[1]._.em_tag)
print(doc[1]._.ud_morph)
print(doc[1]._.em_anas)
print(doc[1]._.ud_anas)
```

... and yields:

<!--pytest-codeblocks:expected-output-->
```
rendőr
NOUN
[/N][Pl][Nom]
Case=Nom|Number=Plur
[('rendőr', '[/N][Pl][Nom]')]
[('NOUN', 'Case=Nom|Number=Plur')]
```
