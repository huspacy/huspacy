# Release steps

1. Build docs: `poetry run lazydocs docs ../spacy-hungarian-models/huspacy/ --src-base-url https://github.com/huspacy/huspacy/blob/master --no-watermark --no-remove-package-prefix --validate`
2. Test README.md code snippets: `poetry run pytest --codeblocks --verbosity=3 ./README.md`
3. Bump version: `poetry run bumpversion --new-version NEW_VERSION --verbose $PART`
4. Build wheel: `poetry build -f wheel`
5. Publish on PyPI: `poetry publish`