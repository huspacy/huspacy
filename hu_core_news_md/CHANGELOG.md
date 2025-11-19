# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 3.8.1 - 2025-11-19
### Changed
- Fixed package naming: hf hub wheel now has a valid filename.

## 3.8.0 - 2024-10-28
### Changed
- spaCy 3.8.x compatibility

## 3.7.0 - 2023-10-25
### Changed
- spaCy 3.7.x compatibility
### Fixed
- Fixed a lemmatization bug: https://github.com/huspacy/huspacy/issues/62 

## 3.6.1 - 2023-08-15
### Changed
- Fine-tuned models

## 3.6.0 - 2023-08-03
### Changed
- spaCy 3.6.x compatibility
- Updated dependencies
- Updated resource list in model description
- Pinned NerKor version

## 3.5.2 - 2023-05-19
### Changed
- Updated dependencies
- Removed lemma smoothing


## 3.5.1 - 2023-03-22
### Changed
- Using the backported EditTreeLemmatizer for speedup inference [explosion/spaCy#12017](https://github.com/explosion/spaCy/pull/12017)
- Updated dependencies

## 3.5.0 - 2023-01-31
### Changed
- spaCy 3.5.x compatibility

## 3.4.2 - 2022-11-10
### Fixed
- Fixed dependencies of lemmatizer components

## 3.4.1 - 2022-10-07
### Initial release
- Added medium model, with medium (100d) vectors based on Webcorpus 2.0
- Improved NER: using beam_ner with update_prob=1.0
- Using the r2.10 version on UD corpus ([GitHub Changelog](https://github.com/UniversalDependencies/UD_Hungarian-Szeged/tree/master))
- Using the v3 version on Szeged-Corpus ([GitHub Changelog](https://github.com/huspacy/huspacy-resources/tree/master/data/processed/szeged-corpus))
- Improved lemmatization
    - Replaced spacy's `trainable_lemmatizer` with our own port of it (`trainable_lemmatizer_v2`) which improves on the lemmatization of uppercase tokens
    - Added lemma smoothing step for improving on common errors of the trainable lemmatizer
