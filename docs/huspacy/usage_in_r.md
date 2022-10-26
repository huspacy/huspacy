# :octicons-arrow-switch-24: Usage in R

# Setup the environemnt

1. Make sure you have conda installed
2. Create a new environment using the [`environemnt.yml`] file in the [huspacy-in-r repository](https://github.com/huspacy/huspacy-in-r): `$ conda env create -n huspacyr --file ./environment.yml`
3. Activate the environment: `$ conda activate huspacyr`

The demo environment install the 3.4.3 version of the `hu_core_news_lg` model. If you need another model or version use `pip` (cf. [`md`](models_gen/install_md/), [`lg`](models_gen/install_lg/), [`trf`](models_gen/install_trf/)) to install the necessary model files to the conda environment.

Having all dependencies installed, all you need to do is to load `spacyr` in the installed environment:

## Usage

```R
library("spacyr")

# Loads the model which is already installed tin the conda environment
spacy_initialize(model = "hu_core_news_lg")
```

HuSpaCy model should now parse any texts:

```R
txt <- c(d1="Csiribiri csiribiri zabszalma,", d2="négy csillag közt alszom ma.")
parsedtxt <- spacy_parse(txt)
```

## Demo

[![Binder](http://mybinder.org/badge_logo.svg)](http://mybinder.org/v2/gh/huspacy/huspacy-in-r/master?filepath=demo.ipynb)

A live demo is accessible through binder [in this repository](https://github.com/huspacy/huspacy-in-r)