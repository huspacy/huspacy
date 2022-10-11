<div align="center">
    <br>
    <img src="https://raw.githubusercontent.com/huspacy/huspacy/develop/.github/resources/logo.png" width="333" alt="HuSpaCy: Industrial strength Hungarian NLP"/>
    <hr/>
</div>
<div align="center">

[![python version](https://img.shields.io/badge/Python-%3E=3.7-blue)](https://github.com/huspacy/huspacy)
[![spacy](https://img.shields.io/badge/built%20with-spaCy-09a3d5.svg)](https://spacy.io)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/huspacy)
[![PyPI version](https://badge.fury.io/py/huspacy.svg)](https://pypi.org/project/huspacy/)
[![license: Apache-2.0](https://img.shields.io/github/license/huspacy/huspacy)](https://github.com/huspacy/huspacy/blob/master/LICENSE)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
<br/>
[![Demo](https://img.shields.io/badge/Try%20the-Demo-important)](https://huggingface.co/spaces/huspacy/demo)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fhuspacy%2Fhuspacy&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=true)](https://hits.seeyoufarm.com)
[![pip downloads](https://img.shields.io/pypi/dm/huspacy.svg)](https://pypi.org/project/huspacy/)
[![stars](https://img.shields.io/github/stars/huspacy/huspacy?style=social)](https://github.com/huspacy/huspacy)
</div>

HuSpaCy is a [spaCy](https://spacy.io) library providing industrial-strength Hungarian language processing facilities through spaCy models. 
The released pipelines consist of a tokenizer, sentence splitter, lemmatizer, tagger (predicting morphological features as well), dependency parser and a named entity recognition module. 
Word and phrase embeddings are also available through spaCy's API.
All models have high throughput, decent memory usage and close to state-of-the-art accuracy. 
A live demo is available [here](https://huggingface.co/spaces/huspacy/demo), model releases are published to [Hugging Face Hub](https://huggingface.co/huspacy/). 

This repository contains material to build HuSpaCy and all of its models in a reproducible way.

## Available Models 

We provide two models, the first one is a CNN-based large model which achieves a good balance between accuracy and processing speed.
This default model ([`hu_core_news_lg`](https://huggingface.co/huspacy/hu_core_news_lg)) provides tokenization, sentence splitting, part-of-speech tagging (UD labels w/ detailed morphosyntactic features), lemmatization, dependency parsing and named entity recognition and ships with pretrained word vectors.

The second model ([`hu_core_news_trf`](https://huggingface.co/huspacy/hu_core_news_trf)) is built on [huBERT](https://huggingface.co/SZTAKI-HLT/hubert-base-cc) and provides the same functionality as the large model except the word vectors. 
It comes with much higher accuracy in the price of increased computational resource usage. We suggest using it with GPU support.

A demo of these models is available at [Hugging Face Spaces](https://huggingface.co/spaces/huspacy/demo).
Models' changes are recorded in respective changelog files. ([`lg`](hu_core_news_lg/CHANGELOG.md), [`trf`](hu_core_news_trf/CHANGELOG.md), [`vectors`](hu_vectors_web_lg/CHANGELOG.md))

## Installation

To get started using the tool, first, we need to download one of the models. The easiest way to achieve this is to install `huspacy` (from [PyPI](https://pypi.org/project/huspacy/)) and then fetch a model through its API.

```bash
pip install huspacy
```

```python
import huspacy

# Download the latest CPU optimized model
huspacy.download()
```

You can install the latest models directly from 🤗 Hugging Face Hub:
   - CPU optimized [large model](https://huggingface.co/huspacy/hu_core_news_lg): `pip install https://huggingface.co/huspacy/hu_core_news_lg/resolve/main/hu_core_news_lg-any-py3-none-any.whl`
   - GPU optimized [transformers model](https://huggingface.co/huspacy/hu_core_news_trf): `pip install https://huggingface.co/huspacy/hu_core_news_trf/resolve/main/hu_core_news_trf-any-py3-none-any.whl`

To speed up inference on GPUs, CUDA should be installed as described in [https://spacy.io/usage](https://spacy.io/usage).


## Usage

HuSpaCy is fully compatible with [spaCy's API](https://spacy.io/api/doc/), newcomers can easily get started with [spaCy 101](https://spacy.io/usage/spacy-101) guide. 

Although HuSpacy models can be loaded with `spacy.load(...)`, the tool provides convenience methods to easily access downloaded models.
```python
# Load the model using spacy.load(...)
import spacy
nlp = spacy.load("hu_core_news_lg")

# Load the default large model (if downloaded)
import huspacy
nlp = huspacy.load()

# Load the model directly as a module
import hu_core_news_lg
nlp = hu_core_news_lg.load()

# Process texts
doc = nlp("Csiribiri csiribiri zabszalma - négy csillag közt alszom ma.")
```
API Documentation is available in the [project wiki](https://github.com/huspacy/huspacy/wiki).

## Development
 
Each model has its own dependency structure managed by `poetry`. For details check the models' readmes ([`lg`](hu_core_news_lg/README.md), [`trf`](hu_core_news_trf/README.md), [`vectors`](hu_vectors/README.md)).

### Repository structure

```
├── .github            -- Github configuration files
├── hu_core_news_lg    -- SpaCy 3.x project files for building the large model
│   ├── configs        -- SpaCy pipeline configuration files
│   ├── meta.json      -- model metadata
│   ├── poetry.lock    -- Poetry lock file
│   ├── poetry.toml    -- Poetry configs
│   ├── project.lock   -- Auto-generated project script
│   ├── project.yml    -- SpaCy Project file describing steps needed to build the model
│   ├── pyproject.toml -- Python project definition file
│   ├── CHANGELOG.md   -- Model changelog
│   └── README.md      -- Instructions on building a model from scratch
├── hu_core_news_trf   -- Spacy 3.x project files for building the transformer based model
│   ├── configs        -- SpaCy pipeline configuration files
│   ├── meta.json      -- model metadata
│   ├── poetry.lock    -- Poetry lock file
│   ├── poetry.toml    -- Poetry configs
│   ├── project.lock   -- Auto-generated project script
│   ├── project.yml    -- SpaCy Project file describing steps needed to build the model
│   ├── pyproject.toml -- Python project definition file
│   ├── CHANGELOG.md   -- Model changelog
│   └── README.md      -- Instructions on building a model from scratch
├── hu_vectors_web_lg  -- Spacy 3.x project files for building word vectors
│   ├── configs        -- SpaCy pipeline configuration files
│   ├── poetry.lock    -- Poetry lock file
│   ├── poetry.toml    -- Poetry configs
│   ├── project.lock   -- Auto-generated project script
│   ├── project.yml    -- SpaCy Project file describing steps needed to build the model
│   ├── pyproject.toml -- Python project definition file
│   ├── CHANGELOG.md   -- Model changelog
│   └── README.md      -- Instructions on building a model from scratch
├── huspacy            -- subproject for the PyPI distributable package
│   ├── huspacy        -- huspacy python package
│   ├── test           -- huspacy tests
│   ├── poetry.lock    -- Poetry lock file
│   ├── poetry.toml    -- Poetry configs
│   ├── pyproject.toml -- Python project definition file
│   ├── CHANGELOG.md   -- HuSpaCy changelog
│   └── README.md      -> ../README.md
├── scripts            -- CLI scripts
├── LICENSE            -- License file
└── README.md          -- This file

```

## Citing

If you use the models or this library in your research please cite this [paper](https://arxiv.org/abs/2201.01956).</br>
Additionally, please indicate the version of the model you used so that your research can be reproduced.


```bibtex
@misc{HuSpaCy:2021,
  title = {{HuSpaCy: an industrial-strength Hungarian natural language processing toolkit}},
  booktitle = {{XVIII. Magyar Sz{\'a}m{\'\i}t{\'o}g{\'e}pes Nyelv{\'e}szeti Konferencia}},
  author = {Orosz, Gy{\"o}rgy and Sz{\' a}nt{\' o}, Zsolt and Berkecz, P{\' e}ter and Szab{\' o}, Gerg{\H o} and Farkas, Rich{\' a}rd}, 
  location = {{Szeged}},
  year = {2022},
}
```

## License

This library is released under the [Apache 2.0 License](https://github.com/huspacy/huspacy/blob/master/LICENSE)

Trained models have their own license ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)) as described on the [models page](https://huggingface.co/huspacy/).

## Contact
For feature request issues and bugs please use the [GitHub Issue Tracker](https://github.com/huspacy/huspacy/issues). Otherwise, please use the [Discussion Forums](https://github.com/huspacy/huspacy/discussions).

## Authors

HuSpaCy is implemented in the [SzegedAI](https://szegedai.github.io/) team, coordinated by [Orosz György](mailto:gyorgy@orosz.link) in the [Hungarian AI National Laboratory, MILAB](https://mi.nemzetilabor.hu/) program.
