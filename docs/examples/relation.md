# Relation Extraction

By using a set of simplerules, we can extract an ordered sequence of subject-verb-object triples from a document or sentence. For example, in the sentence "Anna éppen házat épít magának." (Anna builds a house for herself.) "Anna" will be the subject, "épít" will be the verb, and the "ház" will be the object. This triple will be an extracted relation. Using HuSpaCy for tagging and dependency parsing and the modified code for extraction, we can make a simple relaction extraction tool.

## Importing and using HuSpaCy

```python
nlp = spacy.load("hu_core_news_trf")
doc = nlp("Anna éppen házat épít magának.")
```

## Extraction SVO triples

```python
def subject_verb_object_triples(doclike: types.DocLike) -> Iterable[SVOTriple]:
    if isinstance(doclike, Span):
        sents = [doclike]
    else:
        sents = doclike.sents

    for sent in sents:
        # connect subjects/objects to direct verb heads
        # and expand them to include conjuncts, compound nouns, ...
        verb_sos = collections.defaultdict(lambda: collections.defaultdict(set))
        for tok in sent:
            head = tok.head
            # ensure entry for all verbs, even if empty
            # to catch conjugate verbs without direct subject/object deps
            if tok.pos == VERB:
                _ = verb_sos[tok]
            # nominal subject of active or passive verb
            if tok.dep in _NOMINAL_SUBJ_DEPS:
                if head.pos == VERB:
                    verb_sos[head]["subjects"].update(expand_noun(tok))
            # clausal subject of active or passive verb
            elif tok.dep in _CLAUSAL_SUBJ_DEPS:
                if head.pos == VERB:
                    verb_sos[head]["subjects"].update(tok.subtree)
            # nominal direct object of transitive verb
            elif tok.dep == obj:
                if head.pos == VERB:
                    verb_sos[head]["objects"].update(expand_noun(tok))
            # prepositional object acting as agent of passive verb
            elif tok.dep == pobj:
                if head.dep == agent and head.head.pos == VERB:
                    verb_sos[head.head]["objects"].update(expand_noun(tok))
            # open clausal complement, but not as a secondary predicate
            elif tok.dep == xcomp:
                if (
                    head.pos == VERB
                    and not any(child.dep == obj for child in head.children)
                ):
                    # TODO: just the verb, or the whole tree?
                    # verb_sos[verb]["objects"].update(expand_verb(tok))
                    verb_sos[head]["objects"].update(tok.subtree)
        # fill in any indirect relationships connected via verb conjuncts
        for verb, so_dict in verb_sos.items():
            conjuncts = verb.conjuncts
            if so_dict.get("subjects"):
                for conj in conjuncts:
                    conj_so_dict = verb_sos.get(conj)
                    if conj_so_dict and not conj_so_dict.get("subjects"):
                        conj_so_dict["subjects"].update(so_dict["subjects"])
            if not so_dict.get("objects"):
                so_dict["objects"].update(
                    obj
                    for conj in conjuncts
                    for obj in verb_sos.get(conj, {}).get("objects", [])
                )
        # expand verbs and restructure into svo triples
        for verb, so_dict in verb_sos.items():
            if so_dict["subjects"] and so_dict["objects"]:
                yield SVOTriple(
                    subject=sorted(so_dict["subjects"], key=attrgetter("i")),
                    verb=sorted(expand_verb(verb), key=attrgetter("i")),
                    object=sorted(so_dict["objects"], key=attrgetter("i")),
                )
```

The function with all it's dependencies is available on [GitHub](https://github.com/huspacy/example-applications/blob/main/resources/triples.py).

## Extracting the triples

```python
tuples = subject_verb_object_triples(doc)
```

## Presenting the data

```python
for sub_multiple in tuples[0][0]:
    subject += str(sub_multiple) + ", "
subject = subject[:-2]
for verb_multiple in tuples[0][1]:
    verb += str(verb_multiple) + ", "
verb = verb[:-2]
for obj_multiple in tuples[0][2]:
    object += str(obj_multiple) + ", "
object = object[:-2]

relation_list = [[subject, verb, object]]

df = pd.DataFrame(relation_list, columns=['Subject', 'Verb', 'Object'])
```

## Notes

The method presented above is heavily based on Textacy[¹]'s similar method. We slightly modified to adapt for Hungarian. You can find the full extraction method [here](https://github.com/huspacy/example-applications/blob/main/resources/triples.py).

This example is available on [Hugging Face Spaces](https://huggingface.co/spaces/huspacy/example-applications). The full source code is on [GitHub](https://github.com/huspacy/example-applications/blob/main/examples/relation.py).

[¹]: https://github.com/chartbeat-labs/textacy
