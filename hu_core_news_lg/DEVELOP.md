# Model development

## Train models

1. Install dependencies: `poetry install` (CUDA 11.1 is supported out-of-the-box)
   - Run `poetry run pip install -U pip setuptools wheel` if these packages are missing or not uptodate
2. Activate the virtual environment `poetry shell`
3. Fetch datafiles: `spacy project assets -S` <br/>
   (`-S` won't retry fetch resources if they are already present)
4. Build all the models: `spacy project run all`

## Fine-tune the models

Hyperparameters of the underlying models can be fine-tuned using Weights&Biases: `wandb sweep` with one of the `sweep_*.yml` config file.

## Publish models

1. Make sure dependencies are up-to-date: `poetry update`
2. Bump version: `bumpversion --new-version x.x.x major/micro/patch --verbose`
3. Build the model as described in the previous section
4. Publish the new model to Hugging Face Hub: `poetry run spacy project run publish` (must be executed in the model's directory)
