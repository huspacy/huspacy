# Keyphrase Extraction

Keyphrase extraction is a well-studied problem of natural language processing, thus many ready-made solutions exist. `textacy` is higher-level NLP library (built on spaCy) implementing several keyword extraction methods. By using this tool, we can easily build a simple solution for this problem.

First, you need to load a HuSpaCy model, and process the text you wish to analyze:

```python
import huspacy

nlp = huspacy.load()

doc = nlp(text)
```

Then, you need to decide which key term extraction method should be utilized, as `textacy` implements [several ones](https://textacy.readthedocs.io/en/0.11.0/api_reference/extract.html). For the sake of simplicity we rely on [SGRank](https://aclanthology.org/S15-1013.pdf) and fine-tune it through PoS and word n-gram filters.

```python
from textacy.extract.keyterms.sgrank import sgrank as keywords

terms: List[Tuple[str, float]] = keywords(doc, topn=10, include_pos=("NOUN", "PROPN"),  ngrams=(1, 2, 3))
```

This example is available on [Hugging Face Spaces](https://huggingface.co/spaces/huspacy/example-applications), while the full source code is on [GitHub](https://github.com/huspacy/example-applications/blob/main/examples/keyphrases.py).