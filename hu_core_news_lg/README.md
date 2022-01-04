# Core model


<a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>



The model builds on the [Hungarian UD treebank](https://github.com/UniversalDependencies/UD_Hungarian-Szeged) and the [NerKor corpus](https://github.com/UniversalDependencies/UD_Hungarian-Szeged), thus it is capable of predicting PoS and morphological tags, computing lemmata, providing dependency parses of sentences and marking named entities.

## Build the model

Activate the virtual environment: `poetry shell`

1. Fetch datafiles: `python -m spacy project assets -S` <br/>
   (`-S` won't retry fetch resources if they are already present)
2. Download and transform word vectors:`python -m spacy project run convert_vectors`
3. Preprocess the UD corpus: `python -m spacy project run preprocess_ud`
4. Preprocess the NerKor corpus: `python -m spacy project run preprocess_nerkor`
5. Preprocess the Szeged corpus: `python -m spacy project run preprocess_szegedcorpus`
6. Train the tagger / parser model `python -m spacy project run train_praser`
7. Train the lemmatizer `python -m spacy project run train_lemmatizer`
8. Train the NER `python -m spacy project run train_ner`




