# Hungarian models for spaCy

This repository contains releases of Hungarian models for the spaCy library. For more info on how to download, install and use the models, see the [models documentation](https://spacy.io/docs/usage/models).

## Releases

| Date | Model | Version | Spacy version | Features | Size | Memory | License | Info | Get |
| --- | --- | --- | ---: | --- | ---: | ---: | --- | --- | --- |
| 2018-12-30 | `hu_core_ud_lg` | `0.1.0` | >=2.0.0,<2.1.0 | Word vectors, Brown clusters, Token frequencies, PoS Tagger, Lemmatizer, Dependency parser | 1.8G | 7G | <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a> | [![][i]][i-hu_core_ud_lg-0.1.0] | [![][dl]][hu_core_ud_lg-0.1.0]

[hu_core_ud_lg-0.1.0]: https://github.com/oroszgy/spacy-hungarian-models/releases/download/hu_vectors_web_lg-0.1.0/hu_core_ud_lg-0.1.0-py3-none-any.whl
[i-hu_core_ud_lg-0.1.0]: https://github.com/oroszgy/spacy-hungarian-models/releases/hu_core_ud_lg-0.1.0


[dl]: http://i.imgur.com/gQvPgr0.png
[i]: http://i.imgur.com/OpLOcKn.png

## Install

```bash
pip install https://github.com/oroszgy/spacy-hungarian-models/releases/download/hu_core_ud_lg-0.1.0/hu_core_ud_lg-0.1.0.tar.gz

# Optionally set up shortcut link to load installed package as "hu"
python -m spacy link hu_core_ud_lg hu
```

## Usage

To load a model, use `spacy.load()` method with the model's name:

```python
import spacy
nlp = spacy.load('hu_core_ud_lg')
doc = nlp('Sziasztok, megjöttem.')
```

If you've installed a model via pip, you can also `import` the model's package directly and
call its `load()` method with no arguments.

```python
import hu_core_ud_lg

nlp = hu_core_ud_lg.load()
doc = nlp('Sziasztok, megjöttem.')
```
