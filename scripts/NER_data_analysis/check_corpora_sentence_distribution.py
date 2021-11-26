import matplotlib.pyplot as plt
import seaborn as sns

### inputs: .iob ###
### inputs: .png ###

"""Checking the length distribution of corpora (with seaborn and matplotlib). The diagram is saved locally at the end of the script."""

def wiki_plot():
    with open("/home/gszabo/PycharmProjects/pythonProject/hunNerWiki/train.iob", "r", encoding="utf-8") as f:
        wiki_train = f.readlines()

    with open("/home/gszabo/PycharmProjects/pythonProject/hunNerWiki/dev.iob", "r", encoding="utf-8") as f:
        wiki_dev = f.readlines()

    with open("/home/gszabo/PycharmProjects/pythonProject/hunNerWiki/test.iob", "r", encoding="utf-8") as f:
        wiki_test = f.readlines()

    wiki_train_list = list()
    wiki_dev_list = list()
    wiki_test_list = list()

    current_sent = ""

    #split szavak mentén, (vessző, pont stb. esetén nincs fölös space)

    for i in range(len(wiki_train)):
        if wiki_train[i] != "\n":
            if wiki_train[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += wiki_train[i].split("\t")[0]
                continue
            current_sent += wiki_train[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                wiki_train_list.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    for i in range(len(wiki_dev)):
        if wiki_dev[i] != "\n":
            if wiki_dev[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += wiki_dev[i].split("\t")[0]
                continue
            current_sent += wiki_dev[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                wiki_dev_list.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    for i in range(len(wiki_test)):
        if wiki_test[i] != "\n":
            if wiki_test[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += wiki_test[i].split("\t")[0]
                continue
            current_sent += wiki_test[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                wiki_test_list.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    # wiki plot

    fig, axs = plt.subplots(2, 2, figsize=(8, 6))

    axs[0, 0].set_xlim(0, 200)
    axs[0, 0].set_ylim(0, 35)
    axs[0, 0].set_title("train")
    axs[0, 0].set_ylabel("frequency")
    axs[0, 1].set_xlim(0, 200)
    axs[0, 1].set_ylim(0, 35)
    axs[0, 1].set_title("dev")
    axs[0, 1].set_ylabel("frequency")
    axs[1, 0].set_xlim(0, 200)
    axs[1, 0].set_ylim(0, 35)
    axs[1, 0].set_title("test")
    axs[1, 0].set_ylabel("frequency")

    sns.histplot(wiki_train_list, kde=True, color="red", stat='percent', binwidth=5, ax=axs[0, 0]).set_xlabel(
        "Sentences length (number of words)")
    sns.histplot(wiki_dev_list, kde=True, color="green", stat='percent', binwidth=5, ax=axs[0, 1]).set_xlabel(
        "Sentences length (number of words)")
    sns.histplot(wiki_test_list, kde=True, color="blue", stat='percent', binwidth=5, ax=axs[1, 0]).set_xlabel(
        "Sentences length (number of words)")

    fig.subplots_adjust(top=0.85)
    fig.suptitle('hunNERwiki')
    fig.tight_layout()
    plt.show()

    fig.savefig('hunNERwiki.png', facecolor=fig.get_facecolor(), edgecolor='none')


def nerkor_plot():
    with open("/home/gszabo/PycharmProjects/pythonProject/NerKor/train.iob", "r", encoding="utf-8") as f:
        nerkor_train = f.readlines()

    with open("/home/gszabo/PycharmProjects/pythonProject/NerKor/dev.iob", "r", encoding="utf-8") as f:
        nerkor_dev = f.readlines()

    with open("/home/gszabo/PycharmProjects/pythonProject/NerKor/test.iob", "r", encoding="utf-8") as f:
        nerkor_test = f.readlines()

    nerkor_train_list = list()
    nerkor_dev_list = list()
    nerkor_test_list = list()

    current_sent = ""

    # split szavak mentén, (vessző, pont stb. esetén nincs fölös space)

    for i in range(len(nerkor_train)):
        if nerkor_train[i] != "\n":
            if nerkor_train[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += nerkor_train[i].split("\t")[0]
                continue
            current_sent += nerkor_train[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                nerkor_train_list.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    for i in range(len(nerkor_dev)):
        if nerkor_dev[i] != "\n":
            if nerkor_dev[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += nerkor_dev[i].split("\t")[0]
                continue
            current_sent += nerkor_dev[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                nerkor_dev_list.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    for i in range(len(nerkor_test)):
        if nerkor_test[i] != "\n":
            if nerkor_test[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += nerkor_test[i].split("\t")[0]
                continue
            current_sent += nerkor_test[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                nerkor_test_list.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    # nerkor plot

    fig, axs = plt.subplots(2, 2, figsize=(8, 6))

    axs[0, 0].set_xlim(0, 250)
    axs[0, 0].set_ylim(0, 33)
    axs[0, 0].set_title("train")
    axs[0, 0].set_ylabel("frequency")
    axs[0, 1].set_xlim(0, 250)
    axs[0, 1].set_ylim(0, 33)
    axs[0, 1].set_title("dev")
    axs[0, 1].set_ylabel("frequency")
    axs[1, 0].set_xlim(0, 250)
    axs[1, 0].set_ylim(0, 33)
    axs[1, 0].set_title("test")
    axs[1, 0].set_ylabel("frequency")

    sns.histplot(nerkor_train_list, kde=True, color="red", stat='percent', binwidth=5, ax=axs[0, 0]).set_xlabel(
        "Sentences length (number of words)")
    sns.histplot(nerkor_dev_list, kde=True, color="green", stat='percent', binwidth=5, ax=axs[0, 1]).set_xlabel(
        "Sentences length (number of words)")
    sns.histplot(nerkor_test_list, kde=True, color="blue", stat='percent', binwidth=5, ax=axs[1, 0]).set_xlabel(
        "Sentences length (number of words)")

    fig.subplots_adjust(top=0.85)
    fig.suptitle('NerKor')
    fig.tight_layout()
    plt.show()

    fig.savefig('NerKor.png', facecolor=fig.get_facecolor(), edgecolor='none')



def szfsszegedner_plot():
    with open("/home/gszabo/PycharmProjects/pythonProject/SZFS_SzegedNER/SZFSSzegedNER/train.iob", "r", encoding="utf-8") as f:
        szfs_train = f.readlines()

    with open("/home/gszabo/PycharmProjects/pythonProject/SZFS_SzegedNER/SZFSSzegedNER/dev.iob", "r", encoding="utf-8") as f:
        szfs_dev = f.readlines()

    with open("/home/gszabo/PycharmProjects/pythonProject/SZFS_SzegedNER/SZFSSzegedNER/test.iob", "r", encoding="utf-8") as f:
        szfs_test = f.readlines()

    szfs_train_list = list()
    szfs_dev_list = list()
    szfs_test_list = list()

    current_sent = ""

    # split szavak mentén, (vessző, pont stb. esetén nincs fölös space)

    for i in range(len(szfs_train)):
        if szfs_train[i] != "\n":
            if szfs_train[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += szfs_train[i].split("\t")[0]
                continue
            current_sent += szfs_train[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                szfs_train_list.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    for i in range(len(szfs_dev)):
        if szfs_dev[i] != "\n":
            if szfs_dev[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += szfs_dev[i].split("\t")[0]
                continue
            current_sent += szfs_dev[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                szfs_dev_list.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    for i in range(len(szfs_test)):
        if szfs_test[i] != "\n":
            if szfs_test[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += szfs_test[i].split("\t")[0]
                continue
            current_sent += szfs_test[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                szfs_test_list.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    # szfsplot

    fig, axs = plt.subplots(2, 2, figsize=(8, 6))

    axs[0, 0].set_xlim(0, 100)
    axs[0, 0].set_ylim(0, 30)
    axs[0, 0].set_title("train")
    axs[0, 0].set_ylabel("frequency")
    axs[0, 1].set_xlim(0, 100)
    axs[0, 1].set_ylim(0, 30)
    axs[0, 1].set_title("dev")
    axs[0, 1].set_ylabel("frequency")
    axs[1, 0].set_xlim(0, 100)
    axs[1, 0].set_ylim(0, 30)
    axs[1, 0].set_title("test")
    axs[1, 0].set_ylabel("frequency")

    sns.histplot(szfs_train_list, kde=True, color="red", stat='percent', binwidth=5, ax=axs[0, 0]).set_xlabel(
        "Sentences length (number of words)")
    sns.histplot(szfs_dev_list, kde=True, color="green", stat='percent', binwidth=5, ax=axs[0, 1]).set_xlabel(
        "Sentences length (number of words)")
    sns.histplot(szfs_test_list, kde=True, color="blue", stat='percent', binwidth=5, ax=axs[1, 0]).set_xlabel(
        "Sentences length (number of words)")

    fig.subplots_adjust(top=0.85)
    fig.suptitle('SzegedNER')
    fig.tight_layout()
    plt.show()
    fig.savefig('SzegedNER.png', facecolor=fig.get_facecolor(), edgecolor='none')



def nerkor_fiction_plot():
    with open("../NerKor/alcorpora/fiction/train_fiction.iob", "r", encoding="utf-8") as f:
        fiction_train = f.readlines()
    with open("../NerKor/alcorpora/fiction/dev_fiction.iob", "r", encoding="utf-8") as f:
        fiction_dev = f.readlines()
    with open("../NerKor/alcorpora/fiction/test_fiction.iob", "r", encoding="utf-8") as f:
        fiction_test = f.readlines()


    nerkor_fiction_train = list()
    nerkor_fiction_dev = list()
    nerkor_fiction_test = list()

    current_sent = ""

    for i in range(len(fiction_train)):
        if fiction_train[i] != "\n":
            if fiction_train[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += fiction_train[i].split("\t")[0]
                continue
            current_sent += fiction_train[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                nerkor_fiction_train.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    for i in range(len(fiction_dev)):
        if fiction_dev[i] != "\n":
            if fiction_dev[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += fiction_dev[i].split("\t")[0]
                continue
            current_sent += fiction_dev[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                nerkor_fiction_dev.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    for i in range(len(fiction_test)):
        if fiction_test[i] != "\n":
            if fiction_test[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += fiction_test[i].split("\t")[0]
                continue
            current_sent += fiction_test[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                nerkor_fiction_test.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""


    fig, axs = plt.subplots(2, 2, figsize=(8, 6))

    axs[0, 0].set_xlim(0, 150)
    axs[0, 0].set_ylim(0, 75)
    axs[0, 0].set_title("train")
    axs[0, 0].set_ylabel("frequency")
    axs[0, 1].set_xlim(0, 150)
    axs[0, 1].set_ylim(0, 75)
    axs[0, 1].set_title("dev")
    axs[0, 1].set_ylabel("frequency")
    axs[1, 0].set_xlim(0, 150)
    axs[1, 0].set_ylim(0, 75)
    axs[1, 0].set_title("test")
    axs[1, 0].set_ylabel("frequency")

    sns.histplot(nerkor_fiction_train, kde=True, color="red", stat='percent', binwidth=5, ax=axs[0, 0]).set_xlabel(
        "Sentences length (number of words)")
    sns.histplot(nerkor_fiction_dev, kde=True, color="green", stat='percent', binwidth=5, ax=axs[0, 1]).set_xlabel(
        "Sentences length (number of words)")
    sns.histplot(nerkor_fiction_test, kde=True, color="blue", stat='percent', binwidth=5, ax=axs[1, 0]).set_xlabel(
        "Sentences length (number of words)")

    fig.subplots_adjust(top=0.85)
    fig.suptitle('Nerkor fiction')
    fig.tight_layout()
    plt.show()
    fig.savefig('fiction.png', facecolor=fig.get_facecolor(), edgecolor='none')


def nerkor_legal_plot():
    with open("../NerKor/alcorpora/legal/train_legal.iob", "r", encoding="utf-8") as f:
        legal_train = f.readlines()
    with open("../NerKor/alcorpora/legal/dev_legal.iob", "r", encoding="utf-8") as f:
        legal_dev = f.readlines()
    with open("../NerKor/alcorpora/legal/test_legal.iob", "r", encoding="utf-8") as f:
        legal_test = f.readlines()


    nerkor_legal_train = list()
    nerkor_legal_dev = list()
    nerkor_legal_test = list()

    current_sent = ""

    for i in range(len(legal_train)):
        if legal_train[i] != "\n":
            if legal_train[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += legal_train[i].split("\t")[0]
                continue
            current_sent += legal_train[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                nerkor_legal_train.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    for i in range(len(legal_dev)):
        if legal_dev[i] != "\n":
            if legal_dev[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += legal_dev[i].split("\t")[0]
                continue
            current_sent += legal_dev[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                nerkor_legal_dev.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    for i in range(len(legal_test)):
        if legal_test[i] != "\n":
            if legal_test[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += legal_test[i].split("\t")[0]
                continue
            current_sent += legal_test[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                nerkor_legal_test.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    fig, axs = plt.subplots(2, 2, figsize=(8, 6))

    axs[0, 0].set_xlim(0, 170)
    axs[0, 0].set_ylim(0, 30)
    axs[0, 0].set_title("train")
    axs[0, 0].set_ylabel("frequency")
    axs[0, 1].set_xlim(0, 170)
    axs[0, 1].set_ylim(0, 30)
    axs[0, 1].set_title("dev")
    axs[0, 1].set_ylabel("frequency")
    axs[1, 0].set_xlim(0, 170)
    axs[1, 0].set_ylim(0, 30)
    axs[1, 0].set_title("test")
    axs[1, 0].set_ylabel("frequency")

    sns.histplot(nerkor_legal_train, kde=True, color="red", stat='percent', binwidth=5, ax=axs[0, 0]).set_xlabel(
        "Sentences length (number of words)")
    sns.histplot(nerkor_legal_dev, kde=True, color="green", stat='percent', binwidth=5, ax=axs[0, 1]).set_xlabel(
        "Sentences length (number of words)")
    sns.histplot(nerkor_legal_test, kde=True, color="blue", stat='percent', binwidth=5, ax=axs[1, 0]).set_xlabel(
        "Sentences length (number of words)")

    fig.subplots_adjust(top=0.85)
    fig.suptitle('Nerkor legal')
    fig.tight_layout()
    plt.show()
    fig.savefig('legal.png', facecolor=fig.get_facecolor(), edgecolor='none')


def nerkor_news_plot():
    with open("../NerKor/alcorpora/news/train_news.iob", "r", encoding="utf-8") as f:
        news_train = f.readlines()
    with open("../NerKor/alcorpora/news/dev_news.iob", "r", encoding="utf-8") as f:
        news_dev = f.readlines()
    with open("../NerKor/alcorpora/news/test_news.iob", "r", encoding="utf-8") as f:
        news_test = f.readlines()


    nerkor_news_train = list()
    nerkor_news_dev = list()
    nerkor_news_test = list()

    current_sent = ""

    for i in range(len(news_train)):
        if news_train[i] != "\n":
            if news_train[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += news_train[i].split("\t")[0]
                continue
            current_sent += news_train[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                nerkor_news_train.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    for i in range(len(news_dev)):
        if news_dev[i] != "\n":
            if news_dev[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += news_dev[i].split("\t")[0]
                continue
            current_sent += news_dev[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                nerkor_news_dev.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    for i in range(len(news_test)):
        if news_test[i] != "\n":
            if news_test[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += news_test[i].split("\t")[0]
                continue
            current_sent += news_test[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                nerkor_news_test.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    fig, axs = plt.subplots(2, 2, figsize=(8, 6))

    axs[0, 0].set_xlim(0, 230)
    axs[0, 0].set_ylim(0, 30)
    axs[0, 0].set_title("train")
    axs[0, 0].set_ylabel("frequency")
    axs[0, 1].set_xlim(0, 230)
    axs[0, 1].set_ylim(0, 30)
    axs[0, 1].set_title("dev")
    axs[0, 1].set_ylabel("frequency")
    axs[1, 0].set_xlim(0, 230)
    axs[1, 0].set_ylim(0, 30)
    axs[1, 0].set_title("test")
    axs[1, 0].set_ylabel("frequency")

    sns.histplot(nerkor_news_train, kde=True, color="red", stat='percent', binwidth=5, ax=axs[0, 0]).set_xlabel(
        "Sentences length (number of words)")
    sns.histplot(nerkor_news_dev, kde=True, color="green", stat='percent', binwidth=5, ax=axs[0, 1]).set_xlabel(
        "Sentences length (number of words)")
    sns.histplot(nerkor_news_test, kde=True, color="blue", stat='percent', binwidth=5, ax=axs[1, 0]).set_xlabel(
        "Sentences length (number of words)")

    fig.subplots_adjust(top=0.85)
    fig.suptitle('Nerkor news')
    fig.tight_layout()
    plt.show()
    fig.savefig('news.png', facecolor=fig.get_facecolor(), edgecolor='none')


def nerkor_web_plot():
    with open("../NerKor/alcorpora/web/train_web.iob", "r", encoding="utf-8") as f:
        web_train = f.readlines()
    with open("../NerKor/alcorpora/web/dev_web.iob", "r", encoding="utf-8") as f:
        web_dev = f.readlines()
    with open("../NerKor/alcorpora/web/test_web.iob", "r", encoding="utf-8") as f:
        web_test = f.readlines()


    nerkor_web_train = list()
    nerkor_web_dev = list()
    nerkor_web_test = list()

    current_sent = ""

    for i in range(len(web_train)):
        if web_train[i] != "\n":
            if web_train[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += web_train[i].split("\t")[0]
                continue
            current_sent += web_train[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                nerkor_web_train.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    for i in range(len(web_dev)):
        if web_dev[i] != "\n":
            if web_dev[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += web_dev[i].split("\t")[0]
                continue
            current_sent += web_dev[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                nerkor_web_dev.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    for i in range(len(web_test)):
        if web_test[i] != "\n":
            if web_test[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += web_test[i].split("\t")[0]
                continue
            current_sent += web_test[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                nerkor_web_test.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    fig, axs = plt.subplots(2, 2, figsize=(8, 6))

    axs[0, 0].set_xlim(0, 180)
    axs[0, 0].set_ylim(0, 30)
    axs[0, 0].set_title("train")
    axs[0, 0].set_ylabel("frequency")
    axs[0, 1].set_xlim(0, 180)
    axs[0, 1].set_ylim(0, 30)
    axs[0, 1].set_title("dev")
    axs[0, 1].set_ylabel("frequency")
    axs[1, 0].set_xlim(0, 180)
    axs[1, 0].set_ylim(0, 30)
    axs[1, 0].set_title("test")
    axs[1, 0].set_ylabel("frequency")

    sns.histplot(nerkor_web_train, kde=True, color="red", stat='percent', binwidth=5, ax=axs[0, 0]).set_xlabel(
        "Sentences length (number of words)")
    sns.histplot(nerkor_web_dev, kde=True, color="green", stat='percent', binwidth=5, ax=axs[0, 1]).set_xlabel(
        "Sentences length (number of words)")
    sns.histplot(nerkor_web_test, kde=True, color="blue", stat='percent', binwidth=5, ax=axs[1, 0]).set_xlabel(
        "Sentences length (number of words)")

    fig.subplots_adjust(top=0.85)
    fig.suptitle('Nerkor web')
    fig.tight_layout()
    plt.show()
    fig.savefig('web.png', facecolor=fig.get_facecolor(), edgecolor='none')


def nerkor_wiki_plot():
    with open("../NerKor/alcorpora/wikipedia/train_wikipedia.iob", "r", encoding="utf-8") as f:
        wiki_train = f.readlines()
    with open("../NerKor/alcorpora/wikipedia/dev_wikipedia.iob", "r", encoding="utf-8") as f:
        wiki_dev = f.readlines()
    with open("../NerKor/alcorpora/wikipedia/test_wikipedia.iob", "r", encoding="utf-8") as f:
        wiki_test = f.readlines()


    nerkor_wiki_train = list()
    nerkor_wiki_dev = list()
    nerkor_wiki_test = list()

    current_sent = ""

    for i in range(len(wiki_train)):
        if wiki_train[i] != "\n":
            if wiki_train[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += wiki_train[i].split("\t")[0]
                continue
            current_sent += wiki_train[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                nerkor_wiki_train.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    for i in range(len(wiki_dev)):
        if wiki_dev[i] != "\n":
            if wiki_dev[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += wiki_dev[i].split("\t")[0]
                continue
            current_sent += wiki_dev[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                nerkor_wiki_dev.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    for i in range(len(wiki_test)):
        if wiki_test[i] != "\n":
            if wiki_test[i + 1].split("\t")[0] in ['.', ',', ':', '!']:
                current_sent += wiki_test[i].split("\t")[0]
                continue
            current_sent += wiki_test[i].split("\t")[0] + " "
        else:
            if len(current_sent) != 0:
                nerkor_wiki_test.append(len([c for c in current_sent if c in [' ']]))
                current_sent = ""

    fig, axs = plt.subplots(2, 2, figsize=(8, 6))

    axs[0, 0].set_xlim(0, 80)
    axs[0, 0].set_ylim(0, 35)
    axs[0, 0].set_title("train")
    axs[0, 0].set_ylabel("frequency")
    axs[0, 1].set_xlim(0, 80)
    axs[0, 1].set_ylim(0, 35)
    axs[0, 1].set_title("dev")
    axs[0, 1].set_ylabel("frequency")
    axs[1, 0].set_xlim(0, 80)
    axs[1, 0].set_ylim(0, 35)
    axs[1, 0].set_title("test")
    axs[1, 0].set_ylabel("frequency")

    sns.histplot(nerkor_wiki_train, kde=True, color="red", stat='percent', binwidth=5, ax=axs[0, 0]).set_xlabel(
        "Sentences length (number of words)")
    sns.histplot(nerkor_wiki_dev, kde=True, color="green", stat='percent', binwidth=5, ax=axs[0, 1]).set_xlabel(
        "Sentences length (number of words)")
    sns.histplot(nerkor_wiki_test, kde=True, color="blue", stat='percent', binwidth=5, ax=axs[1, 0]).set_xlabel(
        "Sentences length (number of words)")

    fig.subplots_adjust(top=0.85)
    fig.suptitle('Nerkor wiki')
    fig.tight_layout()
    plt.show()
    fig.savefig('wiki.png', facecolor=fig.get_facecolor(), edgecolor='none')


#prototype

# szeged_train_list = list()
# szeged_dev_list = list()
# szeged_test_list = list()

# current_sent = ""

#-------------------------------------------------------------------------------
#szegedner split

# for i in range(len(szeged_train)):
#     if szeged_train[i] != "\n":
#         current_sent += szeged_train[i].split("\t")[0] + " "
#     else:
#         if len(current_sent) != 0:
#             szeged_train_list.append(len(current_sent))
#             current_sent = ""
#
# for i in range(len(szeged_dev)):
#     if szeged_dev[i] != "\n":
#         current_sent += szeged_dev[i].split("\t")[0] + " "
#     else:
#         if len(current_sent) != 0:
#             szeged_dev_list.append(len(current_sent))
#             current_sent = ""
#
# for i in range(len(szeged_test)):
#     if szeged_test[i] != "\n":
#         current_sent += szeged_test[i].split("\t")[0] + " "
#     else:
#         if len(current_sent) != 0:
#             szeged_test_list.append(len(current_sent))
#             current_sent = ""
#
# all_szeged_list = szeged_train_list + szeged_dev_list + szeged_test_list
#
#

if __name__ == "__main__":
    # wiki_plot()
    # nerkor_plot()
    # szfsszegedner_plot()
    nerkor_fiction_plot()
    # nerkor_legal_plot()
    # nerkor_news_plot()
    # nerkor_web_plot()
    # nerkor_wiki_plot()

