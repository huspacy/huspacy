# DBpedia Spotlight

Using the DBpedia Spotlight integration for SpaCy[¹], we can easily extract and link DBpedia entities from any text.

## Initalizing DBpedia Spotlight

```python
nlp = spacy.load("hu_core_news_trf")
nlp.add_pipe("dbpedia_spotlight", config={'dbpedia_rest_endpoint': 'https://dbpedia-spotlight.dsd.sztaki.hu/hu', 'overwrite_ents': False})
```

## Presenting the entities

```python
doc = nlp("A Mátrix című sci-fi film Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Joe Pantoliano és Hugo Weaving főszereplésével.")
pd.DataFrame([
    {"Text": ent.text, 
    "Resource": ent.kb_id_, 
    "Similarity Score": ent._.dbpedia_raw_result['@similarityScore']}
     for ent in doc.spans["dbpedia_spotlight"]])
```

This example is available on [Hugging Face Spaces](https://huggingface.co/spaces/huspacy/example-applications), while the full source code is on [GitHub](https://github.com/huspacy/example-applications/blob/main/examples/dbpedia.py).

[¹]: https://github.com/MartinoMensio/spacy-dbpedia-spotlig[](anonymizer.md)ht