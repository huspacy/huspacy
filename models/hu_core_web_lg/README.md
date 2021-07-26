# Core model

<a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>



The model builds on the [NerKor corpus](https://github.com/UniversalDependencies/UD_Hungarian-Szeged), thus it is capable of predicting PoS and morphological tags, computing lemmata and extracting named entities.

## Build the model

Activate the virtual environment: `poetry shell`

1. Fetch datafiles: `python -m spacy project assets -S` <br/>
   (`-S` won't retry fetch resources if they are already present)
1. Download and transform word vectors:`python -m spacy project run vectors`
1. Preprocess corpus: `python -m spacy project run preprocess`
1. Train the model `python -m spacy project run train`
1. Create the python package`python -m spacy project run package`

## Results
