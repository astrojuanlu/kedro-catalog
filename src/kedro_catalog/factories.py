from dataclasses import dataclass

from parse import parse

from .datasets import DatasetConfig


def resolve_dataset_config(
    config: DatasetConfig, vars: dict[str, str]
) -> DatasetConfig:
    new_type = config.type.format(**vars)
    # TODO: Recursively resolve nested specs
    new_spec = {
        key: value.format(**vars) if isinstance(value, str) else value
        for key, value in config.spec.items()
    }
    return DatasetConfig(type=new_type, **new_spec)


@dataclass
class FactoryResolver:
    def resolve(
        self, target_name: str, dataset_configs: dict[str, DatasetConfig]
    ) -> DatasetConfig:
        for name, dataset_config in dataset_configs.items():
            result = parse(name, target_name)
            if result:
                break
        else:
            raise ValueError("No matching dataset found")

        return resolve_dataset_config(dataset_config, result.named)
