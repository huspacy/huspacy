[![python version](https://img.shields.io/badge/Python-%3E=3.7-blue)](https://github.com/spacy-hu/spacy-hungarian-models)
[![license](https://img.shields.io/github/license/spacy-hu/spacy-hungarian-models)](https://github.com/centre-for-humanities-computing/DaCy/blob/main/LICENSE)
[![spacy](https://img.shields.io/badge/built%20with-spaCy-09a3d5.svg)](https://spacy.io)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fspacy-hu%2Fspacy-hungarian-models&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=true)](https://hits.seeyoufarm.com)
[![stars](https://img.shields.io/github/stars/spacy-hu/spacy-hungarian-models?style=social)](https://github.com/spacy-hu/spacy-hungarian-models)


# HuSpacy - Hungarian models for spaCy

This repository contains the building blocks and releases of the Hungarian models for [spaCy](https://spacy.io).

## Installation

To get started using the latest Hungarian model, simply install is using pip:

```bash
pip install https://huggingface.co/spacy-hu/hu_core_news_lg/resolve/main/hu_core_news_lg-any-py3-none-any.whl
```

To speed up inference, you might want to run the models on GPU for which you need to add CUDA support for spacy as described in [here](https://spacy.io/usage).

## Usage

```python
# Load the mode using spacy.load().
import spacy
nlp = spacy.load("hu_core_news_lg")

# Or load the model importing as module.
import hu_core_news_lg
nlp = hu_core_news_lg.load()

## Start processing your texts.
doc = nlp('Csiribiri csiribiri zabszalma - négy csillag közt alszom ma.')
```

For a detailed guide on usgae, check [spaCy's documentation](https://spacy.io/usage/linguistic-features).

## Available Models 

Currently, we only support a single large model which has a good balance between accuracy and speed. 

[`hu_core_news_lg`](https://huggingface.co/spacy-hu/hu_core_news_lg) provides tokenization, sentence splitting, part-of-speech tagging (UD labels w/ detailed morphosyntactic features), lemmatization, dependency parsing and named entity recognition and ships with pretrained word vectors.

Models' changes are recorded in the [changelog](https://github.com/spacy-hu/spacy-hungarian-models/blob/master/CHANGELOG.md).

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
│   ├── project.lock               -- Auto-generated project script
│   ├── project.yml                -- Spacy3 Project file describing steps needed to build the model
│   └── README.md                  -- Instructions on building a model from scratch
├── huspacy            -- Source package
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

<!--
```bibtex
@misc{HuSpaCy:2021,
  title = {{HuSpaCy: industrial strength Hungarian natural language processing}},
  booktitle = {{XVIII. Magyar Sz\'{a}m\'{\i}t\'{o}g\'{e}pes Nyelv\'{e}szeti Konferencia}},
  author = {Orosz, Gy\"{o}rgy and Sz\'{a}nt\'{o}, Zsolt and Berkecz, Péter and Szabó, Gergő and Tóth, Bálint and Farkas, Rich\'{a}rd}, 
  year = {forthcoming 2021},
}
```
-->

## License

This library is released under the Apache 2.0 License. See the [`LICENSE`](https://github.com/spacy-hu/spacy-hungarian-models/blob/master/LICENSE) file for more details.

The trained models have their own license as described on the [models hub](https://huggingface.co/spacy-hu/hu_core_news_lg).

## Contact
For feature request issues and bugs please use the [GitHub Issue Tracker](https://github.com/spacy-hu/spacy-hungarian-models/issues). Otherwise, please use the [Discussion Forums](https://github.com/spacy-hu/spacy-hungarian-models/discussions).

## Acknowledgments

The project was supported by the Ministry of Innovation and Technology NRDI Office within the framework of the Artificial Intelligence National Laboratory Program.
