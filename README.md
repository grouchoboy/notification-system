# Notification System

## Quickstart

At the moment the project is empty, but you can install the development
dependencies and run the tests to check that everything is OK.

The dependencies are managed to [`poetry`](https://python-poetry.org/docs/).

```bash
# Install the dependencies and the package itself in development mode
poetry install

# run the tests to check everything is ok
poetry run pytest
```

If you don't have `poetry` installed and don't want to install it, there
is also a `requirements.txt`.

```bash
# create a virtual environment and activate it
python -m venv .venv
source .venv/bin/activate

# install the dependencies
pip install -r requirements.txt

# install the package in development mode
pip install -e .

# run the tests
pytest
```

## Type check and formatting

The project uses `mypy` to check for type errors. To check everything is
correct, simple run:

```bash
poetry run mypy notification_system tests
```

`black` is used to format python code, we recommend format each file for
separate, but if you want for format all the project, run:

```bash
poetry run black notification_system tests
```

If you only want to check that the code is well formatted, but you don't
want to change it, add `--check`.

```bash
poetry run black --check notification_system tests
```
