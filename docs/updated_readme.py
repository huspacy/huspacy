import re
from pathlib import Path

FILES = {
    "intro": "docs/index.md",
    "models": "docs/models/index.md",
    "installation": "docs/huspacy/installation.md",
    "quickstart": "docs/huspacy/quickstart.md",
    "citing": "docs/huspacy/publications.md",
    "contact": "docs/contact.md",
    "license": "docs/huspacy/license.md",
}

TEMPLATE = """
{intro}

This repository contains material to build HuSpaCy and all of its models in a reproducible way.

{installation}

{quickstart}

API Documentation is available in [our website](https://huspacy.github.io/).

{models}

{citing}

{contact}

{license}
"""

ICON_PATTERN = re.compile(r":[a-z0-9\-]{5,}:")

URL_PATTERN = re.compile(r"\(/")


def read_doc(path: str) -> str:
    raw_content = Path(path).open().read().strip()
    content = raw_content.replace(":fontawesome-solid-star:", "⭑").replace(":fontawesome-solid-star-half-stroke:", "⭒")
    content: str = ICON_PATTERN.sub("", content)
    content = URL_PATTERN.sub("(https://huspacy.github.io/", content)
    return content


if __name__ == "__main__":
    docs = {slug: read_doc(path) for slug, path in FILES.items()}
    readme_content = TEMPLATE.format(**docs)
    with open("README.md", "w") as f:
        f.write(readme_content)
