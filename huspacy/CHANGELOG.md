# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## ?
### Fixed
- Applied an edit-tree lemmatizer fix, based on [explosion/spaCy#12017](https://github.com/explosion/spaCy/pull/12017)

## 0.7.0
### New
- Added support for new models (`hu_core_news_md-v3.5.0`, `hu_core_news_lg-v3.5.0`, `hu_core_news_trf_xl-v3.4.0`)
- Updated documentation

## 0.6
### New
- Added a lookup component for sentiment lexicons
- Added integration for novakat's onpp NER model (`nerpp`)
- Added support for new models (`hu_core_news_trf-v3.4.0`, `hu_core_news_md-v3.4.2`, `hu_core_news_lg-v3.4.4`)

### Fixed
- `packaging` dependency was implicit which might cause model loading failures

## 0.5.1
### Changed
- Dropped Python 3.6 support

### New
- Added support for `hu_core_news_lg` `v3.4.3`

## 0.5
### New
- `trainable_lemmatizer_v2`: fork and minor improvement of spaCy's trainable lemmatizer
- `LemmaSmoother` for improving lemmatization output of the `trainable_lemmatizer`
- `RomanToArabic` for convert Roman numbers to Arabic ones
- `LookupLemmatizer` to memoize token,pos -> lemma transformations

### Fixed
- Fixing [#46](https://github.com/huspacy/huspacy/issues/46): huspacy core no longer depends on spaCy
- Refactored components

### Added
- Helper method for listing models available
- `download()` first validates the model before downloading it

## 0.4.3
### Fixed
- Documentation updates
- Fixed model loading

## 0.4.2
### Initial release
- Convenience functions for downloading and loading models


