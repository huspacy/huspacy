FROM python:3.7

RUN python -m ensurepip
RUN pip install spacy>=2.1 lemmy click pandas gensim tqdm conllu

WORKDIR app
COPY hu_core_ud_lg-0.2.0-py3-none-any.whl /app/
COPY model_builder /app/model_builder
COPY conll17_ud_eval.py /app/

RUN pip install -I /app/hu_core_ud_lg-0.2.0-py3-none-any.whl
