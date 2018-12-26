.PHONY: init

init: init_models init_data
	pipenv install
	cd src/emtsv && docker build . -t emtsv

###################################################### DATA ######################################################

init_data:
	mkdir -p data/raw
	mkdir -p data/interim

data/raw/UD_Hungarian-Szeged:
	git clone git@github.com:UniversalDependencies/UD_Hungarian-Szeged.git ./data/raw/UD_Hungarian-Szeged

data/raw/unimorph_hun:
	git clone git@github.com:unimorph/hun.git ./data/raw/unimorph_hun

data/raw/webcorpus_hu:
	mkdir -p data/raw/webcorpus_hu
	cd data/raw/webcorpus_hu && for i in `seq 0 9`; do wget ftp://ftp.mokk.bme.hu/Language/Hungarian/Crawl/Web2/web2-4p-$$i.tar.gz; done

#data/raw/magyarlanc_data:
#	mkdir -p data/raw/magyarlanc_data
#	wget https://github.com/oroszgy/magyarlanc/archive/master.zip -O data/raw/magyarlanc.zip
#	unzip ./magyarlanc.zip

data/raw/Hungarian-annotated-conll17.tar:
	wget https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-1989/Hungarian-annotated-conll17.tar?sequence=21&isAllowed=y -O ./data/raw/Hungarian-annotated-conll17.tar

data/interim/UD_Hungarian-Szeged/hu_szeged-ud-train.json: data/raw/UD_Hungarian-Szeged
	mkdir -p ./data/interim/UD_Hungarian-Szeged
	pipenv run python -m spacy convert ./data/raw/UD_Hungarian-Szeged/hu_szeged-ud-train.conllu ./data/interim/UD_Hungarian-Szeged/

data/interim/UD_Hungarian-Szeged/hu_szeged-ud-dev.json: data/raw/UD_Hungarian-Szeged
	mkdir -p ./data/interim/UD_Hungarian-Szeged
	pipenv run python -m spacy convert ./data/raw/UD_Hungarian-Szeged/hu_szeged-ud-dev.conllu ./data/interim/UD_Hungarian-Szeged/

data/interim/UD_Hungarian-Szeged/hu_szeged-ud-test.json: data/raw/UD_Hungarian-Szeged
	mkdir -p ./data/interim/UD_Hungarian-Szeged
	pipenv run python -m spacy convert ./data/raw/UD_Hungarian-Szeged/hu_szeged-ud-test.conllu ./data/interim/UD_Hungarian-Szeged/

data/interim/UD_Hungarian-Szeged: data/interim/UD_Hungarian-Szeged/hu_szeged-ud-train.json \
									data/interim/UD_Hungarian-Szeged/hu_szeged-ud-dev.json \
									data/interim/UD_Hungarian-Szeged/hu_szeged-ud-test.json

###################################################### MODELS ######################################################

init_models:
	mkdir -p ./models/external/vectors
	mkdir -p ./models/interim/vectors
	mkdir -p ./models/spacy

models/external/vectors/hunembed.bin:
	wget http://corpus.nytud.hu/efnilex-vect/data/hunembed0.0 -O ./models/external/vectors/hunembed.bin

models/external/vectors/hu.szte.w2v.bin:
	wget http://rgai.inf.u-szeged.hu/project/nlp/research/w2v/hu.szte.w2v.bin -O ./models/external/vectors/hu.szte.w2v.bin

models/external/vectors/webcorpuswiki.word2vec.bz2:
	wget https://github.com/oroszgy/hunlp-resources/releases/download/webcorpuswiki_word2vec_v0.1/webcorpuswiki.word2vec.bz2 \
		-O ./models/external/vectors/webcorpuswiki.word2vec.bz2

models/external/webcorpuswiki.freqs:
	wget https://github.com/oroszgy/hunlp-resources/releases/download/webcorpuswiki_freqs_v0.1/webcorpuswiki.freqs \
		-O ./models/external/webcorpuswiki.freqs

models/external/webcorpuswiki.clusters:
	wget https://github.com/oroszgy/hunlp-resources/releases/download/webcorpuswiki_brownclusters_v0.1/paths \
		-O ./models/external/webcorpuswiki.clusters

models/interim/vectors/hu.szte.w2v.txt: models/external/vectors/hu.szte.w2v.bin
	PYTHONPATH="./src" pipenv run python -m models convert-vectors-to-txt ./models/external/vectors/hu.szte.w2v.bin \
		./models/interim/vectors/hu.szte.w2v.txt
	# PYTHONPATH="./src" pipenv run python -m models eval_vectors ./models/interim/vectors/hu.szte.w2v.txt

models/interim/vectors/webcorpuswiki.word2vec.txt: models/external/vectors/webcorpuswiki.word2vec.bz2
	bzcat ./models/external/vectors/webcorpuswiki.word2vec.bz2 > ./models/interim/vectors/webcorpuswiki.word2vec.txt
	# PYTHONPATH="./src" pipenv run python -m models eval_vectors ./models/interim/vectors/webcorpuswiki.word2vec.txt

models/spacy/vectors_lg: models/external/webcorpuswiki.clusters models/external/webcorpuswiki.freqs models/interim/vectors/webcorpuswiki.word2vec.txt
	# FIXME: brown clusters and frequencies are not present in the model
	pipenv run python -m spacy init-model hu models/spacy/vectors_lg models/external/webcorpuswiki.freqs \
		-c ./models/external/webcorpuswiki.clusters -v ./models/interim/vectors/webcorpuswiki.word2vec.txt


models/spacy/ud_lg: models/spacy/vectors_lg data/interim/UD_Hungarian-Szeged
	pipenv run python -m spacy train hu -m ./src/resources/ud_lg_meta.json -V 0.1 -N \
		-n 30 -v models/spacy/vectors_lg  models/spacy/ud_lg \
		./data/interim/UD_Hungarian-Szeged/hu_szeged-ud-train.json ./data/interim/UD_Hungarian-Szeged/hu_szeged-ud-dev.json
	pipenv run python -m spacy evaluate ./models/spacy/ud_lg/model-final \
		./data/interim/UD_Hungarian-Szeged/hu_szeged-ud-test.json
	PYTHONPATH="./src" pipenv run python -m models test-model models/spacy/ud_lg/model-final

models/packaged/ud_lg: models/spacy/ud_lg
	pipenv run python -m spacy package --force models/spacy/ud_lg/model-final/ models/packaged/
	cd ./models/packaged/hu_ud_lg-0.1 && python3 setup.py sdist bdist_wheel
	#TODO: release
