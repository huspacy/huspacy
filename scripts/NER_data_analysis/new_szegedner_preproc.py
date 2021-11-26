"""preprocessing of a new SzegedNER set"""

### input: .txt (conll) ###
### output: .iob ###

def new_SzegedNER_train_preproc():
    with open("SzegedNer/train.txt", "r", encoding="utf-8") as f:
        szegedner_train = f.readlines()


    current_line = ""

    for i in range(len(szegedner_train)):
        if szegedner_train[i] != "\n":
            current_line += szegedner_train[i].split("\t")[0] + "\t" + szegedner_train[i].split("\t")[-1]
        else:
            current_line += "\n"


    with open("SzegedNer/train.iob", "w", encoding="utf-8") as f:
        f.write(current_line)

def new_SzegedNER_dev_preproc():
    with open("SzegedNer/valid.txt", "r", encoding="utf-8") as f:
        szegedner_valid = f.readlines()


    current_line = ""

    for i in range(len(szegedner_valid)):
        if szegedner_valid[i] != "\n":
            current_line += szegedner_valid[i].split("\t")[0] + "\t" + szegedner_valid[i].split("\t")[-1]
        else:
            current_line += "\n"


    with open("SzegedNer/dev.iob", "w", encoding="utf-8") as f:
        f.write(current_line)

def new_SzegedNER_test_preproc():
    with open("SzegedNer/test.txt", "r", encoding="utf-8") as f:
        szegedner_test = f.readlines()


    current_line = ""

    for i in range(len(szegedner_test)):
        if szegedner_test[i] != "\n":
            current_line += szegedner_test[i].split("\t")[0] + "\t" + szegedner_test[i].split("\t")[-1]
        else:
            current_line += "\n"


    with open("SzegedNer/test.iob", "w", encoding="utf-8") as f:
        f.write(current_line)

if __name__ == "__main__":
    new_SzegedNER_train_preproc()
    new_SzegedNER_dev_preproc()
    new_SzegedNER_test_preproc()
