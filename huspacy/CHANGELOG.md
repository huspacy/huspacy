# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
### Changed
- Added support for `hu_core_news_trf-v3.7.1`, which is now downloaded from its release tag

## 0.13.0 - 2026-11-16
### Fixed
- `download()` requests the real wheel filename of the model: models published with a PEP 427 compliant name
  (`hu_core_news_lg`/`hu_core_news_md` 3.8.1, `hu_core_news_trf` 3.7.0, `hu_core_news_trf_xl` 3.5.2) are fetched
  by their versioned filename, which `pip>=25.3` and `uv` accept. Earlier versions keep the legacy `-any-` name.
- Removed a leftover debug print from `download()`

### Changed
- Added support for new models (`hu_core_news_lg-v3.8.1`, `hu_core_news_md-v3.8.1`, `hu_core_news_trf-v3.7.0`)
- Packaging migrated from Poetry to uv: PEP 621 metadata, `uv.lock`, and uv-based CI. The built wheel is unchanged
  apart from the newer metadata version and the SPDX license expression

## 0.12.1 - 2024-10-28
### Fixed
- Model download version check were using the default model's default version when not provided
- Python version compatibility has been fixed

## 0.12.0 - 2024-10-28
### Changed
- Added support for new models  (`hu_core_news_md-v3.8.0`, `hu_core_news_lg-v3.8.0`)
- Sunsetting EOL Pythonn versions

## 0.11.0 - 2023-10-27
### Changed
- Added support for new models  (`hu_core_news_md-v3.7.0`, `hu_core_news_lg-v3.7.0`, `hu_core_news_trf-v3.5.4`)

## 0.10.0 - 2023-08-30
### Changed
- Python 3.11 support
- Added support for new models  (`hu_core_news_md-v3.6.0`, `hu_core_news_md-v3.6.1`, `hu_core_news_lg-v3.6.0`, `hu_core_news_lg-v3.6.1`,`hu_core_news_trf-v3.5.3`)
- `huspacy.download()` now warns if the spaCy required by the model would overwrite is not compatible with the spacy version installed

## 0.9.0 - 2023-05-23
### Changed
- Added support for new models (`hu_core_news_md-v3.5.2`, `hu_core_news_lg-v3.5.2`, `hu_core_news_trf-v3.5.2`, `hu_core_news_trf_xl-v3.5.2`)
- Updated documentation with `benepar` usage and the noun chunking

## 0.8.1 - 2023-03-24
### Fixed
- Replace bogus transformer model versions with fixed ones (`hu_core_news_trf_xl-v3.5.1`, `hu_core_news_trf_xl-v3.5.1`)
- 
## 0.8.0 - 2023-03-23
### Fixed
- Applied an edit-tree lemmatizer fix, based on [explosion/spaCy#12017](https://github.com/explosion/spaCy/pull/12017)
### New
- Added support for new models (`hu_core_news_md-v3.5.1`, `hu_core_news_lg-v3.5.1`, `hu_core_news_trf_xl-v3.5.0`, `hu_core_news_trf_xl-v3.5.0`)

## 0.7.0 - 2023-02.08
### New
- Added support for new models (`hu_core_news_md-v3.5.0`, `hu_core_news_lg-v3.5.0`, `hu_core_news_trf_xl-v3.4.0`, `hu_core_news_trf-v3.4.0`)
- Updated documentation

## 0.6 - 2022-11-11
### New
- Added a lookup component for sentiment lexicons
- Added integration for novakat's onpp NER model (`nerpp`)
- Added support for new models (`hu_core_news_trf-v3.4.0`, `hu_core_news_md-v3.4.2`, `hu_core_news_lg-v3.4.4`)

### Fixed
- `packaging` dependency was implicit which might cause model loading failures

## 0.5.1 - 2022-10-27
### Changed
- Dropped Python 3.6 support

### New
- Added support for `hu_core_news_lg` `v3.4.3`

## 0.5 - 2022-10-12
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

## 0.4.3 - 2022-04-27
### Fixed
- Documentation updates
- Fixed model loading

## 0.4.2 - 2022-01-06
### Initial release
- Convenience functions for downloading and loading models


