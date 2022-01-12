"""lines check"""

with open("../iob_outputs_from_html/iob_file_v_1.iob", "r", encoding="utf-8") as f:
    pred = f.readlines()

with open("../iob_outputs_from_html/emBERT_eval/nerkor_dev_gold_v_1.conllup", "r", encoding="utf-8") as f:
    gold = f.readlines()


for i in range(len(pred)):
    if pred[i].split("\t")[0] != gold[i].split("\t")[0]:
        if pred[i].split("\t")[0] == "&quot;":
            continue
        print(i, pred[i], i, gold[i])
