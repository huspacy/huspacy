
DIR=npchunk_corpora
INPUT=$(DIR)/arcj_teljes.10000.43.out_DEV

all:
	@clear
	@echo "Hungarian NP chunking demo"
	cat $(INPUT) | time python tools/np_chunk.py > out_chunks

