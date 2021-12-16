file = open(r"../data/processed/NerKor/train.conllup", 'r')
f = open("../data/processed/NerKor/train.conllu", 'w')
while True:
    next_line = file.readline()

    if not next_line:
        break;

    correctsentence=""
    if(next_line != "\n"):
        split1=next_line.split()
        #print(split1[9])
        split1[4]="_"
        split1[9]="_"
        #print(split1)
    counter=0
    for i in split1:
        if(counter!=9):
            correctsentence=correctsentence+i + "\t"
        else:
            correctsentence = correctsentence + i
        counter=counter+1
    #print(correctsentence)
    f.write(correctsentence+"\n" )
file.close()
f.close()

file = open(r"../data/processed/NerKor/dev.conllup", 'r')
f = open("../data/processed/NerKor/dev.conllu", 'w')
while True:
    next_line = file.readline()

    if not next_line:
        break;

    correctsentence=""
    if(next_line != "\n"):
        split1=next_line.split()
        #print(split1[9])
        split1[4]="_"
        split1[9]="_"
        #print(split1)
    counter=0
    for i in split1:
        if(counter!=9):
            correctsentence=correctsentence+i + "\t"
        else:
            correctsentence = correctsentence + i
        counter=counter+1
    #print(correctsentence)
    f.write(correctsentence+"\n" )
file.close()
f.close()

file = open(r"../data/processed/NerKor/dev.conllup", 'r')
f = open("../data/processed/NerKor/dev.conllu", 'w')
while True:
    next_line = file.readline()

    if not next_line:
        break;

    correctsentence=""
    if(next_line != "\n"):
        split1=next_line.split()
        #print(split1[9])
        split1[4]="_"
        split1[9]="_"
        #print(split1)
    counter=0
    for i in split1:
        if(counter!=9):
            correctsentence=correctsentence+i + "\t"
        else:
            correctsentence = correctsentence + i
        counter=counter+1
    #print(correctsentence)
    f.write(correctsentence+"\n" )
file.close()
f.close()
