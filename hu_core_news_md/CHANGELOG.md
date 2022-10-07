# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]
### Changed
- Improved NER: using beam_ner with update_prob=1.0
- Using the r2.10 version on UD corpus ([Github Changelog](https://github.com/UniversalDependencies/UD_Hungarian-Szeged/tree/master))
- Using the v3 version on Szeged-Corpus ([Github Changelog](https://github.com/huspacy/huspacy-resources/tree/master/data/processed/szeged-corpus))
- Improved lemmatization
    - Replaced spacy's `trainable_lemmatizer` with our own port of it (`trainable_lemmatizer_v2`) which improves on the lemmatization of uppercase tokens
    - Added lemma smoothing step for improving on common errors of the trainable lemmatizer 

## 3.4.0
### Initial release

- Added medium model, with medium (100d) vectors based on Webcorpus 2.0
