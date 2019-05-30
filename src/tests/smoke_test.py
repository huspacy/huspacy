import hu_core_ud_lg

nlp = hu_core_ud_lg.load()

print([
    (tok.text, tok.lemma_, tok.pos_, tok.tag_, tok.dep_, tok.head.text)
    for tok in nlp('Józsiék házainak szépek az ablakaik.')
])
