build_emtsv:
	cd src/emtsv && docker build . -t emtsv

get_data:
	cd data && make get

get_models:
	cd models && make get

convert_ud_hu: