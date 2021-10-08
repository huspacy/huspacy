import json
from pathlib import Path
from statistics import mean
from typing import Dict, Any

import typer

app = typer.Typer()


@app.command()
def main(parser_results: Path, ner_results: Path, output: Path):
    with parser_results.open() as f1, ner_results.open() as f2, output.open("w") as out:
        all_results: Dict[str, Any] = json.load(f1)
        ner_results: Dict[str, Any] = json.load(f2)
        for key, value in ner_results.items():
            if key not in all_results or all_results[key] is None or key.startswith("ents_"):
                all_results[key] = value
            elif key == "speed":
                all_results[key] = mean([all_results[key], value])

        json.dump(all_results, out, indent=2)


if __name__ == "__main__":
    app()
