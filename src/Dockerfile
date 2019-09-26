FROM python:3.7

RUN python -m ensurepip
RUN pip install spacy>=2.1 lemmy click pandas gensim tqdm conllu mlflow scikit-learn

ARG model_name

WORKDIR app
COPY ${model_name}-py3-none-any.whl /app/
COPY model_builder /app/model_builder
COPY conll17_ud_eval.py /app/

RUN pip install -I /app/${model_name}-py3-none-any.whl
