from typing import Optional

import typer
from huggingface_hub import HfApi
from typer import Typer

app = Typer()


@app.command()
def main(repo_name: str, tag: str,
         message: Optional[str] = typer.Option(None, "-m", help="Tag message"),
         organization: str=typer.Option("huspacy", "-o", help="Organization slug"),
         delete_existing: bool = typer.Option(False, "-d", help="Delete tag if exists")):
    # token = typer.prompt("Auth token")
    api = HfApi()
    if delete_existing:
        api.delete_tag(repo_id=f"{organization}/{repo_name}", tag=tag)
    api.create_tag(repo_id=f"{organization}/{repo_name}", tag=tag, tag_message=message)


if __name__ == '__main__':
    app()
