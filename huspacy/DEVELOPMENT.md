# Release steps

1. Test README.md code snippets: `poetry run pytest --codeblocks --verbosity=3 ./README.md`
2. Bump version: `poetry run bumpversion --new-version NEW_VERSION --verbose $PART`
3. Build wheel: `poetry build -f wheel`
4. Publish on PyPI: `poetry publish`