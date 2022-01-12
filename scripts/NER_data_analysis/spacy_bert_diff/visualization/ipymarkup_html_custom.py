"""small changes to the html file to make it easier to understand"""

with open("../../iob_outputs_from_html/emBERT_eval/html_file_all.html", "r", encoding="utf-8") as f:
    lines = f.readlines()


current = ""
new_line = ""
for i in range(len(lines)):
    if lines[i].startswith("<div"):
        split_line = lines[i].split("white-space: pre-wrap")
        new_line = "<hr>" + split_line[0] + "white-space: pre-wrap; padding-bottom: 40px" + split_line[1]
        current += new_line
    else:
        current += lines[i]


with open("../../iob_outputs_from_html/emBERT_eval/gold_spacy_bert_pred_diff_all.html", "w", encoding="utf-8") as f:
    f.write(current)
