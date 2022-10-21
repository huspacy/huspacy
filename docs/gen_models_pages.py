import re
from pathlib import Path
from typing import Dict

import mkdocs_gen_files
import requests

from huspacy import get_valid_models

MODEL_SLUGS = ["md", "lg", "trf"]

META_URI_TEMPLATE = "https://huggingface.co/huspacy/hu_core_news_{slug}/raw/main/meta.json"

MODEL_PATH_TEMPLATE = (
    "https://huggingface.co/huspacy/hu_core_news_{slug}/blob/main/hu_core_news_{slug}-any-py3-none-any.whl"
)

DOC_URI_TEMPLATE = "https://huggingface.co/huspacy/hu_core_news_{slug}/raw/main/README.md"

COMPARISON_TEMPLATE = """

| Models | `md` | `lg` | `trf`|
| ------ | ---- | ---- | ---- |
| Latest version | {md_version} | {lg_version} | {trf_version} |
| PoS Accuracy | {md_pos_acc:.2f} | {lg_pos_acc:.2f} | {trf_pos_acc:.2f} |
| Morph. Accuracy | {md_morph_acc:.2f} | {lg_morph_acc:.2f} | {trf_morph_acc:.2f} |
| Lemma Accuracy | {md_lemma_acc:.2f} | {lg_lemma_acc:.2f} | {trf_lemma_acc:.2f} |
| Dep. LAS | {md_dep_las:.2f} | {lg_dep_las:.2f} | {trf_dep_las:.2f} |
| Dep. UAS | {md_dep_uas:.2f} | {lg_dep_uas:.2f} | {trf_dep_uas:.2f} |
| NER F1 | {md_ner_f1:.2f} | {lg_ner_f1:.2f} | {trf_ner_f1:.2f} |
| Throughput (token/sec) | {md_throughput:.0f} (CPU) | {lg_throughput:.0f} (CPU) | {trf_throughput:.0f} (GPU) |
| Size | {md_size} | {lg_size} | {trf_size} |
"""

DOC_TEMPLATE = """
# `{name}` model

## Installation

You can either install the model through `pip`:

```bash
# Install the latest model
$ pip install https://huggingface.co/huspacy/hu_core_news_{name}/resolve/main/hu_core_news_{name}-any-py3-none-any.whl

# Install a model with a specific version such as the latest one ({latest_version})
$ pip install https://huggingface.co/huspacy/hu_core_news_{name}/resolve/v{latest_version}/hu_core_news_{name}-any-py3-none-any.whl
```

or by using `huspacy`'s built-in facilities:

```python
import huspacy

# Install the latest model
huspacy.download("hu_core_news_{name}")

# Install a model with a specific version such as the latest one ({latest_version})
huspacy.download("hu_core_news_{name}", "{latest_version}")
```

Available model versions: {versions}

## Details

{details}
"""

MODEL_SIZE_PATTERN = re.compile(r"(\d+(\.\d+)? [MG]B)")


def read_metadata(slug: str) -> Dict:
    metadata = requests.get(META_URI_TEMPLATE.format(slug=slug)).json()
    model_lfs_desc = requests.get(MODEL_PATH_TEMPLATE.format(slug=slug)).text
    model_size = MODEL_SIZE_PATTERN.search(model_lfs_desc).group(1)
    metadata["size"] = model_size
    return metadata


def create_doc(name: str, uri: str) -> str:
    readme_text: str = requests.get(uri).text
    meta_end_idx = readme_text.find("---", readme_text.find("---") + 3) + 3
    readme_text = readme_text[meta_end_idx:]
    versions_available = get_valid_models()[f"hu_core_news_{name}"]
    versions = ", ".join([f"`{version}`" for version in versions_available])

    return DOC_TEMPLATE.format(name=name, details=readme_text, versions=versions, latest_version=versions_available[-1])


def generate_description(models_metadata: Dict[str, Dict]) -> str:
    return COMPARISON_TEMPLATE.format(
        md_version=models_metadata["md"]["version"],
        md_pos_acc=models_metadata["md"]["performance"]["pos_acc"] * 100,
        md_morph_acc=models_metadata["md"]["performance"]["morph_acc"] * 100,
        md_lemma_acc=models_metadata["md"]["performance"]["lemma_acc"] * 100,
        md_dep_las=models_metadata["md"]["performance"]["dep_las"] * 100,
        md_dep_uas=models_metadata["md"]["performance"]["dep_uas"] * 100,
        md_ner_f1=models_metadata["md"]["performance"]["ents_f"] * 100,
        md_throughput=models_metadata["md"]["performance"]["speed"],
        md_size=models_metadata["md"]["size"],
        lg_version=models_metadata["lg"]["version"],
        lg_pos_acc=models_metadata["lg"]["performance"]["pos_acc"] * 100,
        lg_morph_acc=models_metadata["lg"]["performance"]["morph_acc"] * 100,
        lg_lemma_acc=models_metadata["lg"]["performance"]["lemma_acc"] * 100,
        lg_dep_las=models_metadata["lg"]["performance"]["dep_las"] * 100,
        lg_dep_uas=models_metadata["lg"]["performance"]["dep_uas"] * 100,
        lg_ner_f1=models_metadata["lg"]["performance"]["ents_f"] * 100,
        lg_throughput=models_metadata["lg"]["performance"]["speed"],
        lg_size=models_metadata["lg"]["size"],
        trf_version=models_metadata["trf"]["version"],
        trf_pos_acc=models_metadata["trf"]["performance"]["pos_acc"] * 100,
        trf_morph_acc=models_metadata["trf"]["performance"]["morph_acc"] * 100,
        trf_lemma_acc=models_metadata["trf"]["performance"]["lemma_acc"] * 100,
        trf_dep_las=models_metadata["trf"]["performance"]["dep_las"] * 100,
        trf_dep_uas=models_metadata["trf"]["performance"]["dep_uas"] * 100,
        trf_ner_f1=models_metadata["trf"]["performance"]["ents_f"] * 100,
        trf_throughput=models_metadata["trf"]["performance"]["speed"],
        trf_size=models_metadata["trf"]["size"],
    )


def main():
    models_meta = {slug: read_metadata(slug) for slug in MODEL_SLUGS}
    perf_doc_path = Path("models_gen/performance.md")
    with mkdocs_gen_files.open(perf_doc_path, "w") as fd:
        print(generate_description(models_meta), file=fd)

    for slug in MODEL_SLUGS:
        doc = create_doc(slug, DOC_URI_TEMPLATE.format(slug=slug))
        doc_path = Path(f"models_gen/index_{slug}.md")
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            print(doc, file=fd)


main()
