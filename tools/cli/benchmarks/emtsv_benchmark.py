import resource
import typer
from conllu import parse_incr
import conllu
from tqdm import tqdm
from contexttimer import Timer
import requests

app = typer.Typer()


@app.command()
def main(input_file: str, output_file: str = 'emtsv.conllu', valid: bool = True, time: bool = True, memory: bool = True):
    data_file = open(input_file, 'r', encoding='utf-8')
    output_file = open(output_file, 'w', encoding='utf-8')

    sentences = list(parse_incr(data_file))

    if time:
        with Timer() as t:
            runner(output_file, sentences)
        print(f'Time spent: {t.elapsed:.2f} seconds')
    else:
        runner(output_file, sentences)

    output_file.close()

    if valid: make_it_valid()

    if memory: print(f'Maximum memory usage: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.2f} MiB')


@app.command()
def test(input: str = 'Kulka János is szerepel az új szivárványcsaládos kampányban.'):
    with Timer() as t:
        r = requests.post('http://127.0.0.1:5000/tok/morph/pos/emmorph2ud/dep/conll', data={'text': input})
    print(r.text)

    print(f'Time spent: {t.elapsed:.2f} seconds')
    print(f'Maximum memory usage: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.2f} MiB')


def runner(output_file, sentences):
    for tokenList in tqdm(sentences):
        r = requests.post('http://127.0.0.1:5000/tok/morph/pos/emmorph2ud/dep/conll', data={'text': tokenList.metadata["text"]})
        print(f"# sent_id = {tokenList.metadata['sent_id']}",f"# text = {tokenList.metadata['text']}",r.text, sep="\n", file=output_file)


def make_it_valid():
    with open("emtsv.conllu", "r") as f:
        emtsv_text = f.readlines()
    sentences = conllu.parse("".join(emtsv_text).replace('\n\n\n', '\n\n'))
    
    for sentence in sentences:
        root_id = 0
        for word in sentence:
            if word["deprel"] == "ROOT":
                root_id = word["id"]
        
        for word in sentence:
            if word["deprel"] == "PUNCT" and word["head"] == 0:
                word["head"] = root_id
                
        for word in sentence:
            if word["head"] == 0 and word["id"] != root_id:
                word["head"] = root_id
    
    with open("emtsv_single_root.conllu", "w") as f:
        for sentence in sentences:
            f.write(sentence.serialize())

if __name__ == '__main__':
    app()
