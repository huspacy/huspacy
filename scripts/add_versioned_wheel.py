from typing import Optional

import typer
from huggingface_hub import CommitOperationCopy, HfApi
from typer import Typer

app = Typer()


@app.command()
def main(
    repo_name: str,
    version: str,
    message: Optional[str] = typer.Option(None, "-m", help="Commit message"),
    organization: str = typer.Option("huspacy", "-o", help="Organization slug"),
):
    """Publishes a versioned copy of a model's legacy wheel.

    Models released before the wheel filename fix carry a version-less
    `-any-py3-none-any.whl` file, which `pip>=25.3` and `uv` reject. Hugging Face
    tags are immutable, so the versioned file cannot be added under the existing
    release tag: it is created on `main`, next to the legacy wheel. The copy is
    server side, and the identical content is deduplicated by the hub.
    """
    api = HfApi()
    source = f"{repo_name}-any-py3-none-any.whl"
    target = f"{repo_name}-{version}-py3-none-any.whl"
    api.create_commit(
        repo_id=f"{organization}/{repo_name}",
        repo_type="model",
        commit_message=message or f"Add versioned wheel alias for {version}",
        operations=[
            CommitOperationCopy(src_path_in_repo=source, path_in_repo=target)
        ],
    )
    print(f"Copied {source} to {target} in {organization}/{repo_name}")


if __name__ == "__main__":
    app()
