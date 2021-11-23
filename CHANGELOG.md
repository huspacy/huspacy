# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## `hu_core_news_lg`

## Unreleased
### Added
### Changed
- NER model built on NerKor and SzegedNER
- Improved lemmatization for numbers and sentence starting tokens
- Improved lemmatization by using the whole Szeged Corpus
- Improved PoS tagging by pretraining on a silver standard corpus
- Improved Dependency parser by using the pretrained tagger
- Improved sentence splitter: changing the architecture to the multitask neural model

### Fixed
- Compatibility w/ Spacy 3.x

## `hu_core_ud_lg`

Hungarian spacy model based on the [UD Hungarian corpus](https://github.com/UniversalDependencies/UD_Hungarian-Szeged)

## [0.3.1](https://github.com/spacy-hu/spacy-hungarian-models/releases/tag/hu_core_ud_lg-0.3.1) - 2019-10-03
## Fixed
- Compatibility w/ Spacy 2.2.x

## [0.3.0](https://github.com/spacy-hu/spacy-hungarian-models/releases/tag/hu_core_ud_lg-0.3.0) - 2019-09-26
### Added
- Named Entity Recognition

## [0.2.0](https://github.com/spacy-hu/spacy-hungarian-models/releases/tag/hu_core_ud_lg-0.2.0) - 2019-06-02
### Fixed
- Compatibility w/ Spacy 2.1.x
### Added
- Minor sentence segmentation improvements
- Minor improvements in PoS tagging

## [0.1.0](https://github.com/spacy-hu/spacy-hungarian-models/releases/tag/hu_core_ud_lg-0.1.0) - 2019-01-04
### Added
- Lemmatization support using lemmy
- Rule based lemmatizer
- Multi-task CNN-based dependency parser
### Changed
- Support for spaCy 2.x
- Using the [UD Hungarian corpus](https://github.com/UniversalDependencies/UD_Hungarian-Szeged) for the whole training process

## [0.0.1](https://github.com/spacy-hu/spacy-hungarian-models/releases/tag/hu_tagger_web_md-0.1.0) - 2017-06-11
### Added
- Experimental support for spaCy 1.x
- PoS Tagger model with word vectors trained on an unreleased automatically transcribed Szeged Korpusz version