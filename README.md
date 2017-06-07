# Hungarian models for spaCy

This repository contains releases of Hungarian models for the spaCy library. For more info on how to download, install and use the models, see the [models documentation](https://spacy.io/docs/usage/models).

## Releases

| Date | Model | Spacy compatibility | Version | Features | Size | Memory consumption| License | | |
| --- | --- | --- | ---: | --- | ---: | ---: | --- | --- | --- |
| `2017-06-05` | `hu_vectors_web_lg` | 1.8=<, <2.0 | 0.1.0 | Vocabulary, Word vectors | 1.8 GB | 7G | CC BY-NC | [![][i]][i-hu_vectors_web_lg-0.1.0] | [![][dl]][hu_vectors_web_lg-0.1.0] |
| `2017-06-05` | `hu_vectors_web_md` | 1.8=<, <2.0 | 0.1.0 | Vocabulary, Word vectors | 1.0 GB | 2.9G | CC BY-NC | [![][i]][i-hu_vectors_web_lg-0.1.0] | [![][dl]][hu_vectors_web_lg-0.1.0] |

[hu_vectors_web_lg-0.1.0]: https://github.com/oroszgy/spacy-hungarian-models/releases/download/hu_vectors_web_lg-0.1.0/hu_vectors_web_lg-0.1.0.tar.gz
[i-hu_vectors_web_lg-0.1.0]: https://github.com/oroszgy/spacy-hungarian-models/releases/hu_vectors_web_lg-0.1.0

[dl]: http://i.imgur.com/gQvPgr0.png
[i]: http://i.imgur.com/OpLOcKn.png

## Downloading models

```python
pip install https://github.com/oroszgy/spacy-hungarian-models/releases/download/hu_vectors_web_md-0.1.0/hu_vectors_web_lg-0.1.0.tar.gz

# set up shortcut link to load installed package as "hu"
python -m spacy link hu_vectors_web_lg hu
```

## Loading and using models

To load a model, use `spacy.load()` with the model's shortcut link:

```python
import spacy
nlp = spacy.load('hu_vectors_web_lg')
doc = nlp(u'Sziasztok, megjöttem.')
```

If you've installed a model via pip, you can also `import` it directly and
then call its `load()` method with no arguments. This should also work for
older models in previous versions of spaCy.

```python
import spacy
import hu_vectors_web_lg

nlp = hu_vectors_web_lg.load()
doc = nlp(u'Sziasztok, megjöttem.')
```
