UD_LG_VERSION:=$(shell cat ./src/resources/ud_lg_meta.json | jq -r ".version")
UD_LG_NAME:=$(shell cat ./src/resources/ud_lg_meta.json | jq -r '(.lang + "_" + .name)')
ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

.PHONY: init all echo tests

all: models/packaged/$(UD_LG_NAME)-$(UD_LG_VERSION) | tests

echo:
	echo $(UD_LG_NAME) $(UD_LG_VERSION)

init:
	pipenv install
	cd src/emtsv && docker build . -t emtsv

######################################################### DATA #########################################################

#
#data/raw/unimorph_hun:
#	git clone git@github.com:unimorph/hun.git ./data/raw/unimorph_hun
#
#data/raw/webcorpus_hu:
#	mkdir -p data/raw/webcorpus_hu
#	cd data/raw/webcorpus_hu && for i in `seq 0 9`; do wget ftp://ftp.mokk.bme.hu/Language/Hungarian/Crawl/Web2/web2-4p-$$i.tar.gz; done

data/raw/magyarlanc_data:
	mkdir -p data/raw/magyarlanc_data && cd data/raw/magyarlanc_data \
		&& git init && git config core.sparseCheckout true \
		&& git remote add -f origin https://github.com/oroszgy/magyarlanc.git \
		&& echo "data/szk_univ_dep_2.0" > .git/info/sparse-checkout \
		&& echo "data/web_univ_dep" >> .git/info/sparse-checkout \
		&& echo "data/szk_univ_morph_2.5" >> .git/info/sparse-checkout \
		&& git checkout master

data/interim/szk_univ_dep_ud: | data/raw/magyarlanc_data
	mkdir -p data/interim/szk_univ_dep_ud

	PYTHONPATH="./src" pipenv run python -m model_builder convert-szk-to-conllu --dep 	\
		"data/raw/magyarlanc_data/data/szk_univ_dep_2.0/*.ud" data/interim/szk_univ_dep_ud/all_train.conllu \
		./data/raw/UD_Hungarian-Szeged/hu_szeged-ud-dev.conllu ./data/raw/UD_Hungarian-Szeged/hu_szeged-ud-test.conllu

	pipenv run python -m spacy convert data/interim/szk_univ_dep_ud/all_train.conllu data/interim/szk_univ_dep_ud

data/interim/szk_univ_morph: | data/raw/magyarlanc_data
	mkdir -p data/interim/szk_univ_morph

	PYTHONPATH="./src" pipenv run python -m model_builder convert-szk-to-conllu --morph \
		"data/raw/magyarlanc_data/data/szk_univ_morph_2.5/*.ud" data/interim/szk_univ_morph/all_train.conllu \
		./data/raw/UD_Hungarian-Szeged/hu_szeged-ud-dev.conllu ./data/raw/UD_Hungarian-Szeged/hu_szeged-ud-test.conllu

	pipenv run python -m spacy convert data/interim/szk_univ_dep_ud/all_train.conllu data/interim/szk_univ_morph


#data/raw/Hungarian-annotated-conll17.tar:
#	mkdir -p data/raw
#	wget https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-1989/Hungarian-annotated-conll17.tar?sequence=21&isAllowed=y -O ./data/raw/Hungarian-annotated-conll17.tar


data/raw/UD_Hungarian-Szeged:
	mkdir -p ./data/raw/UD_Hungarian-Szeged
	git clone git@github.com:UniversalDependencies/UD_Hungarian-Szeged.git ./data/raw/UD_Hungarian-Szeged

data/interim/UD_Hungarian-Szeged: | data/raw/UD_Hungarian-Szeged
	mkdir -p ./data/interim/UD_Hungarian-Szeged
	pipenv run python -m spacy convert ./data/raw/UD_Hungarian-Szeged/hu_szeged-ud-train.conllu ./data/interim/UD_Hungarian-Szeged/
	pipenv run python -m spacy convert ./data/raw/UD_Hungarian-Szeged/hu_szeged-ud-dev.conllu ./data/interim/UD_Hungarian-Szeged/
	pipenv run python -m spacy convert ./data/raw/UD_Hungarian-Szeged/hu_szeged-ud-test.conllu ./data/interim/UD_Hungarian-Szeged/

data/raw/hunnerwiki:
	mkdir -p ./data/raw/hunnerwiki
	wget http://hlt.sztaki.hu/resources/hunnerwiki/huwiki.1.ner.tsv.gz -O ./data/raw/hunnerwiki/huwiki.1.ner.tsv.gz
	wget http://hlt.sztaki.hu/resources/hunnerwiki/huwiki.2.ner.tsv.gz -O ./data/raw/hunnerwiki/huwiki.2.ner.tsv.gz
	wget http://hlt.sztaki.hu/resources/hunnerwiki/huwiki.3.ner.tsv.gz -O ./data/raw/hunnerwiki/huwiki.3.ner.tsv.gz
	wget http://hlt.sztaki.hu/resources/hunnerwiki/huwiki.4.ner.tsv.gz -O ./data/raw/hunnerwiki/huwiki.4.ner.tsv.gz

	pv ./data/raw/hunnerwiki/*.tsv.gz | zcat > ./data/raw/hunnerwiki/huwiki.tsv

data/raw/szeged_ner:
	mkdir -p data/raw/szeged_ner
	wget http://rgai.inf.u-szeged.hu/project/nlp/download/corpora/business_NER.zip -O data/raw/szeged_ner/business_NER.zip
	unzip data/raw/szeged_ner/business_NER.zip -d data/raw/szeged_ner/
	iconv -f iso-8859-2 --t utf8 data/raw/szeged_ner/hun_ner_corpus.txt | tail -n +2 > data/raw/szeged_ner/hun_ner_corpus_utf8.txt


################################################### EXTERNAL MODELS ###################################################


models/external/vectors/cc.hu.300.vec.gz:
	mkdir -p models/external/vectors
	wget https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.hu.300.vec.gz -O models/external/vectors/cc.hu.300.vec.gz

models/interim/vectors/cc.hu.300.txt: | models/external/vectors/cc.hu.300.vec.gz
	mkdir -p models/interim/vectors
	pv models/external/vectors/cc.hu.300.vec.gz | gzip -d > ./models/interim/vectors/cc.hu.300.txt
#	PYTHONPATH="./src" pipenv run python -m model_builder eval-vectors ./models/interim/vectors/cc.hu.300.txt

models/external/vectors/hunembed.tgz:
	mkdir -p models/external/vectors
	wget http://corpus.nytud.hu/efnilex-vect/data/hunembed0.0 -O ./models/external/vectors/hunembed.tgz
	tar -xvzf ./models/external/vectors/hunembed.tgz -C ./models/external/vectors/

models/external/vectors/webcorpuswiki.word2vec.bz2:
	mkdir -p ./models/external/vectors
	wget https://github.com/oroszgy/hunlp-resources/releases/download/webcorpuswiki_word2vec_v0.1/webcorpuswiki.word2vec.bz2 \
		-O ./models/external/vectors/webcorpuswiki.word2vec.bz2

models/interim/vectors/webcorpuswiki.word2vec.txt: | models/external/vectors/webcorpuswiki.word2vec.bz2
	mkdir -p models/interim/vectors/
	bzcat ./models/external/vectors/webcorpuswiki.word2vec.bz2 > ./models/interim/vectors/webcorpuswiki.word2vec.txt
	# PYTHONPATH="./src" pipenv run python -m model_builder eval-vectors ./model_builder/interim/vectors/webcorpuswiki.word2vec.txt


models/external/webcorpuswiki.freqs:
	mkdir -p ./models/external
	wget https://github.com/oroszgy/hunlp-resources/releases/download/webcorpuswiki_freqs_v0.1/webcorpuswiki.freqs \
		-O ./models/external/webcorpuswiki.freqs

models/external/webcorpuswiki.clusters:
	mkdir -p ./models/external/
	wget https://github.com/oroszgy/hunlp-resources/releases/download/webcorpuswiki_brownclusters_v0.1/paths \
		-O ./models/external/webcorpuswiki.clusters

################################################### GENERATED MODELS ###################################################

#models/spacy/szk_lg: | models/spacy/vectors_lg data/interim/szk_univ_morph data/interim/UD_Hungarian-Szeged
#	mkdir -p ./models/spacy/szk_lg
#	pipenv run python -m spacy train hu -m ./src/resources/ud_lg_meta.json -V 0.1 -P -N \
#		-n 30 -v models/spacy/vectors_lg  models/spacy/szk_lg \
#		 data/interim/szk_univ_morph/all_train.json \
#		 ./data/interim/UD_Hungarian-Szeged/hu_szeged-ud-dev.json
#	pipenv run python -m spacy evaluate \
#		./models/spacy/szk_lg/model-final \
#		./data/interim/UD_Hungarian-Szeged/hu_szeged-ud-test.json

models/spacy/lemmy: | data/raw/UD_Hungarian-Szeged data/interim/szk_univ_dep_ud
	mkdir -p models/spacy/lemmy
	PYTHONPATH="./src" pipenv run python -m model_builder train-lemmy \
		data/interim/szk_univ_dep_ud/all_train.conllu \
		data/raw/UD_Hungarian-Szeged/hu_szeged-ud-dev.conllu \
		models/spacy/lemmy/rules.json

models/spacy/vectors_lg: |  models/external/webcorpuswiki.freqs models/interim/vectors/webcorpuswiki.word2vec.txt models/external/webcorpuswiki.clusters
	mkdir -p ./models/spacy/vectors_lg
	pipenv run python -m spacy init-model \
		hu \
		models/spacy/vectors_lg \
		-f models/external/webcorpuswiki.freqs \
		-c models/external/webcorpuswiki.clusters \
		-v models/interim/vectors/webcorpuswiki.word2vec.txt

models/spacy/ft_vectors_lg: |  models/external/webcorpuswiki.freqs models/external/webcorpuswiki.clusters models/interim/vectors/cc.hu.300.txt
	mkdir -p ./models/spacy/ft_vectors_lg
	pipenv run python -m spacy init-model \
		hu \
		models/spacy/ft_vectors_lg \
		-f models/external/webcorpuswiki.freqs \
		-c models/external/webcorpuswiki.clusters \
		-v models/interim/vectors/cc.hu.300.txt

models/spacy/ud_lg: | data/interim/UD_Hungarian-Szeged models/spacy/vectors_lg
	mkdir -p ./models/spacy/ud_lg
	OPENBLAS_NUM_THREADS=8 GOTO_NUM_THREADS=8 OMP_NUM_THREADS=8\
	embed_size=10000 token_vector_width=256 hidden_width=256 \
	pipenv run python -m spacy train \
		hu \
		models/spacy/ud_lg \
		data/interim/UD_Hungarian-Szeged/hu_szeged-ud-train.json \
		data/interim/UD_Hungarian-Szeged/hu_szeged-ud-dev.json \
		--version $(UD_LG_VERSION) \
		--pipeline tagger,parser \
		--n-iter 60 \
		--n-early-stopping 10 \
		--parser-multitasks dep_tag_offset \
		--vectors models/spacy/vectors_lg \
		--meta-path ./src/resources/ud_lg_meta.json

	token_vector_width=256 pipenv run python -m spacy evaluate ./models/spacy/ud_lg/model-final \
		./data/interim/UD_Hungarian-Szeged/hu_szeged-ud-test.json

models/packaged/$(UD_LG_NAME)-$(UD_LG_VERSION): | models/spacy/lemmy models/spacy/ud_lg
	# Package spacy
	mkdir -p ./models/packaged
	pipenv run python -m spacy package \
		models/spacy/ud_lg/model-final/ \
		models/packaged/ \
		--force \
		--meta-path src/resources/ud_lg_meta.json

	# Dirty hack for fixing the wrong vector name generated
	cd models/packaged/$(UD_LG_NAME)-$(UD_LG_VERSION)/$(UD_LG_NAME)/$(UD_LG_NAME)-$(UD_LG_VERSION)/tagger/ \
		&& jq -r '.pretrained_vectors="$(UD_LG_NAME).vectors"' cfg | \
		jq -r '.token_vector_width=256' > cfg.new \
		&& mv cfg.new cfg

	cd models/packaged/$(UD_LG_NAME)-$(UD_LG_VERSION)/$(UD_LG_NAME)/$(UD_LG_NAME)-$(UD_LG_VERSION)/parser/ \
		&& jq -r '.pretrained_vectors="$(UD_LG_NAME).vectors"' cfg | \
		jq -r '.token_vector_width=256' > cfg.new \
		&& mv cfg.new cfg

	cp models/packaged/$(UD_LG_NAME)-$(UD_LG_VERSION)/meta.json models/packaged/$(UD_LG_NAME)-$(UD_LG_VERSION)/$(UD_LG_NAME)/meta.json

	# Add lemmatizer
	mkdir ./models/packaged/$(UD_LG_NAME)-$(UD_LG_VERSION)/$(UD_LG_NAME)/$(UD_LG_NAME)-$(UD_LG_VERSION)/lemmy/
	cp models/spacy/lemmy/rules.json ./models/packaged/$(UD_LG_NAME)-$(UD_LG_VERSION)/$(UD_LG_NAME)/$(UD_LG_NAME)-$(UD_LG_VERSION)/lemmy/
	cp src/resources/package_init.py ./models/packaged/$(UD_LG_NAME)-$(UD_LG_VERSION)/$(UD_LG_NAME)/__init__.py

	# Build packages
	cd ./models/packaged/$(UD_LG_NAME)-$(UD_LG_VERSION) && python3 setup.py sdist bdist_wheel

tests:
	cp $(ROOT_DIR)/models/packaged/$(UD_LG_NAME)-$(UD_LG_VERSION)/dist/$(UD_LG_NAME)-$(UD_LG_VERSION)-py3-none-any.whl ./src/

	cd src \
	&& docker build -t model_tests . \
	&& docker run -it --rm model_tests \
		/usr/local/bin/python -m model_builder smoke-test $(UD_LG_NAME) \
	&& docker run -it --rm -v $(ROOT_DIR)/data:/app/data model_tests \
		/usr/local/bin/python -m model_builder benchmark-model $(UD_LG_NAME) data/raw/UD_Hungarian-Szeged/hu_szeged-ud-test.conllu

	rm src/$(UD_LG_NAME)-$(UD_LG_VERSION)-py3-none-any.whl
