#!/bin/bash

if [ -z "$1" ]; then
  echo "Running end-to-end training"
  poetry run spacy project assets
  GPU=0 poetry run spacy project run all
else
  echo "Running '$1'"
  GPU=0 poetry run spacy project run $1
fi