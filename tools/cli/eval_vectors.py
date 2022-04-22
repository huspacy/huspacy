import typer
import numpy as np

from floret.floret import _floret as Model
from floret import load_model
from scipy.spatial.distance import cdist
from typing import Tuple, List, Iterable
from pathlib import Path


app = typer.Typer()


def read_analogies(fpath: str) -> Iterable[Tuple[str, str, str, str]]:
    with Path(fpath).open() as f:
        for line in f:
            if line.startswith(":"):
                pass
            else:
                split: List[str] = line.split()
                yield tuple(split)


def eval(model: Model, questions: List[Tuple[str, str, str, str]], most_freq=50_000, topk=1) -> Tuple[float, float]:
    def idx(words: List[str], word: str) -> int:
        try:
            return words.index(word)
        except ValueError:
            return -1

    # Use the most frequent word only
    words, freqs = model.get_words(include_freq=True)
    frequent_words: List[str] = words[:most_freq]
    word_vectors = np.array([model.get_word_vector(w) for w in frequent_words])

    # Count the OOV items and keep the ones in the vocab
    eval_indices_orig = np.array([idx(frequent_words, tup[3]) for tup in questions])
    n_oov_items: int = len(eval_indices_orig[eval_indices_orig == -1])
    eval_indices = eval_indices_orig[eval_indices_orig != -1]
    eval_vecs = [
        model.get_word_vector(q2)
        - model.get_word_vector(q1)
        + model.get_word_vector(q3)
        for i, (q1, q2, q3, q4) in zip(eval_indices_orig, questions)
        if i != -1
    ]

    # Compute cos distance, sort and compute ranks
    distances = cdist(eval_vecs, word_vectors, metric="cosine")
    sim_args = distances.argsort(axis=1)
    eval_indices_ = np.broadcast_to(eval_indices, distances.T.shape).T
    ranks = np.argwhere(eval_indices_ == sim_args).T[1] + 1

    # Compute MRR by including OOV item results
    recip_ranks = 1 / ranks
    recip_ranks = np.concatenate([recip_ranks, np.zeros(n_oov_items)])
    mrr = recip_ranks.mean()

    # Compute accuracy
    tp = (ranks <= topk).sum()
    acc = tp / len(questions)
    oov_ratio = n_oov_items / len(questions)
    return acc, mrr, oov_ratio


@app.command()
def main(vectors: Path, questions_file: Path, most_freq: int = 50_000, topk: int = 1):
    questions: List[Tuple[str, str, str, str]] = list(read_analogies(questions_file))
    model: Model = load_model(str(vectors))
    accuracy, mrr, oov_ratio = eval(model, questions, most_freq, topk)
    print(
        vectors,
        f"Accuracy: {accuracy*100:.2f}%",
        f"MRR: {mrr:.4f}",
        f"OOV ratio: {oov_ratio*100:.2f}%",
        sep="\n"
    )


if __name__ == "__main__":
    app()
