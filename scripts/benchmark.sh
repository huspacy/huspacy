#!/bin/bash

scripts_dir="../huspacy/cli/benchmarks"
token_count=$(grep -P "^[0-9].*$" $1 | wc -l)

# HuSpaCy v3 
huspacyv3_time=()
huspacyv3_memory=()

for i in {1..3} ; do
  echo 'HuSpaCy v3 #'${i}
  huspacyv3_time+=($(python "${scripts_dir}/huspacyv3_benchmark.py" main $1 --no-memory | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
  huspacyv3_memory+=($(python "${scripts_dir}/huspacyv3_benchmark.py" main $1 --no-time | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
done

# HuSpaCy v3 no-ner
huspacyv3_n_time=()
huspacyv3_n_memory=()

for i in {1..3} ; do
  echo 'HuSpaCy v3 w/o ner #'${i}
  huspacyv3_n_time+=($(python "${scripts_dir}/huspacyv3_benchmark.py" main $1 --no-memory --no-ner | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
  huspacyv3_n_memory+=($(python "${scripts_dir}/huspacyv3_benchmark.py" main $1 --no-time --no-ner | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
done

# HuSpaCy v3 gpu
huspacyv3_g_time=()
huspacyv3_g_memory=()

for i in {1..3} ; do
  echo 'HuSpaCy v3 w/ gpu #'${i}
  huspacyv3_g_time+=($(python "${scripts_dir}/huspacyv3_benchmark.py" main $1 --no-memory --gpu | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
  huspacyv3_g_memory+=($(python "${scripts_dir}/huspacyv3_benchmark.py" main $1 --no-time --gpu | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
done

# HuSpaCy v3 gpu no-ner
huspacyv3_gn_time=()
huspacyv3_gn_memory=()

for i in {1..3} ; do
  echo 'HuSpaCy v3 w/ gpu w/o ner #'${i}
  huspacyv3_gn_time+=($(python "${scripts_dir}/huspacyv3_benchmark.py" main $1 --no-memory --gpu --no-ner | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
  huspacyv3_gn_memory+=($(python "${scripts_dir}/huspacyv3_benchmark.py" main $1 --no-time --gpu --no-ner | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
done

# HuSpaCy v3 batch
huspacyv3_b_time=()
huspacyv3_b_memory=()

for i in {1..3} ; do
  echo 'HuSpaCy v3 batch #'${i}
  huspacyv3_b_time+=($(python "${scripts_dir}/huspacyv3_benchmark.py" batch $1 --no-memory | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
  huspacyv3_b_memory+=($(python "${scripts_dir}/huspacyv3_benchmark.py" batch $1 --no-time | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
done

# HuSpaCy v3 batch no-ner
huspacyv3_bn_time=()
huspacyv3_bn_memory=()

for i in {1..3} ; do
  echo 'HuSpaCy v3 batch w/o ner #'${i}
  huspacyv3_bn_time+=($(python "${scripts_dir}/huspacyv3_benchmark.py" batch $1 --no-memory --no-ner | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
  huspacyv3_bn_memory+=($(python "${scripts_dir}/huspacyv3_benchmark.py" batch $1 --no-time --no-ner | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
done

# HuSpaCy v3 batch gpu
huspacyv3_bg_time=()
huspacyv3_bg_memory=()

for i in {1..3} ; do
  echo 'HuSpaCy v3 batch w/ gpu #'${i}
  huspacyv3_bg_time+=($(python "${scripts_dir}/huspacyv3_benchmark.py" batch $1 --no-memory --gpu | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
  huspacyv3_bg_memory+=($(python "${scripts_dir}/huspacyv3_benchmark.py" batch $1 --no-time --gpu | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
done

# HuSpaCy v3 batch gpu no-ner
huspacyv3_bgn_time=()
huspacyv3_bgn_memory=()

for i in {1..3} ; do
  echo 'HuSpaCy v3 batch w/ gpu w/o ner #'${i}
  huspacyv3_bgn_time+=($(python "${scripts_dir}/huspacyv3_benchmark.py" batch $1 --no-memory --gpu --no-ner | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
  huspacyv3_bgn_memory+=($(python "${scripts_dir}/huspacyv3_benchmark.py" batch $1 --no-time --gpu --no-ner | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
done

# Stanza 
stanza_time=()
stanza_memory=()

for i in {1..3} ; do
  echo 'Stanza #'${i}
  stanza_time+=($(python "${scripts_dir}/stanza_benchmark.py" main $1 --no-memory | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
  stanza_memory+=($(python "${scripts_dir}/stanza_benchmark.py" main $1 --no-time | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
done

# Stanza
stanza_g_time=()
stanza_g_memory=()

for i in {1..3} ; do
  echo 'Stanza w/ gpu #'${i}
  stanza_g_time+=($(python "${scripts_dir}/stanza_benchmark.py" main $1 --no-memory --gpu | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
  stanza_g_memory+=($(python "${scripts_dir}/stanza_benchmark.py" main $1 --no-time --gpu | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
done

# UdPipe 
udpipe_time=()
udpipe_memory=()

for i in {1..3} ; do
  echo 'UdPipe #'${i}
  udpipe_time+=($(python "${scripts_dir}/udpipe_benchmark.py" main $1 --no-memory | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
  udpipe_memory+=($(python "${scripts_dir}/udpipe_benchmark.py" main $1 --no-time | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
done

# UdPipe batch
udpipe_b_time=()
udpipe_b_memory=()

for i in {1..3} ; do
  echo 'UdPipe batch #'${i}
  udpipe_b_time+=($(python "${scripts_dir}/udpipe_benchmark.py" batch $1 --no-memory | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
  udpipe_b_memory+=($(python "${scripts_dir}/udpipe_benchmark.py" batch $1 --no-time | grep -oP ': [0-9.]*' | grep -oP '[0-9.]*'))
done

find_min() {
  local min=99999999
  arr=("$@")
  for i in "${arr[@]}"
  do
    (( $(echo "$i < $min" | bc -l) )) && min=$i
  done
  echo $min
}

echo ''

echo '|tool|time|additional infos|'
echo '|---|---|---|'
echo '|spacy-hu|'$(find_min ${huspacyv3_time[@]})'s|spacy 3|'
echo '|spacy-hu|'$(find_min ${huspacyv3_n_time[@]})'s|spacy 3 w/o ner|'
echo '|spacy-hu|'$(find_min ${huspacyv3_g_time[@]})'s|spacy 3 w/ gpu|'
echo '|spacy-hu|'$(find_min ${huspacyv3_gn_time[@]})'s|spacy 3 w/ gpu w/o ner|'
echo '|spacy-hu|'$(find_min ${huspacyv3_b_time[@]})'s|spacy 3 batch|'
echo '|spacy-hu|'$(find_min ${huspacyv3_bn_time[@]})'s|spacy 3 batch w/o ner|'
echo '|spacy-hu|'$(find_min ${huspacyv3_bg_time[@]})'s|spacy 3 batch w/ gpu|'
echo '|spacy-hu|'$(find_min ${huspacyv3_bgn_time[@]})'s|spacy 3 batch w/ gpu w/o ner|'
echo '|stanza|'$(find_min ${stanza_time[@]})'s|cpu|'
echo '|stanza|'$(find_min ${stanza_g_time[@]})'s|gpu|'
echo '|udpipe|'$(find_min ${udpipe_time[@]})'s|spacy-udpipe|'
echo '|udpipe|'$(find_min ${udpipe_b_time[@]})'s|spacy-udpipe batch|'

echo ''

echo '|tool|memory|additional infos|'
echo '|---|---|---|'
echo '|spacy-hu|'$(find_min ${huspacyv3_memory[@]})' MiB|spacy 3|'
echo '|spacy-hu|'$(find_min ${huspacyv3_n_memory[@]})' MiB|spacy 3 w/o ner|'
echo '|spacy-hu|'$(find_min ${huspacyv3_g_memory[@]})' MiB|spacy 3 w/ gpu|'
echo '|spacy-hu|'$(find_min ${huspacyv3_gn_memory[@]})' MiB|spacy 3 w/ gpu w/o ner|'
echo '|spacy-hu|'$(find_min ${huspacyv3_b_memory[@]})' MiB|spacy 3 batch|'
echo '|spacy-hu|'$(find_min ${huspacyv3_bn_memory[@]})' MiB|spacy 3 batch w/o ner|'
echo '|spacy-hu|'$(find_min ${huspacyv3_bg_memory[@]})' MiB|spacy 3 batch w/ gpu|'
echo '|spacy-hu|'$(find_min ${huspacyv3_bgn_memory[@]})' MiB|spacy 3 batch w/ gpu w/o ner|'
echo '|stanza|'$(find_min ${stanza_memory[@]})' MiB|cpu|'
echo '|stanza|'$(find_min ${stanza_g_memory[@]})' MiB|gpu|'
echo '|udpipe|'$(find_min ${udpipe_memory[@]})' MiB|spacy-udpipe|'
echo '|udpipe|'$(find_min ${udpipe_b_memory[@]})' MiB|spacy-udpipe batch|'

echo ''

echo '|tool|token/sec|additional infos|'
echo '|---|---|---|'
echo '|spacy-hu|'$(echo "scale=3; ${token_count} / $(find_min ${huspacyv3_time[@]})" | bc)' token/s|spacy 3|'
echo '|spacy-hu|'$(echo "scale=3; ${token_count} / $(find_min ${huspacyv3_n_time[@]})" | bc)' token/s|spacy 3 w/o ner|'
echo '|spacy-hu|'$(echo "scale=3; ${token_count} / $(find_min ${huspacyv3_g_time[@]})" | bc)' token/s|spacy 3 w/ gpu|'
echo '|spacy-hu|'$(echo "scale=3; ${token_count} / $(find_min ${huspacyv3_gn_time[@]})" | bc)' token/s|spacy 3 w/ gpu w/o ner|'
echo '|spacy-hu|'$(echo "scale=3; ${token_count} / $(find_min ${huspacyv3_b_time[@]})" | bc)' token/s|spacy 3 batch|'
echo '|spacy-hu|'$(echo "scale=3; ${token_count} / $(find_min ${huspacyv3_bn_time[@]})" | bc)' token/s|spacy 3 batch w/o ner|'
echo '|spacy-hu|'$(echo "scale=3; ${token_count} / $(find_min ${huspacyv3_bg_time[@]})" | bc)' token/s|spacy 3 batch w/ gpu|'
echo '|spacy-hu|'$(echo "scale=3; ${token_count} / $(find_min ${huspacyv3_bgn_time[@]})" | bc)' token/s|spacy 3 batch w/ gpu w/o ner|'
echo '|stanza|'$(echo "scale=3; ${token_count} / $(find_min ${stanza_time[@]})" | bc)' token/s|cpu|'
echo '|stanza|'$(echo "scale=3; ${token_count} / $(find_min ${stanza_g_time[@]})" | bc)' token/s|gpu|'
echo '|udpipe|'$(echo "scale=3; ${token_count} / $(find_min ${udpipe_time[@]})" | bc)' token/s|spacy-udpipe|'
echo '|udpipe|'$(echo "scale=3; ${token_count} / $(find_min ${udpipe_b_time[@]})" | bc)' token/s|spacy-udpipe batch|'

