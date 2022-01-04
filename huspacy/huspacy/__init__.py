import sys
from typing import Union, Iterable, Dict, Any
from pathlib import Path

import spacy.util as util
from spacy.vocab import Vocab
from spacy.language import Language
from thinc.api import Config

__URL = "https://huggingface.co/huspacy/hu_core_news_lg/resolve/{version}/{model_name}-any-py3-none-any.whl"
__DEFAULT_VERSION = "main"
__DEFAULT_MODEL = "hu_core_news_lg"


def download(model_name: str = __DEFAULT_MODEL, version: str = __DEFAULT_VERSION) -> None:
    """
    Downloads a HuSpaCy model
    Args:
        model_name (str): model name
        version (str): model version

    Returns:

    """
    download_url = __URL.format(version=version, model_name=model_name)
    cmd = [sys.executable, "-m", "pip", "install"] + [download_url]
    util.run_command(cmd)


# noinspection PyDefaultArgument
def load(
        name: Union[str, Path] = __DEFAULT_MODEL,
        vocab: Union[Vocab, bool] = True,
        disable: Iterable[str] = util.SimpleFrozenList(),
        exclude: Iterable[str] = util.SimpleFrozenList(),
        config: Union[Dict[str, Any], Config] = util.SimpleFrozenDict(),
) -> Language:
    """
    Load a HuSpaCy model

    Args:
        name (str): model name
        vocab (Vocab): A Vocab object. If True, a vocab is created.
        disable (Iterable[str]): Names of pipeline components to disable. Disabled pipes will be loaded but they
            won't be run unless you explicitly enable them by calling nlp.enable_pipe.
        exclude  (Iterable[str]): Names of pipeline components to exclude. Excluded components won't be loaded.
        config (Dict[str, Any] / Config): Config overrides as nested dict or dict
        keyed by section values in dot notation.

    Returns:
        Language: The loaded nlp object

    """
    return util.load_model(
        name, vocab=vocab, disable=disable, exclude=exclude, config=config
    )
