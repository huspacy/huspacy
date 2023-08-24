import re
from pathlib import Path
from typing import Dict

import mkdocs_gen_files
import requests

from huspacy import get_valid_models

MODEL_SLUGS = ["md", "lg", "trf", "trf_xl"]

META_URI_TEMPLATE = "https://huggingface.co/huspacy/hu_core_news_{slug}/raw/main/meta.json"

MODEL_PATH_TEMPLATE = (
    "https://huggingface.co/huspacy/hu_core_news_{slug}/blob/main/hu_core_news_{slug}-any-py3-none-any.whl"
)

DOC_URI_TEMPLATE = "https://huggingface.co/huspacy/hu_core_news_{slug}/raw/main/README.md"

COMPARISON_TEMPLATE = """

{description}

### Performance comparison

| Models | `md` | `lg` | `trf` | `trf_xl` |
| ------ | ---- | ---- | ---- |  ---- |
| Latest version | {md_version} | {lg_version} | {trf_version} | {trf_xl_version} |
| Token F1 | {md_token_f:.2f} | {lg_token_f:.2f} | {trf_token_f:.2f} | {trf_xl_token_f:.2f} |
| Sentence F1 | {md_sents_f:.2f} | {lg_sents_f:.2f} | {trf_sents_f:.2f} | {trf_xl_sents_f:.2f} |
| PoS Accuracy | {md_pos_acc:.2f} | {lg_pos_acc:.2f} | {trf_pos_acc:.2f} | {trf_xl_pos_acc:.2f} |
| Morph. Accuracy | {md_morph_acc:.2f} | {lg_morph_acc:.2f} | {trf_morph_acc:.2f} | {trf_xl_morph_acc:.2f} |
| Lemma Accuracy | {md_lemma_acc:.2f} | {lg_lemma_acc:.2f} | {trf_lemma_acc:.2f} | {trf_xl_lemma_acc:.2f} |
| LAS | {md_dep_las:.2f} | {lg_dep_las:.2f} | {trf_dep_las:.2f} | {trf_xl_dep_las:.2f} |
| UAS | {md_dep_uas:.2f} | {lg_dep_uas:.2f} | {trf_dep_uas:.2f} | {trf_xl_dep_uas:.2f} |
| NER F1 | {md_ner_f1:.2f} | {lg_ner_f1:.2f} | {trf_ner_f1:.2f} | {trf_xl_ner_f1:.2f} |
| Throughput (token/sec) | {md_throughput:.0f} (CPU) | {lg_throughput:.0f} (CPU) | {trf_throughput:.0f} (GPU) | {trf_xl_throughput:.0f} (GPU) |
| Size | {md_size} | {lg_size} | {trf_size} | {trf_xl_size} |
| Memory usage | 2.4 GB | 3.3 GB | 4.8 GB | 18 GB |
"""

INSTALL_TEMPLATE = """

You can either install the model through `pip`:

## Installation

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
"""

DETAILS_TEMPLATE = """

{introduction}

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


def create_details_docs(slug: str) -> str:
    uri = DOC_URI_TEMPLATE.format(slug=slug)
    details: str = requests.get(uri).text
    meta_end_idx = details.find("---", details.find("---") + 3) + 3
    details = details[meta_end_idx:]

    introduction = Path(f"docs/models/readme_{slug}.md").open().read()
    return DETAILS_TEMPLATE.format(introduction=introduction, details=details)


def create_install_doc(name: str) -> str:
    versions_available = get_valid_models()[f"hu_core_news_{name}"]
    versions = ", ".join([f"`{version}`" for version in versions_available])

    return INSTALL_TEMPLATE.format(name=name, versions=versions, latest_version=versions_available[-1])


def generate_description(models_metadata: Dict[str, Dict]) -> str:
    description = Path("docs/models/index.md").open().read()
    return COMPARISON_TEMPLATE.format(
        description=description,
        md_version=models_metadata["md"]["version"],
        md_token_f=models_metadata["md"]["performance"]["token_f"] * 100,
        md_sents_f=models_metadata["md"]["performance"]["sents_f"] * 100,
        md_pos_acc=models_metadata["md"]["performance"]["pos_acc"] * 100,
        md_morph_acc=models_metadata["md"]["performance"]["morph_acc"] * 100,
        md_lemma_acc=models_metadata["md"]["performance"]["lemma_acc"] * 100,
        md_dep_las=models_metadata["md"]["performance"]["dep_las"] * 100,
        md_dep_uas=models_metadata["md"]["performance"]["dep_uas"] * 100,
        md_ner_f1=models_metadata["md"]["performance"]["ents_f"] * 100,
        md_throughput=models_metadata["md"]["performance"]["speed"],
        md_size=models_metadata["md"]["size"],
        lg_version=models_metadata["lg"]["version"],
        lg_token_f=models_metadata["lg"]["performance"]["token_f"] * 100,
        lg_sents_f=models_metadata["lg"]["performance"]["sents_f"] * 100,
        lg_pos_acc=models_metadata["lg"]["performance"]["pos_acc"] * 100,
        lg_morph_acc=models_metadata["lg"]["performance"]["morph_acc"] * 100,
        lg_lemma_acc=models_metadata["lg"]["performance"]["lemma_acc"] * 100,
        lg_dep_las=models_metadata["lg"]["performance"]["dep_las"] * 100,
        lg_dep_uas=models_metadata["lg"]["performance"]["dep_uas"] * 100,
        lg_ner_f1=models_metadata["lg"]["performance"]["ents_f"] * 100,
        lg_throughput=models_metadata["lg"]["performance"]["speed"],
        lg_size=models_metadata["lg"]["size"],
        trf_version=models_metadata["trf"]["version"],
        trf_token_f=models_metadata["trf"]["performance"]["token_f"] * 100,
        trf_sents_f=models_metadata["trf"]["performance"]["sents_f"] * 100,
        trf_pos_acc=models_metadata["trf"]["performance"]["pos_acc"] * 100,
        trf_morph_acc=models_metadata["trf"]["performance"]["morph_acc"] * 100,
        trf_lemma_acc=models_metadata["trf"]["performance"]["lemma_acc"] * 100,
        trf_dep_las=models_metadata["trf"]["performance"]["dep_las"] * 100,
        trf_dep_uas=models_metadata["trf"]["performance"]["dep_uas"] * 100,
        trf_ner_f1=models_metadata["trf"]["performance"]["ents_f"] * 100,
        trf_throughput=models_metadata["trf"]["performance"]["speed"],
        trf_size=models_metadata["trf"]["size"],
        trf_xl_version=models_metadata["trf_xl"]["version"],
        trf_xl_token_f=models_metadata["trf_xl"]["performance"]["token_f"] * 100,
        trf_xl_sents_f=models_metadata["trf_xl"]["performance"]["sents_f"] * 100,
        trf_xl_pos_acc=models_metadata["trf_xl"]["performance"]["pos_acc"] * 100,
        trf_xl_morph_acc=models_metadata["trf_xl"]["performance"]["morph_acc"] * 100,
        trf_xl_lemma_acc=models_metadata["trf_xl"]["performance"]["lemma_acc"] * 100,
        trf_xl_dep_las=models_metadata["trf_xl"]["performance"]["dep_las"] * 100,
        trf_xl_dep_uas=models_metadata["trf_xl"]["performance"]["dep_uas"] * 100,
        trf_xl_ner_f1=models_metadata["trf_xl"]["performance"]["ents_f"] * 100,
        trf_xl_throughput=models_metadata["trf_xl"]["performance"]["speed"],
        trf_xl_size=models_metadata["trf_xl"]["size"],
    )


def main():
    models_meta = {slug: read_metadata(slug) for slug in MODEL_SLUGS}
    perf_doc_path = Path("models/index.md")
    with mkdocs_gen_files.open(perf_doc_path, "w") as fd:
        print(generate_description(models_meta), file=fd)

    for slug in MODEL_SLUGS:
        install_doc = create_install_doc(slug)
        doc_path = Path(f"models/install_{slug}.md")
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            print(install_doc, file=fd)

        details_docs = create_details_docs(slug)
        doc_path = Path(f"models/index_{slug}.md")
        with mkdocs_gen_files.open(doc_path, "w") as fd:
            print(details_docs, file=fd)


main()
