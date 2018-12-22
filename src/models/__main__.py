import click
from gensim.models.keyedvectors import KeyedVectors


@click.group()
def cli():
    pass


@cli.command()
@click.argument("from_path")
@click.argument("to_path")
def convert_bin2txt(from_path, to_path):
    model = KeyedVectors.load_word2vec_format(from_path, binary=True, unicode_errors="replace")
    model.save_word2vec_format(to_path, binary=False)


if __name__ == "__main__":
    cli()
