# Hungarian models for spaCy

This repository contains releases of Hungarian models for the spaCy library. For more info on how to download, install and use the models, see the [models documentation](https://spacy.io/docs/usage/models).

**All the models are experimental, consider them as pre-release alphas.**

## Releases

| Date | Model | Version | Spacy version | Features | Size | Memory | License | Info | Get |
| --- | --- | --- | ---: | --- | ---: | ---: | --- | --- | --- |
| 2017-06-05 | `hu_vectors_web_lg` | `0.1.0` |>=1.8, <2.0 | Vocabulary, Brown clusters, Token frequencies, Word vectors | 1.8G | 7G | <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a> | [![][i]][i-hu_vectors_web_lg-0.1.0] | [![][dl]][hu_vectors_web_lg-0.1.0] 
| 2017-06-07 | `hu_vectors_web_md` | `0.1.0` | >=1.8, <2.0 | Vocabulary, Brown clusters, Token frequencies, Word vectors | 1.0G | 2.9G | <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a> | [![][i]][i-hu_vectors_web_md-0.1.0] | [![][dl]][hu_vectors_web_md-0.1.0] 
| 2017-06-11 | `hu_tagger_web_md` | `0.1.0` | >=1.8, <2.0 | PoS Tagger, Vocabulary, Brown clusters, Token frequencies, Word vectors | 1.0G | >2.9G | <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/3.0//88x31.png" /></a> | [![][i]][i-hu_tagger_web_md-0.1.0] | [![][dl]][hu_tagger_web_md-0.1.0] 

[hu_vectors_web_lg-0.1.0]: https://github.com/oroszgy/spacy-hungarian-models/releases/download/hu_vectors_web_lg-0.1.0/hu_vectors_web_lg-0.1.0.tar.gz
[i-hu_vectors_web_lg-0.1.0]: https://github.com/oroszgy/spacy-hungarian-models/releases/hu_vectors_web_lg-0.1.0

[hu_vectors_web_md-0.1.0]: https://github.com/oroszgy/spacy-hungarian-models/releases/download/hu_vectors_web_md-0.1.0/hu_vectors_web_md-0.1.0.tar.gz
[i-hu_vectors_web_md-0.1.0]: https://github.com/oroszgy/spacy-hungarian-models/releases/hu_vectors_web_md-0.1.0

[hu_tagger_web_md-0.1.0]: https://github.com/oroszgy/spacy-hungarian-models/releases/download/hu_tagger_web_md-0.1.0/hu_tagger_web_md-0.1.0.tar.gz
[i-hu_tagger_web_md-0.1.0]: https://github.com/oroszgy/spacy-hungarian-models/releases/hu_tagger_web_md-0.1.0


[dl]: http://i.imgur.com/gQvPgr0.png
[i]: http://i.imgur.com/OpLOcKn.png

## Downloading models

```python
pip install https://github.com/oroszgy/spacy-hungarian-models/releases/download/hu_tagger_web_md-0.1.0/hu_tagger_web_md-0.1.0.tar.gz

# set up shortcut link to load installed package as "hu"
python -m spacy link hu_tagger_web_md hu
```

## Loading and using models

To load a model, use `spacy.load()` with the model's shortcut link:

```python
import spacy
nlp = spacy.load('hu_tagger_web_md')
doc = nlp(u'Sziasztok, megjöttem.')
```

If you've installed a model via pip, you can also `import` it directly and
then call its `load()` method with no arguments. This should also work for
older models in previous versions of spaCy.

```python
import spacy
import hu_tagger_web_md

nlp = hu_tagger_web_md.load()
doc = nlp(u'Sziasztok, megjöttem.')
```
