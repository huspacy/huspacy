# Hungarian models for spaCy

This repository contains the building blocks and the releases of Hungarian models for [spaCy](https://spacy.io).

## Development
 
### Installing requirements

- `poetry install` will install all the dependencies
- For better performance you might need to [reinstall spacy with GPU support](https://spacy.io/usage), e.g. `poetry add spacy[cuda92]` will add support for CUDA 9.2 (`poetry run poe cuda92`)

### Repository structure

```
├── data               -- Spacy 3.x project files for building a model for news texts
│   ├── external       -- External models required to train models (e.g. word vectors)
│   ├── processed      -- Processed data ready to feed spacy
│   └── raw            -- Raw corpora being transformed
├── hu_core_news_lg    -- Spacy 3.x project files for building a model for news texts
├── huspacy            -- Source package
│   └── cli            -- Command line scripts (Python)
├── models             -- Trained models and related metadata
├── scripts            -- Bash scripts
├── LICENSE            -- License file
├── poetry.lock        -- Locked poetry dependencies files
├── poetry.toml        -- Poetry configurations
├── pyproject.toml     -- Python project configutation, including dependencies managed with Poetry 
├── README.md          -- This file
└── resources          -- Resources
```

Each model directory has the same structure

```
├── configs                    -- Configuration files 
│   └── default.cfg      -- The default configuration file
├── project.lock               -- Auto-generated project script
├── project.yml                -- Spacy3 Project file describing steps needed to build the model
└── README.md                  -- Instructions on building a model from scratch

```