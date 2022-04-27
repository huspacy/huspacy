# Core vectors


<a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>

This model contains [floret](https://github.com/explosion/floret) vectors trained on the [Hungarian Webcorpus 2.0](https://hlt.bme.hu/en/resources/webcorpus2)

## Build the model

Make sure you have `gcc` and `parallel` installed.

Activate the virtual environment: `poetry shell` and `cd hu_vectors`

1. Fetch datafiles: `python -m spacy project assets -S` <br/>
   (`-S` won't retry fetch resources if they are already present)
2. Build all models: `python -m spacy project run all`
