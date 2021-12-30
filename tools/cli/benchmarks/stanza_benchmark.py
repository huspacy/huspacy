import resource
import stanza
import typer
from stanza.utils.conll import CoNLL
from conllu import parse_incr
from tqdm import tqdm
from contexttimer import Timer

app = typer.Typer()


@app.command()
def main(input_file: str, output_file: str = 'stanza.conllu', gpu: bool = False, time: bool = True, memory: bool = True):
    nlp = stanza.Pipeline('hu', use_gpu=gpu)

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
def test(input: str = 'Kulka János is szerepel az új szivárványcsaládos kampányban.'):
    nlp = stanza.Pipeline('hu')
    
    with Timer() as t:
        print(CoNLL.doc2conll_text(nlp(input)))
    
    print(f'Time spent: {t.elapsed:.2f} seconds')
    print(f'Maximum memory usage: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.2f} MiB')


def runner(nlp, output_file, sentences):
    for tokenList in tqdm(sentences):
        doc = nlp(tokenList.metadata['text'])
        print(f'# sent_id = {tokenList.metadata["sent_id"]}', f'# text = {tokenList.metadata["text"]}',
              CoNLL.doc2conll_text(doc), sep='\n', file=output_file)


if __name__ == '__main__':
    stanza.download('hu')
    app()
