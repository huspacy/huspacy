"""There were unnecessary lines in the gold, so the lines aren’t right for comparison, where the words in the lines had to be the same."""

with open("../iob_outputs_from_html/emBERT_eval/nerkor_dev_gold.conllup", "r", encoding="utf-8") as f:
    gold = f.readlines()

current = ""

for i in range(len(gold)):
    if gold[i] != "\n":
        current += gold[i].split("\t")[0] + "\t" + gold[i].split("\t")[-1]
    else:
        if gold[i - 1] == "\n": # unnecessary lines
            continue
        current += "\n"

with open("../iob_outputs_from_html/emBERT_eval/nerkor_dev_gold_v_1.conllup", "w", encoding="utf-8") as f:
    f.write(current)
