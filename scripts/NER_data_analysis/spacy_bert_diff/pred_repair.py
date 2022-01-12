"""There were unnecessary lines in the corpus, so the lines were not correct for comparison, where the words of the lines had to be the same."""

with open("../iob_outputs_from_html/iob_files.iob", "r", encoding="utf-8") as f:
    pred = f.readlines()

current = ""

for i in range(len(pred)):
    if pred[i] != "\n":
        if pred[i].startswith("\t"):
            continue
        current += pred[i] # unnecessary lines
    else:
        current += "\n"

with open("../iob_outputs_from_html/iob_file_v_1.iob", "w", encoding="utf-8") as f:
    f.write(current)
