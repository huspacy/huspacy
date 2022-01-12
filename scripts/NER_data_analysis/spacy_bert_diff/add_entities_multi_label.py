"""standard iob form"""

with open("../iob_outputs_from_html/raw_iob.iob", "r", encoding="utf-8") as f:
    iob_files = f.readlines()


with open("../iob_outputs_from_html/iob_files.iob", "w", encoding="utf-8") as f:
    for i in range(len(iob_files)):
        if iob_files[i] != "\n":
            current = iob_files[i].split("\t")[1].strip()
            current_word = iob_files[i].split("\t")[0].strip()

            if i == 0 or iob_files[i - 1] == "\n":
                if current == "O":
                    f.write(current_word + "\t" + current + "\n")
                    # print(current_word + "\t" + current + "\n")
                elif current != "O":
                    f.write(current_word + "\t" + "B-" + current + "\n")
                    # print(current_word + "\t" + "B-" + current + "\n")
                continue

            if iob_files[i - 1].split("\t")[1].strip() == "O" and current == "O":
                f.write(current_word + "\t" + "O" + "\n")
                # print(current_word + "\t" + "O" + "\n")
                continue

            if i != 0 and iob_files[i - 1] != "\n":
                if iob_files[i - 1].split("\t")[1].strip() == current:
                    f.write(current_word + "\t" + "I-" + current + "\n")
                    # print(current_word + "\t" + "I-" + current + "\n")
                elif i != 0 and iob_files[i - 1].split("\t")[1].strip() == "O":
                    f.write(current_word + "\t" + "B-" + current + "\n")
                    # print(current_word + "\t" + "B-" + current + "\n")
                else:
                    f.write(current_word + "\t" + "O" + "\n")
                    # print(current_word + "\t" + "O" + "\n")

        else:
            f.write("\n")
            # print("\n")
alma = 42