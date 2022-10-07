# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- Improved NER: using beam_ner with update_prob=1.0
- Using the r2.10 version on UD corpus ([Github Changelog](https://github.com/UniversalDependencies/UD_Hungarian-Szeged/tree/master))
- Using the v3 version on Szeged-Corpus ([Github Changelog](https://github.com/huspacy/huspacy-resources/tree/master/data/processed/szeged-corpus))
- spacy 3.4.x compatibility
- Updated `spacy-experimental` (including the biaffine parser) dependency

## 3.2.4
### Changed
- Updated dependencies

## 3.2.3
### Changed
- Improved lookup lemmatizer: bugfix and morph. feats usage for indexing lemma

## 3.2.2
### Added
- Added lookup lemmatizer before edit tree lemmatizer in the pipeline
- Added lemma smoother after edit tree lemmatizer in the pipeline

## 3.2.1
### Changed
- Minor improvements in the training pipeline

## 3.2.0
### Added
- Transformer encoder
- Experimental edit-tree-lemmatizer
- Experimental biaffine parser
- Using the Szarvas-Farkas split for SzegedNER
- Learning lemmata w/o "+" characters
- hunnerwiki is no longer used to train the NER
- Started using spacy's model numbering convention


