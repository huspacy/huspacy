import resource
import spacy_udpipe
import typer
# noinspection PyUnresolvedReferences
from spacy_conll import init_parser
from conllu import parse_incr
from tqdm import tqdm
from contexttimer import Timer

app = typer.Typer()


@app.command()
def main(input_file: str, output_file: str = 'udpipe.conllu', time: bool = True, memory: bool = True):
    nlp = spacy_udpipe.load("hu")
    nlp.add_pipe("conll_formatter")

    data_file = open(input_file, 'r', encoding='utf-8')
    output_file = open(output_file, 'w', encoding='utf-8')

    sentences = list(parse_incr(data_file))

    if time:
        with Timer() as t:
            runner(nlp, output_file, sentences)
        print(f'Time spent: {t.elapsed:.2f} seconds')
    else:
        runner(nlp, output_file, sentences)

    output_file.close()

    if memory: print(f'Maximum memory usage: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.2f} MiB')


@app.command()
def batch(input_file: str, time: bool = True, memory: bool = True):
    nlp = spacy_udpipe.load("hu")

    data_file = open(input_file, "r", encoding="utf-8")
    sentences = list(parse_incr(data_file))
    
    texts = [s.metadata["text"] for s in sentences]

    if time:
        with Timer() as t:
            res = list(nlp.pipe(texts))
        print(f'Time spent: {t.elapsed:.2f} seconds')
    else:
        res = list(nlp.pipe(texts))

    if memory: print(f'Maximum memory usage: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.2f} MiB')


@app.command()
def test(input: str = 'Kulka János is szerepel az új szivárványcsaládos kampányban.'):
    nlp = spacy_udpipe.load("hu")
    nlp.add_pipe("conll_formatter")

    with Timer() as t:
        print(nlp(input)._.conll_str)

    print(f'Time spent: {t.elapsed:.2f} seconds')
    print(f'Maximum memory usage: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.2f} MiB')


def runner(nlp, output_file, sentences):
    for tokenList in tqdm(sentences):
        doc = nlp(tokenList.metadata['text'])
        print(f'# sent_id = {tokenList.metadata["sent_id"]}', f'# text = {tokenList.metadata["text"]}', doc._.conll_str,
              sep='\n', file=output_file)


if __name__ == '__main__':
    spacy_udpipe.download('hu')
    app()
