"""post-processing of spacy eval script to iob format"""

with open("../iob_outputs_from_html/entities.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

alma = 42
iob_text = ""

for i in range(len(lines)):
    if lines[i].startswith("<div"):
        split_O_tag = lines[i].split(">")[1][:-2]
        if len(split_O_tag) == 0:
            continue

        if "/div" in lines[i]:
            iob_text_split = lines[i].split(">")[1][:-6]
            words = iob_text_split.split(" ")
            for word in words:
                iob_text += word + "\t" + "O" + "\n"
        elif "/div" not in lines[i]:
            iob_text_split_no_div = lines[i].split(">")[1][:-2]
            words_no_div = iob_text_split_no_div.split(" ")
            for word_no_div in words_no_div:
                iob_text += word_no_div + "\t" + "O" + "\n"
        else:
            for O_tags in split_O_tag:
                iob_text += O_tags + "\t" + "O" + "\n"
    elif lines[i].endswith("/div>\n"):
        # if i == 100:
        #     asd = 42
        if lines[i].strip() == "</div>":
            continue
        temp = lines[i].strip()[:-7]
        words = temp.split(" ")
        if len(words) == 0:
            continue
        for word in words:
            iob_text += word + "\t" + "O" + "\n"

    elif not lines[i].startswith("<") and not lines[i].startswith("\n") and "<" not in lines[i]:
        temp = lines[i].strip()
        if " " in temp and lines[i + 1].split(">")[1][:-6] in ["LOC", "PER", "ORG", "MISC"]:
            iob_text_split = temp.split(" ")
            for text in iob_text_split:
                iob_text += text + "\t" + lines[i + 1].split(">")[1][:-6] + "\n"
        elif " " not in temp and lines[i + 1].split(">")[1][:-6] in ["LOC", "PER", "ORG", "MISC"]:
            iob_text += temp + "\t" + lines[i + 1].split(">")[1][:-6] + "\n"
        else:
            O_tag = temp.split(" ")
            for word in O_tag:
                iob_text += word + "\t" + "O" + "\n"
    elif lines[i].startswith("</figure"):
        iob_text += ("\n")

    # if i == 200:
    #     break

with open("../iob_outputs_from_html/raw_iob.iob", "w", encoding="utf-8") as iob_file:
    iob_file.write(iob_text)
