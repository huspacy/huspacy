    Hungarian multi-task CNN trained on Universal Dependencies (hu_szeged). Assigns context-specific token vectors, Brown cluster IDs, word probabilities, POS tags, dependency parse and lemmata.
    
    
    Feature | Description
    -- | --
    Name | hu_core_ud_lg
    Version | 0.1.0
    spaCy | >=2.0.0
    Model size | 1350 MB
    Pipeline | tokenizer, sentencizer, tagger, parser, lemmatizer
    Vectors | 1140008 unique vectors (300 dimensions)
    Sources | Universal Dependencies, Szeged Corpus, Web Corpus, Wikipedia
    License | CC BY-NC-SA 4.0
    
    ## Pipeline details
    
    &nbsp; | Vectors | Tokenizer | Sentencizer | Tagger | Parser | Lemmatizer 
    -- | -- | -- | -- | -- | -- | -- |
    Model | [Word2Vec CBOW `dim=300` `minfreq=10`](https://github.com/oroszgy/hunlp-resources/releases/tag/webcorpuswiki_word2vec_v0.1) | Rule-based implemented in SpaCy | Rule-based | Multi-task CNN | multi-task CNN | [Lemmy (CST-like)](https://github.com/sorenlind/lemmy/)
    Training data | Wikipedia dump (2017-04-21)) and the [Hungarian Webcorpus](http://mokk.bme.hu/resources/webcorpus/) | - | - | [CONLL'17 training data](https://github.com/UniversalDependencies/UD_Hungarian-Szeged) | [CONLL'17 test data](https://github.com/UniversalDependencies/UD_Hungarian-Szeged) | UD converted Szeged Korpusz
    Test data | [Hungarian analogical questions](http://corpus.nytud.hu/efnilex-vect/data/questions-words-hu.txt) | [CONLL'17 test data](https://github.com/UniversalDependencies/UD_Hungarian-Szeged) | [CONLL'17 test data](https://github.com/UniversalDependencies/UD_Hungarian-Szeged) | [CONLL'17 test data](https://github.com/UniversalDependencies/UD_Hungarian-Szeged) | [CONLL'17 test data](https://github.com/UniversalDependencies/UD_Hungarian-Szeged) | [CONLL'17 test data](https://github.com/UniversalDependencies/UD_Hungarian-Szeged) 
    Accuracy | `ACC` 20.95 | `F1` 99.88 | `F1` 96.64| `ACC` 95.11 | `UAS` 77.52 `LAS` 68.45 | `ACC` 95.60
    
