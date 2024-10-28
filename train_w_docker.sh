#!/bin/bash

# Check if an argument was provided
if [ -z "$1" ]; then
  echo "No directory path provided."
  exit 1
fi

if [ ! -d "$1" ]; then
  echo "The path '$1' is not a valid directory."
  exit 1
fi

model_dir=$1
model_name=$(basename $model_dir)

docker buildx build -t trainer-${model_name} "${model_dir}" --build-context root="." -f ./Dockerfile
docker run -it --rm --name trainer-${model_name} \
  --runtime=nvidia \
  -v "$(pwd)/${model_dir}"/data:/app/model/data \
  -v "$(pwd)/${model_dir}"/models:/app/model/models \
  -v "$(pwd)/${model_dir}"/configs:/app/model/configs \
  -v "$(pwd)/${model_dir}"/packages:/app/model/packages \
  -v "$(pwd)/${model_dir}"/wandb:/app/model/wandb \
  -v "$(pwd)/${model_dir}"/../huspacy:/app/huspacy \
  -v "$(pwd)/${model_dir}"/../scripts:/app/scripts \
  trainer-${model_name} "./train.sh" "${@:2}"