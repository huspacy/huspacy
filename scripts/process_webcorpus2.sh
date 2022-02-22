wget -q -O - https://nessie.ilab.sztaki.hu/~ndavid/Webcorpus2_clean/$1 | zcat | grep "# text =" | cut -c 10- > ../data/processed/webcorpus2/cleaned/${1::-7}.txt
echo "$1 ✔️"