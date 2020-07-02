# Notification System

Implementation of the coding exercise **Notification Simulator**.

## System Dependencies

The requirements are the followings:
    
  - Python 3.8 (I recommend the use of [pyenv](https://github.com/pyenv/pyenv) to manage multiple Python versions
  - [Poetry](https://python-poetry.org/docs/)
  - GNU Make

## Quickstart

The dependencies are managed with [`poetry`](https://python-poetry.org/docs/).

```bash
# Install the dependencies and the package itself in development mode
make install

# run the tests to check everything is ok
make test
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

## Quickstart with Docker

If you don't want to install the dependencies and you have Docker, it's possible
to run the tests and the example script with Docker:

```bash
# build the image
docker build -t notification_system . 

# run the tests
docker run notification_system poetry run pytest --cov

# run the example script
docker run --rm notification_system poetry run python example.py
```

## Execute a example run

The file `example.py` contains the example run described in the exercise
specification. You can execute the script with:

```bash
make example
```

The example creates 1000 users. It also creates and delivers 5 messages to all
of the users. Simulation a loss ratio and an open ratio of the messages.

## Type check and formatting

The project uses `mypy` to check for type errors. To check everything is
correct, simple run:

```bash
make mypy
```

`black` is used to format python code, we recommend format each file for
separate, but if you want for format all the project, run:

```bash
make format
```

If you only want to check that the code is well formatted, but you don't
want to change it, add `--check`.

```bash
make format-check
```

## If this was a real application

If this was a real application, the first thing I would change would be the data 
storage system. Now, the application uses a limited in-memory system. For the
majority of use cases the data source of truth has to be ACID. I would choose Postgres
or MySQL as database backend.

Next, I would add a queue system. The event system is synchronous and in the same
thread. In the future, that could limit the scaling of the application. I would 
integrate something like Redis or RabbitMQ, depending of the requirements, to
process the events. Also, I would refactor the delivery system to deliver messages
using events.
