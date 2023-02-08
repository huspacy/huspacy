# :octicons-database-24: Models overview

We provide several pretrained models:

1. [`hu_core_news_lg`](https://huggingface.co/huspacy/hu_core_news_lg) is a CNN-based large model which achieves a good
   balance between accuracy and processing speed. This default model provides tokenization, sentence splitting,
   part-of-speech tagging (UD labels w/ detailed morphosyntactic features), lemmatization, dependency parsing and named
   entity recognition and ships with pretrained word vectors.
2. [`hu_core_news_trf`](https://huggingface.co/huspacy/hu_core_news_trf) is built
   on [huBERT](https://huggingface.co/SZTAKI-HLT/hubert-base-cc) and provides the same functionality as the large model
   except the word vectors. It comes with much higher accuracy in the price of increased computational resource usage.
   We suggest using it with GPU support.
3. [`hu_core_news_md`](https://huggingface.co/huspacy/hu_core_news_md) greatly improves on `hu_core_news_lg`'s
   throughput by loosing some accuracy. This model could be a good choice when processing speed is crucial.

HuSpaCy's model versions follows [spaCy's versioning scheme](https://spacy.io/models#model-versioning).

A demo of the models is available at [Hugging Face Spaces](https://huggingface.co/spaces/huspacy/demo).

To read more about the model's architecture we suggest
reading [the relevant sections from spaCy's documentation](https://spacy.io/models#design).

### Comparison

| Models          | `md`                                                                                                                     | `lg`                                                                                             | `trf`                                                                                                                                | `trf_xl`                                                                                                                 |
|-----------------|--------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|   
| Embeddings      | 100d floret                                                                                                              | 300d floret                                                                                      | transformer:<br/>[`huBert`](https://huggingface.co/SZTAKI-HLT/hubert-base-cc)                                                        | transformer:<br/>[`xlm-roberta-large`](https://huggingface.co/xlm-roberta-large)                                         |
| Target hardware | CPU                                                                                                                      | CPU                                                                                              | GPU                                                                                                                                  | GPU                                                                                                                      |
| Accuracy        | :fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star-half-stroke:             | :fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star: | :fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star-half-stroke: | :fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star: |
| Resource usage  | :fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star: | :fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star: | :fontawesome-solid-star::fontawesome-solid-star:                                                                                     | :fontawesome-solid-star-half-stroke:                                                                                     |

