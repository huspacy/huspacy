# :material-heart-half: Matching sentiment lexicons

HuSpaCy is shipped with two sentiment lexicons. 
The component loads up a lexicon and match words with it. 
The module can use two sentiment lexicons, the default one is the [PolText Lab's resource](https://github.com/poltextlab/sentiment_hun) 
while one can also load the [PrecoSenti](https://opendata.hu/dataset/hungarian-sentiment-lexicon) lexicon.

## Load the component

<!--
```python
from spacy.lang.hu import Hungarian

nlp = Hungarian()
```
-->

Load the default sentiment lexicon (`poltext`)

<!--pytest-codeblocks:cont-->
```python
import huspacy.integrations

nlp.add_pipe("sentiment_lexicon")
```

Or you can specify the lexicon to be used by passing addition configuration during initialization `nlp.add_pipe("sentiment_lexicon", config={"lexicon_id": "precognox"})
`.

Then you can start discovering sentiment values of spans and tokens:

<!--pytest-codeblocks:cont-->
```python
doc = nlp("Ez szuper jó")

print(doc.spans["sentiment"])  # ["szuper", "jó"]

print(doc[1]._.sentiment)  # 'POS'
print(doc[2]._.sentiment)  # 'POS'

```