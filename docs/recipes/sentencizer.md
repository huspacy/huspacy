All models come with a machine learning based sentencizer. If by any reason, you want to rely on a rule-base one,
HuSpacy got your back as it contains a classic sentence boundary detector component.

In order to use it, you should replace the `senter` pipeline step:

```python
import huspacy

nlp = huspacy.load("hu_core_news_lg")
nlp.replace_pipe("senter", "hun_sentencizer")

```