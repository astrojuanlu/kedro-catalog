from __future__ import annotations

from dataclasses import dataclass

import polars as pl

from kedro_catalog.datasets import DatasetSpec


@dataclass
class CSVDataset:
    filepath: str

    @classmethod
    def from_spec(cls, spec: DatasetSpec) -> CSVDataset:
        return cls(filepath=spec["filepath"])

    def load(self) -> pl.DataFrame:
        return pl.read_csv(self.filepath)

    def save(self, data: pl.DataFrame) -> None:
        data.write_csv(self.filepath)
