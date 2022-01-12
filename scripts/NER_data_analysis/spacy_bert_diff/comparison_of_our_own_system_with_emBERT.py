"""gold, spacy prediction, bert prediction"""

with open("../iob_outputs_from_html/emBERT_eval/nerkor_dev_gold_v_1.conllup", "r", encoding="utf-8") as f:
    gold = f.readlines()

with open("../iob_outputs_from_html/iob_file_v_1.iob", "r", encoding="utf-8") as f:
    our_pred = f.readlines()

with open("../iob_outputs_from_html/emBERT_eval/nerkor_dev_emBERT_v_1.conllup", "r", encoding="utf-8") as f:
    bert = f.readlines()

current = "token\tgold\tspacy\tbert\n"

for i in range(len(gold)):
    if gold[i] != "\n":
        current += gold[i].strip() + "\t" + our_pred[i].split("\t")[1].strip() + "\t" + bert[i].split("\t")[1]
    else:
        current += "\n"

with open("../iob_outputs_from_html/emBERT_eval/result.conllup", "w", encoding="utf-8") as f:
    f.write(current)


