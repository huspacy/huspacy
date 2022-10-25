# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 3.4.3
## Fixed
- Improved hyperparameters on dependency parsing 

## 3.4.2
### Changed
- Improved NER: using beam_ner with update_prob=1.0
- Using the r2.10 version on UD corpus ([Github Changelog](https://github.com/UniversalDependencies/UD_Hungarian-Szeged/tree/master))
- Using the v3 version on Szeged-Corpus ([Github Changelog](https://github.com/huspacy/huspacy-resources/tree/master/data/processed/szeged-corpus))
- Improved lemmatization
    - Replaced spacy's `trainable_lemmatizer` with our own port of it (`trainable_lemmatizer_v2`) which improves on the lemmatization of uppercase tokens
    - Added lemma smoothing step for improving on common errors of the trainable lemmatizer 

## 3.4.1
### Changed
- Improved lookup lemmatizer: bugfix and morph. feats usage for indexing lemma

## 3.4.0
### Changed
- spaCy 3.4.x compatibility
- improved tagging performance

## 3.3.1
### Added
- Added lookup lemmatizer before edit tree lemmatizer in the pipeline
- Added lemma smoother after edit tree lemmatizer in the pipeline

## 3.3.0
### Changed
- Replaced Lemmy lemmatizer w/ edit tree lemmatizer

## 3.2.2
### Changed
- Replaced static word vectors w/ char n-gram based floret ones
- Added multistep training to mitigate non-deterministic training behaviour

## 3.2.1
### Changed
- Using the Szarvas-Farkas split for SzegedNER
- Learning lemmata w/o "+" characters
- hunnerwiki is no longer used to train the NER
- Started using spacy's model numbering convention


## 0.4.2
### Fixed
- Better integration of the lemmatizer
- Updated the project's documentation

## 0.4.1
### Added
### Changed
- NER model is built on NerKor and SzegedNER
- Improved lemmatization for numbers and sentence starting tokens
- Improved lemmatization by using the whole Szeged Corpus
- Improved PoS tagging by pretraining on a silver standard corpora
- Improved Dependency parser by using pretraining on silver standard corpora
- Improved sentence splitter by using the multitask neural model
    
### Fixed
- Compatibility w/ Spacy 3.x


## [0.3.1](https://github.com/huspacy/huspacy/releases/tag/hu_core_ud_lg-0.3.1) - 2019-10-03
### Fixed
- Compatibility w/ Spacy 2.2.x

## [0.3.0](https://github.com/huspacy/huspacy/releases/tag/hu_core_ud_lg-0.3.0) - 2019-09-26
### Added
- Named Entity Recognition

## [0.2.0](https://github.com/huspacy/huspacy/releases/tag/hu_core_ud_lg-0.2.0) - 2019-06-02
### Fixed
- Compatibility w/ Spacy 2.1.x
### Added
- Minor sentence segmentation improvements
- Minor improvements in PoS tagging

## [0.1.0](https://github.com/huspacy/huspacy/releases/tag/hu_core_ud_lg-0.1.0) - 2019-01-04
### Added
- Lemmatization support using lemmy
- Rule based lemmatizer
- Multi-task CNN-based dependency parser
### Changed
- Support for spaCy 2.x
- Using the [UD Hungarian corpus](https://github.com/UniversalDependencies/UD_Hungarian-Szeged) for the whole training process

## [0.0.1](https://github.com/huspacy/huspacy/releases/tag/hu_tagger_web_md-0.1.0) - 2017-06-11
### Added
- Experimental support for spaCy 1.x
- PoS Tagger model with word vectors trained on an unreleased automatically transcribed Szeged Korpusz version