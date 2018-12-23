.PHONY: interim/ud_v0.1 packaged/ud_v0.1

init:
	mkdir -p external
	mkdir -p interim
	mkdir -p packaged

get: init get_vectors external/webcorpuswiki.freqs external/webcorpuswiki.clusters

get_vectors: external/hunembed.bin external/hu.szte.w2v.bin external/webcorpuswiki.word2vec.bz2

external/hunembed.bin:
	wget http://corpus.nytud.hu/efnilex-vect/data/hunembed0.0 -O ./external/hunembed.bin

external/hu.szte.w2v.bin:
	wget http://rgai.inf.u-szeged.hu/project/nlp/research/w2v/hu.szte.w2v.bin -O ./external/hu.szte.w2v.bin

external/webcorpuswiki.word2vec.bz2:
	wget https://github.com/oroszgy/hunlp-resources/releases/download/webcorpuswiki_word2vec_v0.1/webcorpuswiki.word2vec.bz2 -O ./external/webcorpuswiki.word2vec.bz2

external/webcorpuswiki.freqs:
	wget https://github.com/oroszgy/hunlp-resources/releases/download/webcorpuswiki_freqs_v0.1/webcorpuswiki.freqs -O cwebcorpuswiki.freqs

external/webcorpuswiki.clusters:
	wget https://github.com/oroszgy/hunlp-resources/releases/download/webcorpuswiki_brownclusters_v0.1/paths -O ./external/webcorpuswiki.clusters

interim/hu.szte.w2v.txt:
	PYTHONPATH="../src" pipenv run python -m models convert-vectors-to-txt ./external/hu.szte.w2v.bin ./interim/hu.szte.w2v.txt
	PYTHONPATH="../src" pipenv run python -m models eval_vectors ./interim/hu.szte.w2v.txt

interim/vocab_v0.1: external/webcorpuswiki.clusters interim/hu.szte.w2v.txt
	pipenv run python -m spacy init-model hu interim/vocab_v0.1 -c ./external/webcorpuswiki.clusters -v ./interim/hu.szte.w2v.txt

interim/ud_v0.1: interim/vocab_v0.1
	pipenv run python -m spacy train hu -m ../src/resources/ud_meta.json -V 0.1 -N -n 30 -v interim/vocab_v0.1  interim/ud_v0.1 ../data/interim/UD_Hungarian-Szeged/hu_szeged-ud-train.json ../data/interim/UD_Hungarian-Szeged/hu_szeged-ud-dev.json
	pipenv run python -m spacy evaluate ./models/interim/ud_v0.1/model-final ./data/interim/UD_Hungarian-Szeged/hu_szeged-ud-test.json
	# Evaluate on test set, use preprocessed data?

packaged/ud_v0.1: interim/ud_v0.1
	mkdir -p packaged/ud_v0.1
	pipenv run python -m spacy package ./interim/ud_v0.1/model-final ./packaged/ud_v0.1
	cd ./packaged/ud_v0.1 && python3 setup.py sdist bdist_wheel
