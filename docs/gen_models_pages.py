from pathlib import Path
from typing import Dict

import mkdocs_gen_files
import requests

from huspacy import get_valid_models

META_URIS = {
    "md": "https://huggingface.co/huspacy/hu_core_news_md/raw/main/meta.json",
    "lg": "https://huggingface.co/huspacy/hu_core_news_lg/raw/main/meta.json",
    "trf": "https://huggingface.co/huspacy/hu_core_news_trf/raw/main/meta.json",
}

DOC_URIS = {
    "md": "https://huggingface.co/huspacy/hu_core_news_md/raw/main/README.md",
    "lg": "https://huggingface.co/huspacy/hu_core_news_lg/raw/main/README.md",
    "trf": "https://huggingface.co/huspacy/hu_core_news_trf/raw/main/README.md",
}

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
"""

DOC_TEMPLATE = """
# `{name}` model

## Installation

You can either install the model through `pip`:

```bash
# Install the latest model
$ pip install https://huggingface.co/huspacy/hu_core_news_{name}/resolve/main/hu_core_news_{name}-any-py3-none-any.whl

# Install a model with a specific version
$ pip install https://huggingface.co/huspacy/hu_core_news_{name}/resolve/[VERSION]/hu_core_news_{name}-any-py3-none-any.whl
```

or by using `huspacy`'s built-in facilities:

```python
import huspacy

# Install the latest model
huspacy.download("hu_core_news_{name}")

# Install a model with a specific version
huspacy.download("hu_core_news_{name}", version)
```

Available model versions: {versions}

## Details

{details}
"""


def read_metadat(uri: str) -> Dict:
    return requests.get(uri).json()


def create_doc(name: str, uri: str) -> str:
    readme_text: str = requests.get(uri).text
    meta_end_idx = readme_text.find("---", readme_text.find("---") + 3) + 3
    readme_text = readme_text[meta_end_idx:]
    versions = ", ".join([f"`{version}`" for version in get_valid_models()[f"hu_core_news_{name}"]])

    return DOC_TEMPLATE.format(name=name, details=readme_text, versions=versions)


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
        lg_version=models_metadata["lg"]["version"],
        lg_pos_acc=models_metadata["lg"]["performance"]["pos_acc"] * 100,
        lg_morph_acc=models_metadata["lg"]["performance"]["morph_acc"] * 100,
        lg_lemma_acc=models_metadata["lg"]["performance"]["lemma_acc"] * 100,
        lg_dep_las=models_metadata["lg"]["performance"]["dep_las"] * 100,
        lg_dep_uas=models_metadata["lg"]["performance"]["dep_uas"] * 100,
        lg_ner_f1=models_metadata["lg"]["performance"]["ents_f"] * 100,
        lg_throughput=models_metadata["lg"]["performance"]["speed"],
        trf_version=models_metadata["trf"]["version"],
        trf_pos_acc=models_metadata["trf"]["performance"]["pos_acc"] * 100,
        trf_morph_acc=models_metadata["trf"]["performance"]["morph_acc"] * 100,
        trf_lemma_acc=models_metadata["trf"]["performance"]["lemma_acc"] * 100,
        trf_dep_las=models_metadata["trf"]["performance"]["dep_las"] * 100,
        trf_dep_uas=models_metadata["trf"]["performance"]["dep_uas"] * 100,
        trf_ner_f1=models_metadata["trf"]["performance"]["ents_f"] * 100,
        trf_throughput=models_metadata["trf"]["performance"]["speed"],
    )


def main():
    models_meta = {name: read_metadat(uri) for name, uri in META_URIS.items()}
    perf_doc_path = Path("models_gen/performance.md")
    with mkdocs_gen_files.open(perf_doc_path, "w") as fd:
        print(generate_description(models_meta), file=fd)

    for name, uri in DOC_URIS.items():
        doc = create_doc(name, uri)
        doc_path = Path(f"models_gen/index_{name}.md")
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            print(doc, file=fd)


main()
