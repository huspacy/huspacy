init:
	mkdir -p raw
	mkdir -p external
	mkdir -p interim
	mkdir -p processed

get: init raw/UD_Hungarian-Szeged raw/unimorph_hun raw/webcorpus_hu raw/Hungarian-annotated-conll17.tar

raw/UD_Hungarian-Szeged:
	git clone git@github.com:UniversalDependencies/UD_Hungarian-Szeged.git ./raw/UD_Hungarian-Szeged

raw/unimorph_hun:
	git clone git@github.com:unimorph/hun.git ./raw/unimorph_hun

raw/webcorpus_hu:
	mkdir -p raw/webcorpus_hu
	cd raw/webcorpus_hu && for i in `seq 0 9`; do wget ftp://ftp.mokk.bme.hu/Language/Hungarian/Crawl/Web2/web2-4p-$$i.tar.gz; done

#raw/magyarlanc_data:
#	mkdir -p raw/magyarlanc_data
#	wget https://github.com/oroszgy/magyarlanc/archive/master.zip -O magyarlanc.zip
#	unzip ./magyarlanc.zip

raw/Hungarian-annotated-conll17.tar:
	wget https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-1989/Hungarian-annotated-conll17.tar?sequence=21&isAllowed=y -O ./raw/Hungarian-annotated-conll17.tar

interim/UD_Hungarian-Szeged/hu_szeged-ud-train.json:
	mkdir -p ./interim/UD_Hungarian-Szeged
	pipenv run python -m spacy convert ./raw/UD_Hungarian-Szeged/hu_szeged-ud-train.conllu ./interim/UD_Hungarian-Szeged/

interim/UD_Hungarian-Szeged/hu_szeged-ud-dev.json:
	mkdir -p ./interim/UD_Hungarian-Szeged
	pipenv run python -m spacy convert ./raw/UD_Hungarian-Szeged/hu_szeged-ud-dev.conllu ./interim/UD_Hungarian-Szeged/

interim/UD_Hungarian-Szeged/hu_szeged-ud-test.json:
	mkdir -p ./interim/UD_Hungarian-Szeged
	pipenv run python -m spacy convert ./raw/UD_Hungarian-Szeged/hu_szeged-ud-test.conllu ./interim/UD_Hungarian-Szeged/

interim/UD_Hungarian-Szeged: interim/UD_Hungarian-Szeged/hu_szeged-ud-train.json \
								interim/UD_Hungarian-Szeged/hu_szeged-ud-dev.json \
								interim/UD_Hungarian-Szeged/hu_szeged-ud-test.json