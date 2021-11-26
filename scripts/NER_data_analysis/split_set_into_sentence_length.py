
"""dividing a given corpus 'test' or 'dev' set into arbitrary sentence lengths"""

### input: .iob file ###
### output: .iob files ###

with open("../test.iob", "r", encoding="utf-8") as f:
    test_split = f.readlines()


very_low = list()
very_very_low = list()
low = list()
med = list()
high = list()
current = ""
counter = 0
counter_len = ""

for i in range(len(test_split)):
    if test_split[i] != "\n":
        current += test_split[i]
        counter += 1
    else:
        current += "\n"
        if counter <= 5:
            with open("test/test_very_very_low.iob", "a", encoding="utf-8") as f:
                f.write(current)

            current = current.split("\n")
            current = current[:-2]
            for j in range(len(current)):
                counter_len += current[j].split("\t")[0] + " "

            very_very_low.append(counter_len)
            current = ""
            counter_len = ""
            counter = 0

            continue
        if 5 < counter and counter <= 10:
            with open("test/test_very_low.iob", "a", encoding="utf-8") as f:
                f.write(current)

            current = current.split("\n")
            current = current[:-2]
            for j in range(len(current)):
                counter_len += current[j].split("\t")[0] + " "

            very_low.append(counter_len)
            current = ""
            counter_len = ""
            counter = 0

            continue
        if 10 < counter and counter <= 25:
            with open("test/test_low.iob", "a", encoding="utf-8") as f:
                f.write(current)

            current = current.split("\n")
            current = current[:-2]
            for j in range(len(current)):
                counter_len += current[j].split("\t")[0] + " "

            low.append(counter_len)
            current = ""
            counter_len = ""
            counter = 0

            continue
        if 25 < counter and counter <= 50:
            with open("test/test_med.iob", "a", encoding="utf-8") as f:
                f.write(current)

            current = current.split("\n")
            current = current[:-2]
            for j in range(len(current)):
                counter_len += current[j].split("\t")[0] + " "

            med.append(counter_len)
            current = ""
            counter_len = ""
            counter = 0

            continue
        if 50 < counter:
            with open("test/test_high.iob", "a", encoding="utf-8") as f:
                f.write(current)

            current = current.split("\n")
            current = current[:-2]
            for j in range(len(current)):
                counter_len += current[j].split("\t")[0] + " "

            high.append(counter_len)
            current = ""
            counter_len = ""
            counter = 0

            continue

print("very_very_low =>5", len(very_low))
print("5 < very_low <= 10", len(very_low))
print("10 < low <= 25 ", len(low))
print("25 < med <= 50 ", len(med))
print("high: 50< ", len(high))
