import sys

import pytest

import huspacy
from huspacy import get_valid_models
from huspacy.utils import run_command

LATEST_MODELS = [(name, versions[-1]) for name, versions in get_valid_models().items()]


@pytest.mark.parametrize("model_name,version", LATEST_MODELS)
@pytest.mark.slow
def test_model(model_name, version):
    # Cleanup environment
    run_command([sys.executable, "-m", "pip", "uninstall", "spacy", "-y"])
    for model_name, _ in LATEST_MODELS:
        run_command([sys.executable, "-m", "pip", "uninstall", model_name, "-y"])

    huspacy.download(model_name, version)
    nlp = huspacy.load(model_name)

    doc = nlp("Csiribiri csiribiri Zabszalma - Négy csillag közt alszom ma.")
    assert doc is not None
