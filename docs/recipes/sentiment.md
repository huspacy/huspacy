# :material-heart-half: Matching sentiment lexicons

HuSpaCy is shipped with two sentiment lexicons. 
The component loads up a lexicon and match words with it. 
The module can use two sentiment lexicons, the default one is the [PolText Lab's resource](https://github.com/poltextlab/sentiment_hun) 
while one can also load the [PrecoSenti](https://opendata.hu/dataset/hungarian-sentiment-lexicon) lexicon.

## Load the component

```python
import huspacy
import huspacy.integrations

# Load the default lexicon
nlp = huspacy.load("hu_core_news_lg")
nlp.add_pipe("sentiment_lexicon")

# Load a specific lexicon
nlp = huspacy.load("hu_core_news_lg")
nlp.add_pipe("sentiment_lexicon", config={"lexicon_id": "precognox"})
```

## Extract sentiment values

```python
doc = nlp("Ez szuper jó")

print(doc.spans["sentiment"])  # ["szuper", "jó"]

print(doc[1]._.sentiment)  # 'POS'
print(doc[2]._.sentiment)  # 'POS'

```