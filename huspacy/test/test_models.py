import pytest

import huspacy
from huspacy import get_valid_models

LATEST_MODELS = [(name, versions[-1]) for name, versions in get_valid_models().items()]


@pytest.mark.parametrize("model_name,version", LATEST_MODELS)
@pytest.mark.slow
def test_model(model_name, version):
    huspacy.download(model_name, version)
    nlp = huspacy.load(model_name)

    doc = nlp("Csiribiri csiribiri Zabszalma - Négy csillag közt alszom ma.")
    assert doc is not None
