# :octicons-package-dependencies-24: Installation

To get started using the tool, first, we need to download one of the models. The easiest way to achieve this is to install `huspacy` (from [PyPI](https://pypi.org/project/huspacy/)) and then fetch a model through its API.

```bash
pip install huspacy
```

```python
import huspacy

# Download the latest CPU optimized model
huspacy.download()
```

### Install the models directly

You can install the latest models directly from 🤗 Hugging Face Hub:

- CPU optimized [large model](https://huggingface.co/huspacy/hu_core_news_lg): `pip install https://huggingface.co/huspacy/hu_core_news_lg/resolve/main/hu_core_news_lg-any-py3-none-any.whl`
- GPU optimized [transformers model](https://huggingface.co/huspacy/hu_core_news_trf): `pip install https://huggingface.co/huspacy/hu_core_news_trf/resolve/main/hu_core_news_trf-any-py3-none-any.whl`

To speed up inference on GPUs, CUDA should be installed as described in [https://spacy.io/usage](https://spacy.io/usage).

Read more on the models [here](/models)
