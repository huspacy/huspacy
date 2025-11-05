# Model development

## Train models

1. Install dependencies: `uv sync` (CUDA 13.0 is supported out-of-the-box)
2. Fetch datafiles: `uv run spacy project assets`
3. Build all the models: `GPU=1 uv run spacy project run all`

## Fine-tune the models

Hyperparameters of the underlying models can be fine-tuned using Weights&Biases: `wandb sweep` with one of the `sweep_*.yml` config file.

## Publish models

1. Make sure dependencies are up-to-date
2. Bump version: `bumpversion --new-version x.x.x major/micro/patch --verbose`
3. Build the model as described in the previous section
4. Publish the new model to Hugging Face Hub: `uv run spacy project run publish` (must be executed in the model's directory)
