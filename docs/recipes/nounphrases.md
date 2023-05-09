# Extracting noun phrases

Even though, spaCy's rule-based noun chunking facilities are not yet supported, you can still extract noun phrases using the Berkeley Neural Parser (`benepar`). 

## Install dependencies

First you'll need to install the tool by issuing `pip install benepar` or `pip install huspacy[np]`

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

Then, `benepar` models should be downloaded and added to a HuSpaCy pipeline:

<!--pytest-codeblocks:cont-->
```python
import benepar
import os

# Workaround for incompatible protobuf versions
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"]="python"

benepar.download('benepar_hu2')

nlp.add_pipe("benepar", config={"model": "benepar_hu2"})
```

One can use this simple method to extract maximal noun phrase:

<!--pytest-codeblocks:cont-->
```python
from spacy.tokens import Span
from typing import *

def extract_max_np(span: Span) -> Iterable[Span]:
  if "NP" in span._.labels:
    yield span
  else:
    for child in span._.children:
      yield from extract_max_np(child)
```

Then

<!--pytest-codeblocks:cont-->
```python
doc = nlp("Ők korábban népszavazási kérdéseket jelentettek be, és azt ígérik, folytatják.")

for sent in doc.sents:
  for np in extract_max_np(sent):
    print(np)
```

prints:

<!--pytest-codeblocks:expected-output-->
```
Ők
népszavazási kérdéseket
azt
```
