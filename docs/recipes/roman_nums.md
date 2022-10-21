In case you want to use the arabic value of roman numbers, you can use one of our optional pipeline steps.

In order to process numbers, `roman_to_arabic` module should be added to the pipeline:

```python
import huspacy

nlp = huspacy.load("hu_core_news_lg")
nlp.add_pipe("roman_to_arabic")

doc = nlp("A IV. kerület Újpest.")
print(doc[1].lemma_) # Should yield "4."
```