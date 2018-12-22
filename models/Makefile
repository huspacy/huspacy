init:
	mkdir -p external
	mkdir -p interim
	mkdir -p processed

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
	PYTHONPATH="../src" pipenv run python -m models convert-bin2txt ./external/hu.szte.w2v.bin ./interim/hu.szte.w2v.txt