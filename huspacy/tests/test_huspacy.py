from typing import Dict

import pytest

import huspacy


@pytest.mark.parametrize(
    "model_name,version",
    [
        ["dummy", "1.0.0"],
        ["en_core_web_lg", "3.2.0"],
        ["hu_core_news_lg", "4.0.0"],
    ],
)
def test_download_fails(model_name: str, version: str):
    with pytest.raises(AssertionError) as e:
        huspacy.download(model_name, version)
        print(e)


def test_get_all_valid_models():
    valid_models: Dict = huspacy.get_valid_models()
    assert len(valid_models) == 4

    valid_models: Dict = huspacy.get_valid_models(None)
    assert len(valid_models) == 4


def test_get_valid_models():
    valid_models: Dict = huspacy.get_valid_models("3.2.1")
    assert len(valid_models) == 2

    valid_models: Dict = huspacy.get_valid_models("3.3.0")
    assert len(valid_models) == 1

    valid_models: Dict = huspacy.get_valid_models("3.4.0")
    assert len(valid_models) == 4

    valid_models: Dict = huspacy.get_valid_models("3.5.0")
    assert len(valid_models) == 4

    valid_models: Dict = huspacy.get_valid_models("3.5.2")
    assert len(valid_models) == 4

    valid_models: Dict = huspacy.get_valid_models("3.6.0")
    assert len(valid_models) == 2


@pytest.mark.parametrize(
    "model_name,version,expected_url",
    [
        (
            "hu_core_news_lg",
            "3.8.1",
            "https://huggingface.co/huspacy/hu_core_news_lg/resolve/v3.8.1/hu_core_news_lg-3.8.1-py3-none-any.whl",
        ),
        (
            "hu_core_news_md",
            "3.8.0",
            "https://huggingface.co/huspacy/hu_core_news_md/resolve/v3.8.0/hu_core_news_md-any-py3-none-any.whl",
        ),
        (
            "hu_core_news_trf",
            "3.7.0",
            "https://huggingface.co/huspacy/hu_core_news_trf/resolve/main/hu_core_news_trf-3.7.0-py3-none-any.whl",
        ),
        (
            "hu_core_news_trf",
            "3.7.1",
            "https://huggingface.co/huspacy/hu_core_news_trf/resolve/v3.7.1/hu_core_news_trf-3.7.1-py3-none-any.whl",
        ),
        (
            "hu_core_news_trf",
            "3.5.4",
            "https://huggingface.co/huspacy/hu_core_news_trf/resolve/v3.5.4/hu_core_news_trf-any-py3-none-any.whl",
        ),
        (
            "hu_core_news_trf_xl",
            "3.5.2",
            "https://huggingface.co/huspacy/hu_core_news_trf_xl/resolve/main/hu_core_news_trf_xl-3.5.2-py3-none-any.whl",
        ),
        (
            "hu_core_news_lg",
            "main",
            "https://huggingface.co/huspacy/hu_core_news_lg/resolve/main/hu_core_news_lg-any-py3-none-any.whl",
        ),
    ],
)
def test_wheel_url(model_name: str, version: str, expected_url: str):
    assert huspacy._wheel_url(model_name, version) == expected_url

