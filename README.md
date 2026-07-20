<span align="center">

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![tests](https://github.com/billwallis/cachetronaut/actions/workflows/tests.yaml/badge.svg)](https://github.com/billwallis/cachetronaut/actions/workflows/tests.yaml)
[![coverage](https://raw.githubusercontent.com/billwallis/cachetronaut/refs/heads/main/coverage.svg)](https://smarie.github.io/python-genbadge/)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/billwallis/cachetronaut/main.svg)](https://results.pre-commit.ci/latest/github/billwallis/cachetronaut/main)
[![GitHub last commit](https://img.shields.io/github/last-commit/billwallis/cachetronaut)](https://shields.io/badges/git-hub-last-commit)

</span>

---

# Cachetronaut

Utilities for long-lived caches.

## Installation

Install directly from source:

```shell
pip install cachetronaut@git+https://github.com/billwallis/cachetronaut@v0.0.1
```

## Usage

Currently, this exposes a single decorator, `file_cache`, which takes a filepath and a timedelta expiration:

```python
import datetime
import pathlib

import cachetronaut

@cachetronaut.file_cache(
    filepath=pathlib.Path("path/to/file.pickle"),
    expiration=datetime.timedelta(hours=1),
)
def some_expensive_computation():
    # do expensive thing
    return expensive_result
```

The decorator uses [pickle](https://docs.python.org/3/library/pickle.html) to write the result to a file, hence the `.pickle` extension in the example above -- but you can use whatever extension you want.

The cached files will not be deleted without replacement. If a cached file has "expired", this will only mean that it will be regenerated at runtime prior to being used.

## Contributing

Install the dependencies:

```shell
python -m venv .venv/
source .venv/bin/activate
pip install poethepoet

poe install
```
