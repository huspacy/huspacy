# Large model


<a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>



The model builds on the [Hungarian UD treebank](https://github.com/UniversalDependencies/UD_Hungarian-Szeged) and the [NerKor corpus](https://github.com/UniversalDependencies/UD_Hungarian-Szeged), thus it is capable of predicting PoS and morphological tags, computing lemmata, providing dependency parses of sentences and marking named entities. 

## Train models

1. Install dependencies: `poetry install` To enable GPU support you need to install `cupy` and `torch`. For CUDA 11.1 issue:
    - `poetry run python -m pip install cupy-cuda111`
    - `poetry run python -m pip install torch==1.9.0+cu111 -f https://download.pytorch.org/whl/torch_stable.html`
2. Activate the virtual environment `poetry shell`
3. Fetch datafiles: `spacy project assets -S` <br/>
   (`-S` won't retry fetch resources if they are already present)
4. Build all the models: `spacy project run all`

## Fine-tune the models

Hyperparameters of the underlying models can be fine-tuned using Weights&Biases: `wandb sweep` with one of the `sweep_*.yml` config file.

## Publish models

1. Make sure dependencies are up-to-date: `poetry update`
2. Bump version: `bumpversion patch` / `minor` / `major`
3. Build the model as described in the previous section
4. Publish the new model to Hugging Face Hub: `python -m spacy project run publish` (must be executed in the model's directory)
