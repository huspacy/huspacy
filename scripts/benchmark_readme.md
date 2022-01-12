# Readme to Benchmark

The `benchmark.sh` script takes an argument to which file to test on. The script runs tests on HuSpaCy, Stanza, and UDPipe. It runs each sub-benchmarking script three times on memory usage and on time spent.

- With HuSpaCy v3, it runs with default, GPU, batch, and batch w/ GPU settings.
- With Stanza, it runs with default and GPU settings.
- With UDPipe, it runs with default and batch settings.

To try it out, use the `./benchmark.sh ../data/raw/UD_Hungarian-Szeged/hu_szeged-ud-test.conllu` command in the `scripts` folder.

Usage: `./benchmark.sh <input file>`

## Sub-benchmarking scripts

If you want to try out the sub-benchmarking scripts separately, you can. These scripts can be found in the `huspacy/cli/benchmarks` folder.

### HuSpaCy w/ spaCy 3

You need to install spaCy 3, the spacy_conll package, and [this package](https://huggingface.co/huspacy/hu_core_news_lg) from Hugging Face Hub.
To run, use the `python huspacyv3_benchmark.py` command with the following arguments:

- `main <input file> [--output-file <output file>] [{--gpu} / --no-gpu] [{--time} / --no-time] [{--memory} / --no-memory] [{--ner} / --no-ner]`
- `batch <input file> [--output-file <output file>] [{--gpu} / --no-gpu] [{--time} / --no-time] [{--memory} / --no-memory] [{--ner} / --no-ner]`
- `test [--input <sentence>]`

### Stanza

You need to install the stanza package.
To run, use the `python stanza_benchmark.py` command with the following arguments:

- `main <input file> [--output-file <output file>] [{--gpu} / --no-gpu] [{--time} / --no-time] [{--memory} / --no-memory]`
- `test [--input <sentence>]`

### UDPipe w/ spaCy

You need to install spaCy 3, the spacy_conll package, and the spacy-udpipe package.
To run, use the `python udpipe_benchmark.py` command with the following arguments:

- `main <input file> [--output-file <output file>]  [{--time} / --no-time] [{--memory} / --no-memory]`
- `test [--input <sentence>]`

### emtsv

You need to start a docker container with the `docker run --rm -p5000:5000 -it mtaril/emtsv` command.
To run, use the `python emtsv_benchmark.py` command with the following arguments:

- `main <input file> [--output-file <output file>] [{--valid} / --no-valid] [{--time} / --no-time] [{--memory} / --no-memory]`
- `test [--input <sentence>]`

*FYI: this is not available in the `benchmark.sh` script.*

### HuSpaCy w/ spaCy 2

You need to install spaCy 2, the spacy-conll==2.1.0 package, and [this whl file](https://github.com/huspacy/huspacy/releases/hu_core_ud_lg-0.1.0).
To run, use the `python huspacyv2_benchmark.py` command with the following arguments:

- `main <input file> [--output-file <output file>] [{--time} / --no-time] [{--memory} / --no-memory]`
- `test [--input <sentence>]`

*FYI: this is not available in the `benchmark.sh` script.*
