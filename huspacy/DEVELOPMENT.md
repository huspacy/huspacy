## Install dependencies

Make sure you have poetry installed, then issue: `poetry install`

## Release steps

1. Make sure all tests pass: `poetry run pytest`
2. Test README.md code snippets: `poetry run pytest --codeblocks --verbosity=3 ./README.md`
3. Bump version: `poetry run bumpversion --new-version NEW_VERSION --verbose major/minor/patch`
4. Build wheel: `poetry build -f wheel`
5. Publish on PyPI: `poetry publish`