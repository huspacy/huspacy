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
