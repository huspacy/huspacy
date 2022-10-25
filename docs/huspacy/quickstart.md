# # :octicons-command-palette-24: Quicstart
HuSpaCy is fully compatible with [spaCy's API](https://spacy.io/api/doc/), newcomers can easily get started with [spaCy 101](https://spacy.io/usage/spacy-101) guide.

Although HuSpacy models can be loaded with `spacy.load(...)`, the tool provides convenience methods to easily access downloaded models.

```python
# Load the model using spacy.load(...)
import spacy
nlp = spacy.load("hu_core_news_lg")
```

```python
# Load the default large model (if downloaded)
import huspacy
nlp = huspacy.load()
```

```python
# Load the model directly as a module
import hu_core_news_lg
nlp = hu_core_news_lg.load()
```

To process texts, you can simply call the loaded model (i.e. the [`nlp` callable object](https://spacy.io/api/language#call)) 

```python
doc = nlp("Csiribiri csiribiri zabszalma - négy csillag közt alszom ma.")
```

As HuSpaCy is built on spaCy, the returned [`doc` document](https://spacy.io/api/doc#_title) contains all the annotations given by the pipeline components.
