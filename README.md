# Hungarian models for spaCy

This repository contains the building blocks and the releases of Hungarian models for [spaCy](https://spacy.io).

## Development

Training runs are tracked with [Weights & Biases](https://wandb.ai/teams/spacy-hu) while issues are managed in Trello: 
### Installing requirements

- `poetry install` will install all the dependencies
- For better performance you might need to [reinstall spacy with GPU support](https://spacy.io/usage), e.g. `poetry add spacy[cuda92]` will add support for CUDA 9.2

