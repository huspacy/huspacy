# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.6
- Added support for sentiment lexicons

## 0.5.1
### Changed
- Dropped Python 3.6 support
- Added support for `hu_core_news_lg` `v3.4.3`

## 0.5
### Components
- `trainable_lemmatizer_v2`: fork
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


