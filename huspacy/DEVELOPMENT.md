# Generating docs

```bash
lazydocs docs ../spacy-hungarian-models/huspacy/ --src-base-url https://github.com/huspacy/huspacy/blob/master --no-watermark --no-remove-package-prefix --validate
```

# Creating a release

```bash
bumpversion --new-version NEW_VERSION --verbose $PART 
poetry build -f wheel
poetry publish
```