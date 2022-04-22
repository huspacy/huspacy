from conllu import parse_incr

import typer

app = typer.Typer()

@app.command()
def main(input_file: str, output_file: str):
    sentences = list(parse_incr(open(input_file, 'r')))

    for sentence in sentences:
        n_roots = 0
        first_root_id = -1

        for word in sentence:
            if word["head"] == 0:
                n_roots += 1

                if n_roots == 1:
                    first_root_id = word["id"]
                else:
                    # n_roots > 1

                    word["head"] = first_root_id
                    word["deprel"] = "nmod"

    with open(output_file, 'w') as f:
        f.writelines([sentence.serialize() for sentence in sentences])


if __name__ == "__main__":
    app()
