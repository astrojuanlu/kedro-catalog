import typing as t

from pydantic import BaseModel, model_serializer, model_validator

DatasetSpec: t.TypeAlias = dict[str, t.Any]


class DatasetConfig(BaseModel):
    type: str
    spec: DatasetSpec

    @model_validator(mode="before")
    @classmethod
    def validate_model(cls, data: t.Any) -> t.Any:
        data = data.copy()
        dataset_type = data.pop("type")
        return {
            "type": dataset_type,
            "spec": data,
        }

    @model_serializer
    def serialize_model(self) -> dict[str, t.Any]:
        return {
            "type": self.type,
            **self.spec,
        }


class DatasetProtocol(t.Protocol):
    @classmethod
    def from_spec(cls, spec: DatasetSpec) -> ...: ...

    def load(self) -> ...: ...

    def save(self, data: ...) -> None: ...
