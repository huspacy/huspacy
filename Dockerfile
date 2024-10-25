FROM nvidia/cuda:12.6.2-cudnn-devel-ubuntu20.04

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.8.3 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt-get update && apt install -y \
    curl \
    software-properties-common \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN add-apt-repository ppa:deadsnakes/ppa

RUN apt-get update && apt install -y \
    python3.12 \
    python3.12-distutils \
    git \
    && rm -rf /var/lib/apt/lists/*


RUN ln -s /usr/bin/python3.12 /usr/bin/python
RUN ln -s /usr/bin/python3.12 /usr/bin/python --force
RUN curl -sSL https://install.python-poetry.org | python3.12 -

WORKDIR /app/model

COPY pyproject.toml /app/model
COPY poetry.lock /app/model
COPY poetry.toml /app/model

RUN poetry install

COPY meta.json /app/model
COPY project.yml /app/model
COPY --from=root train.sh /app/model
