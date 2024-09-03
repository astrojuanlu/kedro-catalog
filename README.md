# kedro-catalog

[![Documentation Status](https://readthedocs.org/projects/kedro-catalog/badge/?version=latest)](https://kedro-catalog.readthedocs.io/en/latest/?badge=latest)
[![Code style: ruff-format](https://img.shields.io/badge/code%20style-ruff_format-6340ac.svg)](https://github.com/astral-sh/ruff)
[![PyPI](https://img.shields.io/pypi/v/kedro-catalog)](https://pypi.org/project/kedro-catalog)

Prototype of a next-generation DataCatalog for Kedro.

Niceties:
- Basic dataset loading
- Basic factory resolution
- Lazy loading of catalog items ([#2829](https://github.com/kedro-org/kedro/issues/2829))
- Easy custom dataset creation ([#1936](https://github.com/kedro-org/kedro/issues/1936))
- Lean, easy to understand codebase
- No ABCs

It does not support:
- Versions (are they needed? [#4129](https://github.com/kedro-org/kedro/issues/4129),
  [#2355](https://github.com/kedro-org/kedro/issues/2355))
- Credentials (should we rework them completely? [#3811](https://github.com/kedro-org/kedro/issues/3811))
- Mutability (does it send the wrong message? [#2728](https://github.com/kedro-org/kedro/issues/2728))

## Usage

```python
In [1]: catalog_config = {
   ...:     "ds1": {
   ...:         "type": "polars.CSVDataset",
   ...:         "filepath": "iris.csv",
   ...:     },
   ...:     "ds_{name}": {
   ...:         "type": "polars.CSVDataset",
   ...:         "filepath": "{name}.csv",
   ...:     },
   ...: }

In [2]: from kedro_catalog import DataCatalog

In [3]: catalog = DataCatalog.from_config(catalog_config)
   ...: catalog
Out[3]: DataCatalog(_dataset_configs={...}, _resolver=FactoryResolver())

In [4]: catalog.load("ds1").head(1)
Out[4]:
shape: (1, 5)
┌──────────────┬─────────────┬──────────────┬─────────────┬─────────┐
│ sepal_length ┆ sepal_width ┆ petal_length ┆ petal_width ┆ species │
│ ---          ┆ ---         ┆ ---          ┆ ---         ┆ ---     │
│ f64          ┆ f64         ┆ f64          ┆ f64         ┆ str     │
╞══════════════╪═════════════╪══════════════╪═════════════╪═════════╡
│ 5.1          ┆ 3.5         ┆ 1.4          ┆ 0.2         ┆ setosa  │
└──────────────┴─────────────┴──────────────┴─────────────┴─────────┘

In [5]: catalog.load("ds_iris").head(1)
Out[5]:
shape: (1, 5)
┌──────────────┬─────────────┬──────────────┬─────────────┬─────────┐
│ sepal_length ┆ sepal_width ┆ petal_length ┆ petal_width ┆ species │
│ ---          ┆ ---         ┆ ---          ┆ ---         ┆ ---     │
│ f64          ┆ f64         ┆ f64          ┆ f64         ┆ str     │
╞══════════════╪═════════════╪══════════════╪═════════════╪═════════╡
│ 5.1          ┆ 3.5         ┆ 1.4          ┆ 0.2         ┆ setosa  │
└──────────────┴─────────────┴──────────────┴─────────────┴─────────┘
```

## Installation

To install, run

```
$ uv pip install kedro-catalog
```

## Development

To run style checks:

```
$ uv tool install pre-commit
$ pre-commit run -a
```
