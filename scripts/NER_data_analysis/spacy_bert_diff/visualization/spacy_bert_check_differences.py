"""the errors of the two systems are compared"""

with open("../../iob_outputs_from_html/emBERT_eval/result.conllup", "r", encoding="utf-8") as f:
    lines = f.readlines()

error = 0
sent = ""
diff = list()
for i in range(len(lines)):
    if i == 0:
        continue
    if lines[i] != "\n":
        if lines[i + 1].split("\t")[0] in [",", ".", "!", ":", "?", "(", ")", "_", "-", "'", '"', "/", "=", "%"]:
            sent += lines[i].split("\t")[0]
        elif lines[i].split("\t")[0] in ["-"]:
            sent += lines[i].split("\t")[0]
        else:
            sent += lines[i].split("\t")[0] + " "
        word = lines[i].split("\t")[0]
        gold = lines[i].split("\t")[1]
        spacy = lines[i].split("\t")[2]
        bert = lines[i].split("\t")[3][:-1]
        if gold == "O" and spacy == "O" and bert == "O":
            continue
        else:
        # gold != "O" and spacy != "O" and bert != "O":
            word_end_pos = len(sent) - 1
            word_start_pos = len(sent) - len(word) - 1
            diff.append(word + "\t" + gold + "\t" + spacy + "\t" + bert + "\t" + str(word_start_pos) + "\t" + str(word_end_pos))
            error += 1
    else:
        if error != 0:
            with open("../../iob_outputs_from_html/emBERT_eval/diff_v5.txt", "a", encoding="utf-8") as f:
                f.write(sent + "\n")
                for i in range(len(diff)):
                    f.write(diff[i] + "\n")
                f.write("\n")
        error = 0
        sent = ""
        diff = list()

