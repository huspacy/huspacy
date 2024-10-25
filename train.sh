#!/bin/bash

poetry run spacy project assets
GPU=0 poetry run spacy project run all