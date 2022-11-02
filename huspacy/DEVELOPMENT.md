## Install dependencies

Make sure you have poetry installed, then issue: `poetry install --with docs --with dev`

## Release steps

1. Make sure all tests pass: `poetry run pytest`
2. Test README.md code snippets: `poetry run pytest --codeblocks --verbosity=3 ./README.md`
3. Bump version: `poetry run bumpversion --new-version NEW_VERSION --verbose major/minor/patch`
4. Build wheel: `poetry build -f wheel`
5. Publish on PyPI: `poetry publish`
6. Publish on GitHub: `VERSION=$(cat .bumpversion.cfg | grep "current_version =" | cut -c 19-) gh release create huspacy-v$VERSION dist/huspacy-$VERSION-py3-none-any.whl -t huspacy-v$VERSION`