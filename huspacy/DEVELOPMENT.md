## Repository structure

```
├── .github            -- Github configuration files
├── docs               -- Documentation source files
├── hu_core_news_lg    -- SpaCy 3.x project files for building the large model
│   ├── configs        -- SpaCy pipeline configuration files
│   ├── meta.json      -- model metadata
│   ├── poetry.lock    -- Poetry lock file
│   ├── poetry.toml    -- Poetry configs
│   ├── project.lock   -- Auto-generated project script
│   ├── project.yml    -- SpaCy Project file describing steps needed to build the model
│   ├── pyproject.toml -- Python project definition file
│   ├── CHANGELOG.md   -- Model changelog
│   └── README.md      -- Instructions on building a model from scratch
├── hu_core_news_trf   -- Spacy 3.x project files for building the transformer based model
│   ├── configs        -- SpaCy pipeline configuration files
│   ├── meta.json      -- model metadata
│   ├── poetry.lock    -- Poetry lock file
│   ├── poetry.toml    -- Poetry configs
│   ├── project.lock   -- Auto-generated project script
│   ├── project.yml    -- SpaCy Project file describing steps needed to build the model
│   ├── pyproject.toml -- Python project definition file
│   ├── CHANGELOG.md   -- Model changelog
│   └── README.md      -- Instructions on building a model from scratch
├── hu_vectors_web_lg  -- Spacy 3.x project files for building word vectors
│   ├── configs        -- SpaCy pipeline configuration files
│   ├── poetry.lock    -- Poetry lock file
│   ├── poetry.toml    -- Poetry configs
│   ├── project.lock   -- Auto-generated project script
│   ├── project.yml    -- SpaCy Project file describing steps needed to build the model
│   ├── pyproject.toml -- Python project definition file
│   ├── CHANGELOG.md   -- Model changelog
│   └── README.md      -- Instructions on building a model from scratch
├── huspacy            -- subproject for the PyPI distributable package
│   ├── huspacy        -- huspacy python package
│   ├── tests          -- huspacy tests
│   ├── poetry.lock    -- Poetry lock file
│   ├── poetry.toml    -- Poetry configs
│   ├── pyproject.toml -- Python project definition file
│   ├── CHANGELOG.md   -- HuSpaCy changelog
│   └── README.md      -> ../README.md
├── mkdocs.yml         -- Mkdocs config file
├── scripts            -- CLI scripts
├── LICENSE            -- License file
└── README.md          -- This file

```

## Release steps

First of all, we need all the dependecies installed: `poetry install --with docs --with dev --all-extras`

1. Make sure all tests pass: `poetry run pytest`
2. Update the readme, if there are changes in `docs`: `poetry run docs/update_readme.py`
3. Test README.md code snippets: `poetry run pytest --codeblocks --verbosity=3 ./README.md`
4. Bump version: `poetry run bumpversion --new-version NEW_VERSION --verbose major/minor/patch`
5. Build wheel: `poetry build -f wheel`
6. Publish on PyPI: `poetry publish`
7. Publish on GitHub: `VERSION=$(cat .bumpversion.cfg | grep "current_version =" | cut -c 19-) gh release create huspacy-v$VERSION dist/huspacy-$VERSION-py3-none-any.whl -t huspacy-v$VERSION`