# :octicons-database-24: Models overview

We provide several pretrained models, the ([`hu_core_news_lg`](https://huggingface.co/huspacy/hu_core_news_lg)) one is a
CNN-based large model which achieves a good balance between accuracy and processing speed.
This default model provides tokenization, sentence splitting, part-of-speech tagging (UD labels w/ detailed
morphosyntactic features), lemmatization, dependency parsing and named entity recognition and ships with pretrained word
vectors.

The second model ([`hu_core_news_trf`](https://huggingface.co/huspacy/hu_core_news_trf)) is built
on [huBERT](https://huggingface.co/SZTAKI-HLT/hubert-base-cc) and provides the same functionality as the large model
except the word vectors.
It comes with much higher accuracy in the price of increased computational resource usage. We suggest using it with GPU
support.

The [`hu_core_news_md`](https://huggingface.co/huspacy/hu_core_news_md) pipeline greatly improves on `hu_core_news_lg`'s
throughput by loosing some accuracy. This model could be a good choice when processing speed is crucial.

A demo of these models is available at [Hugging Face Spaces](https://huggingface.co/spaces/huspacy/demo).

### Comparison

| Models         | `md`                                                                                                                                                                                                                                             | `lg`                                                                                                                                                                                              | `trf`                                                                                                        |
|----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------| 
| *Embeddings*   | 100d floret                                                                                                                                                                                                                                      | 300d floret                                                                                                                                                                                       | transformer: [`huBert`](https://huggingface.co/SZTAKI-HLT/hubert-base-cc)                                    |
| Target hardwer | CPU                                                                                                                                                                                                                                              | CPU                                                                                                                                                                                               | GPU                                                                                                          |
| Accuracy       | :fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star-half-stroke:                                                                                                                                     | :fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star:                                                                                                  | :fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star-half-stroke: |
| Resource usage | :fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star:  | :fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star::fontawesome-solid-star:  | :fontawesome-solid-star::fontawesome-solid-star:                                                             |

