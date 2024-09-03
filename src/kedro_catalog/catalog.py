from __future__ import annotations

import typing as t
from dataclasses import dataclass

from .datasets import DatasetConfig, DatasetProtocol
from .factories import FactoryResolver


def find_dataset_class(dataset_type: str) -> type[DatasetProtocol]:
    # FIXME: This is a hack, the logic could be mostly copied from Kedro
    if dataset_type == "polars.CSVDataset":
        from .csv import CSVDataset

        return CSVDataset

    raise NotImplementedError(f"Dataset type {dataset_type} is not supported")


class DataCatalogProtocol(t.Protocol):
    @classmethod
    def from_config(cls, config: dict[str, dict[str, t.Any]]) -> ...: ...

    def load(self, name: str) -> t.Any: ...

    def save(self, name: str, data: t.Any) -> None: ...


@dataclass
class DataCatalog:
    _dataset_configs: dict[str, DatasetConfig]
    _resolver: FactoryResolver = FactoryResolver()

    @classmethod
    def from_config(cls, config: dict[str, dict[str, t.Any]]) -> DataCatalog:
        dataset_configs = {
            name: DatasetConfig.model_validate(dataset_config)
            for name, dataset_config in config.items()
        }

        # This performs eager instantiation, which we want to defer!
        # https://github.com/kedro-org/kedro/issues/2829
        # datasets = {
        #     name: find_dataset_class(dataset_config.type).from_spec(
        #         dataset_config.specxy
        #     )
        #     for name, dataset_config in dataset_configs.items()
        # }

        # Alternatively, we could find all the dataset classes already,
        # but that might trigger expensive imports
        # dataset_proxys = {
        #     name: (find_dataset_class(dataset_config.type), dataset_config.spec)
        #     for name, dataset_config in dataset_configs.items()
        # }

        # We just store the validated configs instead
        return cls(dataset_configs)

    def get_dataset(self, name: str) -> DatasetProtocol:
        # NOTE: This could be a cached, maybe with @lru_cache
        # but will that mean that datasets stay in memory for longer?
        # Might need to use weakrefs or get smart
        if name in self._dataset_configs:
            dataset_config = self._dataset_configs[name]
        else:
            dataset_config = self._resolver.resolve(name, self._dataset_configs)

        ds_class, spec = find_dataset_class(dataset_config.type), dataset_config.spec
        return ds_class.from_spec(spec)

    def load(self, name: str) -> t.Any:
        return self.get_dataset(name).load()

    def save(self, name: str, data: t.Any) -> None:
        self.get_dataset(name).save(data)
