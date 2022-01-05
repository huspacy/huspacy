# Core model


<a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>



The model builds on the [Hungarian UD treebank](https://github.com/UniversalDependencies/UD_Hungarian-Szeged) and the [NerKor corpus](https://github.com/UniversalDependencies/UD_Hungarian-Szeged), thus it is capable of predicting PoS and morphological tags, computing lemmata, providing dependency parses of sentences and marking named entities.

## Build the model

Activate the virtual environment: `poetry shell` and `cd hu_core_news_lg`

1. Fetch datafiles: `python -m spacy project assets -S` <br/>
   (`-S` won't retry fetch resources if they are already present)
2. Build all models: `python -m spacy project run all`

## Publish models and packages

1. Make sure dependencies are up-to-date: `poetry update`
2. Bump version: `bumpversion patch` / `minor` / `major`
3. Build the model as described in the previous section
4. Publish the new model to Hugging Face Hub: `python -m spacy project run all` (must be executed in the model's directory)
5. Create a new `huspacy` release by issuing: `poetry build -f wheel` (in the `huspacy` directory)
6. Upload the new release to PyPI: `poetry publish` (execute in the `huspacy` directory)




