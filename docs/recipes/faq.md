<!--pytest-codeblocks:skipfile-->

# :octicons-question-24: Frequently asked questions

## HuSpaCy is slow, what can I do?

Not it's not. :) You have several options to speed up your processing pipeline.

1. If accuracy is not crucial use a smaller model: `md` < `lg` < `trf`
2. Utilize GPU: use the following directive **before** loading the model (and [make sure](https://spacy.io/usage#gpu) all GPU related dependencies are installer). [This simple notebook](https://colab.research.google.com/drive/1gD4OzCddbFM76yS1kWVDDbZd9rrCiho7#scrollTo=bPnMq5tGAiM7) might help you get started.
   ```python
   spacy.prefer_gpu()
   ```
3. Batch processing of multiple documents are always faster. Use the [`Language.pipe()`](https://spacy.io/api/language#pipe) method, and increase the `batch_size` if needed. Additionally, the `n_process` parameter can be used to orchestrate multiprocessing when running models on CPU.
   ```python
   texts = ["first doc", "second doc"]
   docs = nlp.pipe(texts, batch_size=1024, n_jobs=2)
      ```
4. Disable components not needed. When mining documents for named entities, the default model unnecessarily computes lemmata, PoS tags and dependency trees. You can easily disable them during model loading (c.f. [`spacy.load()`](https://spacy.io/api/top-level/#spacy.load) or [`huspacy.load()`](/reference/huspacy/__init__/#huspacy.load)) or using [`Language.disable_pipe()`](https://spacy.io/api/language/#disable_pipe)
   ```python
   nlp = huspacy.load("hu_core_news_lg", disable=["tagger"])
   ```
   or
   ```python
   nlp.disable_pipe("tagger")
   ```

## Models require too much RAM, how can I reduce their memory footprint?

HuSpaCy models use distinct language models for almost each of their components. This architecture decision enables the model achieving higher precision compromising on increased memory usage. However, if you only need certain components, others can be disabled as shown above.
   
## The NER model usually confuses ORG and LOC entities, why is that?

The underlying model has been trained on corpora following the "tag-for-meaning" guideline which yields context dependent labels. For example referring to "Budapest" in the context of the Hungarian government should yield the `ORG` label while in other contexts it should be tagged as a `LOC`.

## Can I use HuSpaCy for my commercial software?

Yes, the tool is licensed under [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) license, while all the models are [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
