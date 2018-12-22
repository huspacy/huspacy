build:
	pipenv install
	cd src/emtsv && docker build . -t emtsv

get_data:
	cd data && make get

get_models:
	cd models && make get

v0.1:
	cd models && make interim/hu.szte.w2v.txt
	pipenv run python -m spacy init-model hu ./models/interim/v0.1 -c ./models/external/webcorpuswiki.clusters -v ./models/interim/hu.szte.w2v.txt