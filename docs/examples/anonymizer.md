# Text Anonymization

Using Presidio[¹] and Faker[²], we can easily make a simple text anonymization tool or PII (Personally Identifiable Information) removal tool. The (hu)spaCy integration of Presidio can be used to identify and remove personal data, such as names, locations, phone numbers, or even bank details. This tool uses (hu)spaCy's Named Entity Recognition facilities and further pattern matching rules. What is more, an easy-to-use de-identification method is provided by Faker as we show below.

## Initializing Presidio with HuSpaCy

### Option 1: using only model names

```python
// Here we use the hu_core_news_lg model, but any model supporting NER is a valid option
configuration = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "hu", "model_name": "hu_core_news_lg", }],
}

provider = NlpEngineProvider(nlp_configuration=configuration)
nlp_engine = provider.create_engine()

analyzer = AnalyzerEngine(nlp_engine=nlp_engine,
                            supported_languages=["hu"],)
```

### Option 2: Building on a previously initialized `nlp` 

```python
class HuSpaCyNlpEngine(SpacyNlpEngine):
    def __init__(self, nlp: Language):
        self.nlp = {"hu": nlp}


def process():
    nlp = spacy.load("hu_core_news_trf")

    nlp_engine = HuSpaCyNlpEngine(nlp)

    analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["hu"])
```

## Configuring Faker operators

```python
fake = Faker(locale=["hu_HU"])

fake_operators = {
    "PERSON": OperatorConfig("custom", {"lambda": lambda x: fake.name()}),
    "LOCATION": OperatorConfig("custom", {"lambda": lambda x: fake.address()}),
    "EMAIL_ADDRESS": OperatorConfig("custom", {"lambda": lambda x: fake.email()}),
    "PHONE_NUMBER": OperatorConfig("custom", {"lambda": lambda x: fake.phone_number()}),
    "CRYPTO": OperatorConfig("custom", {"lambda": lambda x: fake.password()}),
    "IP_ADDRESS": OperatorConfig("custom", {"lambda": lambda x: fake.ipv4()}),
    "URL": OperatorConfig("custom", {"lambda": lambda x: fake.url()}),
    "DATE_TIME": OperatorConfig("custom", {"lambda": lambda x: fake.date()}),
    "CREDIT_CARD": OperatorConfig("custom", {"lambda": lambda x: fake.credit_card_number()}),
    "IBAN_CODE": OperatorConfig("custom", {"lambda": lambda x: fake.iban()}),
}
```

## Applying Presidio's anonymizer with Faker

```python
anonymizer = AnonymizerEngine()
anonymized_text = anonymizer.anonymize(text=text, analyzer_results=results, operators=fake_operators)
```

This example is available on [Hugging Face Spaces](https://huggingface.co/spaces/huspacy/example-applications), while the full source code is on [GitHub](https://github.com/huspacy/example-applications/blob/main/examples/anon.py).

[¹]: https://github.com/microsoft/presidio
[²]: https://github.com/joke2k/faker
