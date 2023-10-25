# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 3.5.4 - 2023-10-25
### Fixed
- Fixed a lemmatization bug: https://github.com/huspacy/huspacy/issues/62 

## 3.5.3 - 2023-08-30
### Changed
- Updated hyperparameters

## 3.5.2 - 2023-05-19
### Changed
- Updated dependencies
- Removed lemma smoothing
- Fixed a bug prohibiting the processing of large documents https://github.com/huspacy/huspacy/issues/54

## 3.5.1 - 2023-03-24
### Fixed
- Fixed conflicting dependencies

## 3.5.0 - 2023-03-22
### Changed
- spaCy 3.5.x compatibility
- Using the backported EditTreeLemmatizer for speedup inference [explosion/spaCy#12017](https://github.com/explosion/spaCy/pull/12017)

## 3.4.0 - 2022-09-20
### Changed
- Improved NER: using beam_ner with update_prob=1.0
- Using the r2.10 version on UD corpus ([GitHub Changelog](https://github.com/UniversalDependencies/UD_Hungarian-Szeged/tree/master))
- Using the v3 version on Szeged-Corpus ([GitHub Changelog](https://github.com/huspacy/huspacy-resources/tree/master/data/processed/szeged-corpus))
- spacy 3.4.x compatibility
- Updated `spacy-experimental` (including the biaffine parser) dependency

## 3.2.4 - 2022-09-07
### Changed
- Updated dependencies

## 3.2.3 - 2022-08-12
### Changed
- Improved lookup lemmatizer: bugfix and morph. feats usage for indexing lemma

## 3.2.2 - 2022-05-30
### Added
- Added lookup lemmatizer before edit tree lemmatizer in the pipeline
- Added lemma smoother after edit tree lemmatizer in the pipeline

## 3.2.1 - 2022-04-25
### Changed
- Minor improvements in the training pipeline

## 3.2.0 - 2022-04-02
### Added
- Transformer encoder
- Experimental edit-tree-lemmatizer
- Experimental biaffine parser
- Using the Szarvas-Farkas split for SzegedNER
- Learning lemmata w/o "+" characters
- hunnerwiki is no longer used to train the NER
- Started using spacy's model numbering convention


