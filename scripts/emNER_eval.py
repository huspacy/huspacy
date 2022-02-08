from seqeval.metrics import classification_report
from seqeval.metrics import f1_score
from typing import List
import os

# the order for evaluating the script is in the main function

def create_fake_conll_form_without_iob_to_emNER_input():
    """tokenized sentences for emNER
    input: iob format"""

    with open("/NerKor/test.iob", "r", encoding="utf-8") as f:
        corpus = f.readlines()

    current = "form\n" # to the emNER form

    for i in range(len(corpus)):
        if corpus[i] != "\n":
            current += corpus[i].split("\t")[0] + "\n"
        else:
            current += "\n"

    with open("input_for_emNER_nerkor_test.conllup", "w", encoding="utf-8") as f:
        f.write(current)


def conll_conv2_iobes():
    """conll convert to iobes form"""

    if not os.path.exists("nekor_test.out"):
        return

    with open("nerkor_test.out", "r", encoding="utf-8") as f:
        corpus = f.readlines()

    current = ""

    for i in range(len(corpus)):
        if i == 0:
            continue
        if corpus[i] != "\n":
            current += corpus[i].split("\t")[0] + "\t" + corpus[i].split("\t")[-1]
        else:
            current += "\n"

    with open("emNER_nerkor_test.iobes", "w", encoding="utf-8") as f:
        f.write(current)

def iobes_convert2_iob():
    """emNER has an iobes output format, so we convert it to simple iob"""

    if not os.path.exists("emNER_nerkor_test.iobes"):
        return

    with open("emNER_nerkor_test.iobes", "r", encoding="utf-8") as f:
        corpus = f.readlines()

    with open("emNER_nerkor_test.iob", "w", encoding="utf-8") as f:
        for i in range(len(corpus)):
            if corpus[i] != "\n":
                line = corpus[i].split("\t")[0] + "\t" + corpus[i].split("\t")[1]
                if line.split("\t")[1].startswith("1"):
                    temp = line.split("\t")[1][1:]
                    line = corpus[i].split("\t")[0] + "\t" + "B" + temp
                if line.split("\t")[1].startswith("E"):
                    temp = line.split("\t")[1][1:]
                    line = corpus[i].split("\t")[0] + "\t" + "I" + temp
                f.write(line)
            else:
                f.write("\n")


def pred():
    if not os.path.exists("emNER_nerkor_test.iob"):
        return

    with open("emNER_nerkor_test.iob", "r", encoding="utf-8") as f:
        pred_iob = f.readlines()

    pred_list = list()
    current_list = list()

    for i in range(len(pred_iob)):
        if len(pred_iob[i].strip()) != 0:
            current_list.append(pred_iob[i].split("\t")[1][:-1])
        else:
            pred_list.append(current_list)
            current_list = list()

    print(len(pred_list))
    return pred_list


def gold():
    with open("/NerKor/test.iob", "r", encoding="utf-8") as f:
        gold_iob = f.readlines()

    gold_list = list()
    current_list = list()

    for i in range(len(gold_iob)):
        if len(gold_iob[i].strip()) != 0:
            current_list.append(gold_iob[i].split("\t")[1][:-1])
        else:
            gold_list.append(current_list)
            current_list = list()

    print(len(gold_list))
    return gold_list


def fscore(gold_iob: List[List[str]], pred_iob: List[List[str]]):
    print(f1_score(gold_iob, pred_iob))
    print(classification_report(gold_iob, pred_iob))



if __name__ == "__main__":
    # create_fake_conll_form_without_iob_to_emNER_input()
    # bash: cat input_for_emNER_nerkor_test.conllup | docker run -i mtaril/emtsv:latest emMorph,emTag,emNER > nerkor_test.out
    # conll_conv2_iob()
    # iobes_convert2_iob()
    fscore(gold(), pred())
