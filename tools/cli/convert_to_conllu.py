import glob
from pathlib import Path

import typer

app = typer.Typer()


@app.command()
def main(input_file_pattern: str, output_file: Path):
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w") as out:
        for input_file in glob.glob(input_file_pattern):
            with open(input_file) as inp:
                i = 0,
                for line in inp:
                    line = line.strip()
                    if line.startswith("#"):
                        i = 0
                        continue
                    elif len(line) > 0:
                        i += 1
                        parts = line.split("\t")
                        parts = [str(i)] + parts[:-1] + ["_", "_", "_"] + parts[-1:]
                        out.write("\t".join(parts))
                    else:
                        i = 0
                    out.write("\n")


if __name__ == "__main__":
    app()
