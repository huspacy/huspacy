build:
	pipenv install
	cd src/emtsv && docker build . -t emtsv

get_data:
	cd data && make get

get_models:
	cd models && make get

v0.1:
	cd data && make interim/UD_Hungarian-Szeged
	cd models && make interim/ud_v0.1
