import json
from pathlib import Path
from typing import Optional, Dict

import typer

app = typer.Typer()


def read_score(model_path: Path, metric: str) -> float:
    with (model_path / "model-best" / "meta.json").open() as f:
        data: Dict = json.load(f)
        return data["performance"][metric]


@app.command()
def main(target_path: Path, metric: str):
    fname: str = str(target_path.name)
    parent_dir: Path = target_path.parent

    best_score: float = -1.0
    best_model: Optional[Path] = None
    for candidate_model in parent_dir.glob(f"{fname}-*"):
        act_score: float = read_score(candidate_model, metric)
        if act_score > best_score:
            best_score = act_score
            best_model = candidate_model

    print(f"Linking best model: {best_model} with {metric}={best_score}")
    if best_model is not None:
        target_path.is_symlink()
        if target_path.exists():
            target_path.rmdir()
        if target_path.is_symlink():
            target_path.unlink()
        target_path.absolute().symlink_to(best_model.absolute())


if __name__ == '__main__':
    app()
