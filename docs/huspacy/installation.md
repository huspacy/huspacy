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

You can install the models directly from 🤗 Hugging Face Hub:

- CPU optimized [large model](https://huggingface.co/huspacy/hu_core_news_lg): `pip install hu_core_news_lg@https://huggingface.co/huspacy/hu_core_news_lg/resolve/v3.8.1/hu_core_news_lg-3.8.1-py3-none-any.whl`
- GPU optimized [transformers model](https://huggingface.co/huspacy/hu_core_news_trf): `pip install hu_core_news_trf@https://huggingface.co/huspacy/hu_core_news_trf/resolve/v3.7.1/hu_core_news_trf-3.7.1-py3-none-any.whl`

The model wheels carry their version in the filename, as `pip>=25.3` and `uv` require. The same URLs are installed with `uv`:

```console
$ uv add https://huggingface.co/huspacy/hu_core_news_lg/resolve/v3.8.1/hu_core_news_lg-3.8.1-py3-none-any.whl
```

The transformers model is published under its version tag from `3.7.1` on. Earlier versions (`3.7.0` and below) keep their versioned wheel on the `main` branch of the repository, because their release tags predate the filename change.

To speed up inference on GPU, CUDA must be installed as described in [https://spacy.io/usage](https://spacy.io/usage).

Read more on the models [here](/models)
