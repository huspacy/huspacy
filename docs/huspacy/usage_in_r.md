# :octicons-arrow-switch-24: Usage in R

## Recommended installation method

<!--pytest-codeblocks:skipfile-->

1. Make sure you have conda installed
2. Install `spacyr`:
    ```R
    install.packages("spacyr")
    library("spacyr")
    spacy_install()
     ```
3. Install one of the models (cf. [`md`](models_gen/install_md/), [`lg`](models_gen/install_lg/), [`trf`](models_gen/install_trf/)) into the `spacy_condaenv` conda environment.

### Alternative installation method

1. Create a new conda environment using the [`environment.yml`](https://github.com/huspacy/huspacy-in-r/blob/master/environment.yml) file in the [huspacy-in-r repository](https://github.com/huspacy/huspacy-in-r): `$ conda env create -n huspacyr --file ./environment.yml`
2. Activate the environment: `$ conda activate huspacyr`

The demo environment comes with the 3.4.3 version of the `hu_core_news_lg` model. If you need another model (or version) use `pip` (cf. [`md`](models_gen/install_md/), [`lg`](models_gen/install_lg/), [`trf`](models_gen/install_trf/)) to install the necessary model files to the conda environment.

## Usage

Having all dependencies installed, all you need to do is to load `spacyr` and initialize it with a HuSpaCy model:

```R
library("spacyr")

# Loads the model which is already installed tin the conda environment
spacy_initialize(model = "hu_core_news_lg")
```

HuSpaCy should now parse any texts:

```R
txt <- c(d1="Csiribiri csiribiri zabszalma,", d2="négy csillag közt alszom ma.")
parsedtxt <- spacy_parse(txt)
```

## Demo

[![Binder](http://mybinder.org/badge_logo.svg)](http://mybinder.org/v2/gh/huspacy/huspacy-in-r/master?filepath=demo.ipynb)

A live demo is accessible through binder [in this repository](https://github.com/huspacy/huspacy-in-r)