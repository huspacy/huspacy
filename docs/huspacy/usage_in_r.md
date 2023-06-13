# :octicons-arrow-switch-24: Usage in R

## Installation

<!--pytest-codeblocks:skipfile-->

1. Make sure you have `conda` installed
2. Install a HuSpaCy model with `conda` (cf. [`md`](models_gen/install_md/), [`lg`](models_gen/install_lg/), [`trf`](models_gen/install_trf/)):

```R
library(reticulate)

conda_install(envname="huspacyr", "https://huggingface.co/huspacy/hu_core_news_lg/resolve/v3.5.2/hu_core_news_lg-any-py3-none-any.whl" ,pip=TRUE)
```

## Usage

Having all dependencies installed, all you need to do is to load `spacyr` and initialize it with a HuSpaCy model:

```R
library("spacyr")

# Loads the model which is already installed tin the conda environment
spacy_initialize(model = "hu_core_news_lg", condaenv="huspacyr")
```

HuSpaCy should now parse any texts:

```R
txt <- c(d1="Csiribiri csiribiri zabszalma,", d2="négy csillag közt alszom ma.")
parsedtxt <- spacy_parse(txt)
```
