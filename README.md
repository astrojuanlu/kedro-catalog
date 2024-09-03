# kedro-catalog

[![Documentation Status](https://readthedocs.org/projects/kedro-catalog/badge/?version=latest)](https://kedro-catalog.readthedocs.io/en/latest/?badge=latest)
[![Code style: ruff-format](https://img.shields.io/badge/code%20style-ruff_format-6340ac.svg)](https://github.com/astral-sh/ruff)
[![PyPI](https://img.shields.io/pypi/v/kedro-catalog)](https://pypi.org/project/kedro-catalog)

Prototype of a next-generation DataCatalog for Kedro.

Niceties:
- Basic dataset loading
- Basic factory resolution
- Catalog items are lazily loaded ([#2829](https://github.com/kedro-org/kedro/issues/2829))
- Creating custom datasets is easier ([#1936](https://github.com/kedro-org/kedro/issues/1936))
- It gets trivially represented on REPLs ([#1721](https://github.com/kedro-org/kedro/issues/1721))
- Has public API to retrieve dataset objects ([#1778](https://github.com/kedro-org/kedro/issues/1778#issuecomment-1728079791))
- ...which in turn have public properties ([#3929](https://github.com/kedro-org/kedro/issues/3929))
- No ABCs are needed because there's no shared logic, only Protocols ([#4138](https://github.com/kedro-org/kedro/issues/4138))

The codebase is lean and makes heavy use of `@dataclass` and Pydantic models. I'm no software engineer so I'm not claiming it's well designed, but hopefully it's easy to understand (and therefore criticise).

Of course, it's tiny because it leaves lots of things out of the table. It critically does not support:

- Versions. But, are they really needed? [#4129](https://github.com/kedro-org/kedro/issues/4129),
  [#2355](https://github.com/kedro-org/kedro/issues/2355))
- Credentials. But, shouldn't we rework them completely already? [#3811](https://github.com/kedro-org/kedro/issues/3811))
- Mutability. But doesn't it send the wrong message? [#2728](https://github.com/kedro-org/kedro/issues/2728))

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
