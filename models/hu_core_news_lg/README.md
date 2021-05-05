# Syntax model


<a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>



The model builds on the [Hungarian UD treebank](https://github.com/UniversalDependencies/UD_Hungarian-Szeged), thus it is capable of predicting PoS and morphological tags, computing lemmata and predicting dependency syntax of sentences.

## Build the model

Activate the virtual environment: `poetry shell`

1. Fetch datafiles: `python -m spacy projects assets`
1. Download and transform word vectors:`python -m spacy projects run vectors`
1. Preprocess corpus: `python -m spacy projects run preprocessing`
1. Train the model `python -m spacy projects run train`
1. Create the python package`python -m spacy projects run package`

## Results
