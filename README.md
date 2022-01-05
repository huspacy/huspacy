
[![python version](https://img.shields.io/badge/Python-%3E=3.7-blue)](https://github.com/huspacy/huspacy)
[![spacy](https://img.shields.io/badge/built%20with-spaCy-09a3d5.svg)](https://spacy.io)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/huspacy)
[![PyPI version](https://badge.fury.io/py/huspacy.svg)](https://pypi.org/project/huspacy/)
[![license: Apache-2.0](https://img.shields.io/github/license/huspacy/huspacy)](https://github.com/huspacy/huspacy/blob/master/LICENSE)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fspacy-hu%2Fspacy-hungarian-models&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=true)](https://hits.seeyoufarm.com)
[![pip downloads](https://img.shields.io/pypi/dm/huspacy.svg)](https://pypi.org/project/huspacy/)
[![Demo](https://img.shields.io/badge/Try%20the-Demo-important)](https://huggingface.co/spaces/huspacy/demo)
[![stars](https://img.shields.io/github/stars/huspacy/huspacy?style=social)](https://github.com/huspacy/huspacy)


# HuSpaCy: Industrial-strength Hungarian NLP

HuSpaCy is a [spaCy](https://spacy.io) model and a library providing industrial-strength Hungarian language processing facilities. 
The released pipeline consists of a tokenizer, sentence splitter, lemmatizer, tagger (predicting morphological features as well), dependency parser and a named entity recognition module. 
Word and phrase embeddings are also available through spaCy's API.
All models have high throughput, decent memory usage and close to state-of-the-art accuracy. 
A live demo is available [here](https://huggingface.co/spaces/huspacy/demo), model releases are published to [Hugging Face Hub](https://huggingface.co/huspacy/hu_core_news_lg). 

This repository contains material to build HuSpaCy's models from the ground up.

## Installation

To get started using the tool, first, you need to do download the model. The easiest way to achieve this is fetch the model by installing the `huspacy` package from PyPI:

```bash
pip install huspacy
```

This utility package exposes convenience methods for downloading and using the latest model:

```python
import huspacy

# Download the latest model
huspacy.download()

# Download the specified model 
huspacy.download(version="v0.4.1")

# Load the previously downloaded model (hu_core_news_lg)
nlp = huspacy.load()
```

Alternatively, one can install the latest model from Hugging Face Hub directly:

```bash
pip install https://huggingface.co/huspacy/hu_core_news_lg/resolve/main/hu_core_news_lg-any-py3-none-any.whl
```

To speed up inference using GPUs, CUDA support can be installed as described in [https://spacy.io/usage](https://spacy.io/usage).

## Usage

HuSpaCy is fully compatible with [spaCy's API](https://spacy.io/api/doc/), newcomers can easily get started using [spaCy 101](https://spacy.io/usage/spacy-101) guide. 

Although HuSpacy models can be leaded with `spacy.load()`, the tool provides convenience methods to easily access downloaded models.
```python
# Load the model using huspacy
import huspacy
nlp = huspacy.load()

# Load the mode using spacy.load()
import spacy
nlp = spacy.load("hu_core_news_lg")

# Load the model directly as a module
import hu_core_news_lg
nlp = hu_core_news_lg.load()

# Either way you get the same model and can start processing texts.
doc = nlp("Csiribiri csiribiri zabszalma - négy csillag közt alszom ma.")
```

## Available Models 

Currently, we provide a single large model which achieves a good balance between accuracy and processing speed. A demo of this model is available at [Hugging Face Spaces](https://huggingface.co/spaces/huspacy/demo).
This default model ([`hu_core_news_lg`](https://huggingface.co/huspacy/hu_core_news_lg)) provides tokenization, sentence splitting, part-of-speech tagging (UD labels w/ detailed morphosyntactic features), lemmatization, dependency parsing and named entity recognition and ships with pretrained word vectors.

Models' changes are recorded in the [changelog](https://github.com/huspacy/huspacy/blob/master/CHANGELOG.md).

## Development
 
### Installing requirements

- `poetry install` will install all the dependencies
- For better performance you might need to [reinstall spacy with GPU support](https://spacy.io/usage), e.g. `poetry add spacy[cuda92]` will add support for CUDA 9.2 

### Repository structure

```
├── .github            -- Github configuration files
├── data               -- Data files
│   ├── external       -- External models required to train models (e.g. word vectors)
│   ├── processed      -- Processed data ready to feed spacy
│   └── raw            -- Raw data, mostly corpora as they are obtained from the web
├── hu_core_news_lg    -- Spacy 3.x project files for building a model for news texts
│   ├── configs        -- Spacy pipeline configuration files
│   ├── project.lock   -- Auto-generated project script
│   ├── project.yml    -- Spacy3 Project file describing steps needed to build the model
│   └── README.md      -- Instructions on building a model from scratch
├── huspacy            -- subproject for the PyPI distributable package
├── tools              -- Source package for tools
│   └── cli            -- Command line scripts (Python)
├── models             -- Trained models and their metadata
├── resources          -- Resource files
├── scripts            -- Bash scripts
├── tests              -- Test files 
├── CHANGELOG.md       -- Keeps the changelog
├── LICENSE            -- License file
├── poetry.lock        -- Locked poetry dependencies files
├── poetry.toml        -- Poetry configurations
├── pyproject.toml     -- Python project configutation, including dependencies managed with Poetry 
└── README.md          -- This file
```

## Citing

If you use the models or this library in your research please cite this [paper]().</br>
Additionally, please indicate the version of the model you used so that your research can be reproduced.


```bibtex
@misc{HuSpaCy:2021,
  title = {{HuSpaCy: industrial strength Hungarian natural language processing}},
  booktitle = {{XVIII. Magyar Sz{\'a}m{\'\i}t{\'o}g{\'e}pes Nyelv{\'e}szeti Konferencia}},
  author = {Orosz, Gy{\"o}rgy and Sz{\' a}nt{\' o}, Zsolt and Berkecz, P{\' e}ter and Szab{\' o}, Gerg{\H o} and Farkas, Rich{\' a}rd}, 
  year = {in press 2021},
}
```

## License

This library is released under the [Apache 2.0 License](https://github.com/huspacy/huspacy/blob/master/LICENSE)

The trained models have their own license ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-nc/4.0/)) as described on the [models page](https://huggingface.co/huspacy/hu_core_news_lg).

## Contact
For feature request issues and bugs please use the [GitHub Issue Tracker](https://github.com/huspacy/huspacy/issues). Otherwise, please use the [Discussion Forums](https://github.com/huspacy/huspacy/discussions).

## Authors

HuSpaCy is implemented in the [SzegedAI](https://szegedai.github.io/) team, coordinated by [Orosz György](mailto:gyorgy@orosz.link) in the [Hungarian AI National Laboratory, MILAB](https://mi.nemzetilabor.hu/) program.
