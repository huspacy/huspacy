There can be cases when the default four-type NER does not suffice, one needs a more fine-grained entity type system.
Attila Novak developed a [corpus](https://github.com/novakat/NYTK-NerKor-Cars-OntoNotesPP) and an [entity recognition system](https://huggingface.co/novakat/nerkor-cars-onpp-hubert) consisting more than 30 entity types. We provide easy
integration with his tool.

## Load

Loading the model can be achieved by adding the `nerpp` component.

```python
import huspacy
import huspacy.components

# Load the default lexicon
nlp = huspacy.load("hu_core_news_lg")
nlp.add_pipe("nerpp")
```
Please note that using this component requires `transformers`, `torch` and `spacy-alignments` to be installed.
Installing HuSpaCy with `trf` extras automates this step:

```bash
$ pip install huspacy[trf]
```

## Get entity annotations

The `nerpp` components stores entities as spans on the document under the `"ents"` key:

```python
doc = nlp("A Ford Focus egy alsó-középkategóriás családi autó")
print(doc.spans["ents"]) # ["Ford Focus"]
print(doc.spans["ents"][0].label_) # "CAR"
```
## Citing
If you use this component, please cite:

```bibtex
@InProceedings{novak-novak:2022:LREC,
  author    = {Nov{\'{a}}k, Attila  and  Nov{\'{a}}k, Borb{\'{a}}la},
  title     = {NerKor+Cars-OntoNotes++},
  booktitle      = {Proceedings of the 13th Language Resources and Evaluation Conference (LREC 2022)},
  month          = {June},
  year           = {2022},
  address        = {Marseille, France},
  publisher      = {European Language Resources Association},
  pages     = {1907--1916},
    url       = {http://www.lrec-conf.org/proceedings/lrec2022/pdf/2022.lrec-1.203.pdf}
}
```

