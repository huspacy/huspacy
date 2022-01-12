"""visualization with ipymarkup"""

from ipymarkup import format_span_line_markup
from ipymarkup.palette import palette, BLUE, RED, GREEN, ORANGE, Palette

with open("../../iob_outputs_from_html/emBERT_eval/diff_v5.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

ents = list()
spans = list()
text = ""

with open("../../iob_outputs_from_html/emBERT_eval/html_file_all.html", "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html><html lang="hu"><head><title>ipymarkup</title><meta charset="UTF-8"></head><body style="font-size: 16px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; padding: 4rem 2rem; direction: ltr">""")

for i in range(len(lines)):
    if lines[i] != "\n":
        if "\t" not in lines[i]:
            text = lines[i]
        else:
            ents.append(lines[i])
    else:
        count = 0
        for ent in range(len(ents)):
            if ents[ent].split("\t")[1] != "O":
                gold = ents[ent].split("\t")[1]
            else:
                gold = ents[ent].split("\t")[1]
            if ents[ent].split("\t")[2] != "O":
                spacy = ents[ent].split("\t")[2]
            else:
                spacy = ents[ent].split("\t")[2]
            if ents[ent].split("\t")[3] != "O":
                bert = ents[ent].split("\t")[3]
            else:
                bert = ents[ent].split("\t")[3]

            start_pos = ents[ent].split("\t")[4]
            end_pos = ents[ent].split("\t")[5][:-1]
            if gold != "O":
                gold_tuple = ""

                # if text == "Az Arrabona Futsal Club 2007-ben jutott fel az élvonalba, majd két év múlva már Duna Takarék-ETO néven szerepelt a hazai NB I-ben. \n":
                #     alma = 42
                current_gold = gold.split("-")[1]
                if len(ents) >= ent + 2:
                    if ents[ent].split("\t")[1].startswith("B-") and ents[ent + 1].split("\t")[1].startswith("I-") \
                            and current_gold == ents[ent + 1].split("\t")[1].split("-")[1]:
                        for_count = count
                        while for_count <= len(ents) - 2:
                            if ents[for_count + 1].split("\t")[1].startswith("I-") and current_gold ==\
                                    ents[for_count + 1].split("\t")[1].split("-")[1]:
                                end_pos = ents[for_count + 1].split("\t")[5][:-1]
                            else:
                                break
                            for_count += 1
                        gold_tuple = (int(start_pos), int(end_pos), gold.split("-")[1] + "-G")
                        spans.append(gold_tuple)

                if len(ents) >= ent + 2:
                    if ents[ent].split("\t")[1].startswith("B-") and ents[ent + 1].split("\t")[1].startswith("B-"):
                        gold_tuple = (int(start_pos), int(end_pos), gold.split("-")[1] + "-G")
                        spans.append(gold_tuple)
                    elif ents[ent].split("\t")[1].startswith("B-") and ents[ent + 1].split("\t")[1].startswith("O"):
                        gold_tuple = (int(start_pos), int(end_pos), gold.split("-")[1] + "-G")
                        spans.append(gold_tuple)
                    if ents[ent].split("\t")[1].startswith("I-") and ents[ent + 1].split("\t")[1].startswith("B-"):
                        pass
                    if ents[ent].split("\t")[1].startswith("I-") and ents[ent + 1].split("\t")[1].startswith("I-"):
                        pass

                elif len(ents) < ent + 2 and ents[ent].split("\t")[1].startswith("B-"):
                    gold_tuple = (int(start_pos), int(end_pos), gold.split("-")[1] + "-G")
                    spans.append(gold_tuple)

                elif len(ents) < ent + 2 and ents[ent].split("\t")[1].startswith("I-"):
                    pass
            start_pos = ents[ent].split("\t")[4]
            end_pos = ents[ent].split("\t")[5][:-1]
            if spacy != "O":
                spacy_tuple = ""

                if text == "A Lakers-Sixers-Spurs-Rockets versenyfutás győztese a Los Angeles lett, LeBron 2018 júliusában aláírt egy négyéves, 154 millió dollárt érő szerződést. \n":
                    alma = 42

                # if len(ents) >= ent + 2:
                #     if ents[ent].split("\t")[1].startswith("B-") and ents[ent + 1].split("\t")[1].startswith("I-"):
                #         for count in range(len(ents) - 1):
                #             if ents[count + 1].split("\t")[1].startswith("I-"):
                #                 end_pos = ents[count + 1].split("\t")[5][:-1]
                #         spacy_tuple = (int(start_pos), int(end_pos), spacy + "-S")
                #         spans.append(spacy_tuple)

                current_spacy = spacy.split("-")[1]
                if len(ents) >= ent + 2:
                    if ents[ent].split("\t")[2].startswith("B-") and ents[ent + 1].split("\t")[2].startswith("I-") \
                            and current_spacy == ents[ent + 1].split("\t")[2].split("-")[1]:
                        for_count = count
                        while for_count <= len(ents) - 2:
                            if ents[for_count + 1].split("\t")[2].startswith("I-") and current_spacy == \
                                    ents[for_count + 1].split("\t")[2].split("-")[1]:
                                end_pos = ents[for_count + 1].split("\t")[5][:-1]
                            else:
                                break
                            for_count += 1
                        spacy_tuple = (int(start_pos), int(end_pos), spacy.split("-")[1] + "-S")
                        spans.append(spacy_tuple)

                if len(ents) >= ent + 2:
                    if ents[ent].split("\t")[2].startswith("B-") and ents[ent + 1].split("\t")[2].startswith("B-"):
                        spacy_tuple = (int(start_pos), int(end_pos), spacy.split("-")[1] + "-S")
                        spans.append(spacy_tuple)
                    elif ents[ent].split("\t")[2].startswith("B-") and ents[ent + 1].split("\t")[2].startswith("O"):
                        spacy_tuple = (int(start_pos), int(end_pos), spacy.split("-")[1] + "-S")
                        spans.append(spacy_tuple)
                    if ents[ent].split("\t")[2].startswith("I-") and ents[ent + 1].split("\t")[2].startswith("B-"):
                        pass
                    if ents[ent].split("\t")[2].startswith("I-") and ents[ent + 1].split("\t")[2].startswith("I-"):
                        pass

                elif len(ents) < ent + 2 and ents[ent].split("\t")[2].startswith("B-"):
                    spacy_tuple = (int(start_pos), int(end_pos), spacy.split("-")[1] + "-S")
                    spans.append(spacy_tuple)

                elif len(ents) < ent + 2 and ents[ent].split("\t")[2].startswith("I-"):
                    pass
            start_pos = ents[ent].split("\t")[4]
            end_pos = ents[ent].split("\t")[5][:-1]
            if bert != "O":
                bert_tuple = ""

                if text == "A Lakers-Sixers-Spurs-Rockets versenyfutás győztese a Los Angeles lett, LeBron 2018 júliusában aláírt egy négyéves, 154 millió dollárt érő szerződést. \n":
                    alma = 42

                # if len(ents) >= ent + 2:
                #     if ents[ent].split("\t")[1].startswith("B-") and ents[ent + 1].split("\t")[1].startswith("I-"):
                #         for count in range(len(ents) - 1):
                #             if ents[count + 1].split("\t")[1].startswith("I-"):
                #                 end_pos = ents[count + 1].split("\t")[5][:-1]
                #         bert_tuple = (int(start_pos), int(end_pos), bert + "-B")
                #         spans.append(bert_tuple)

                current_bert = bert.split("-")[1]
                if len(ents) >= ent + 2:
                    if ents[ent].split("\t")[3].startswith("B-") and ents[ent + 1].split("\t")[3].startswith("I-") \
                            and current_bert == ents[ent + 1].split("\t")[3].split("-")[1]:
                        for_count = count
                        while for_count <= len(ents) - 2:
                            if ents[for_count + 1].split("\t")[3].startswith("I-") and current_bert == \
                                    ents[for_count + 1].split("\t")[3].split("-")[1]:
                                end_pos = ents[for_count + 1].split("\t")[5][:-1]
                            else:
                                break
                            for_count += 1
                        bert_tuple = (int(start_pos), int(end_pos), bert.split("-")[1] + "-B")
                        spans.append(bert_tuple)

                if len(ents) >= ent + 2:
                    if ents[ent].split("\t")[3].startswith("B-") and ents[ent + 1].split("\t")[3].startswith("B-"):
                        bert_tuple = (int(start_pos), int(end_pos), bert.split("-")[1] + "-B")
                        spans.append(bert_tuple)

                    elif ents[ent].split("\t")[3].startswith("B-") and ents[ent + 1].split("\t")[3].startswith("O"):
                        bert_tuple = (int(start_pos), int(end_pos), bert.split("-")[1] + "-B")
                        spans.append(bert_tuple)

                    if ents[ent].split("\t")[3].startswith("I-") and ents[ent + 1].split("\t")[3].startswith("B-"):
                        pass
                    if ents[ent].split("\t")[3].startswith("I-") and ents[ent + 1].split("\t")[3].startswith("I-"):
                        pass

                elif len(ents) < ent + 2 and ents[ent].split("\t")[3].startswith("B-"):
                    bert_tuple = (int(start_pos), int(end_pos), bert.split("-")[1] + "-B")
                    spans.append(bert_tuple)

                elif len(ents) < ent + 2 and ents[ent].split("\t")[3].startswith("I-"):
                    pass
            count += 1

        out = list(format_span_line_markup(text, spans, palette=Palette([BLUE, RED, GREEN], cache={
            "PER-G": BLUE,
            "ORG-G": RED,
            "LOC-G": GREEN,
            "MISC-G": ORANGE,
            "PER-S": BLUE,
            "ORG-S": RED,
            "LOC-S": GREEN,
            "MISC-S": ORANGE,
            "PER-B": BLUE,
            "ORG-B": RED,
            "LOC-B": GREEN,
            "MISC-B": ORANGE,
        }), width=500, line_gap=20, line_width=5, label_size=9, background='white'))
        ents = list()
        spans = list()
        text = ""
        with open("../../iob_outputs_from_html/emBERT_eval/html_file_all.html", "a", encoding="utf-8") as f:
            # f.write("""<!DOCTYPE html><html lang="hu"><head><title>ipymarkup</title><meta charset="UTF-8"></head><body style="font-size: 16px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; padding: 4rem 2rem; direction: ltr">""")
            for line in out:
                f.write(line)
            # f.write("</body></html>")
            f.write("\n")

with open("../../iob_outputs_from_html/emBERT_eval/html_file_all.html", "a", encoding="utf-8") as f:
    f.write("</body></html>")





# text = "Október 26-án, legelső blogposztunk évfordulóján megemlékeztünk arról, hogyan született meg az ötlet, hogy elindítsuk a Global Voices-t."
# entiti1 = "Global"
# start1 = text.find(entiti1)
# end1 = int(start1) + len(entiti1)
#
# entiti2 = "Voices-t"
# start2 = text.find(entiti2)
# end2 = int(start2) + int(len(entiti2))
# spans = [(start1, end1, "B-ORG"), (start2, end2, "I-ORG"), (start1, end2, "KAKI")]

# Global	B-ORG	B-ORG	B-MISC
# Voices-t	I-ORG	I-ORG	I-MISC
# from IPython.display import display, HTML
# from IPython.core.display import HTML