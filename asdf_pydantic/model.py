import textwrap
from typing import Any, ClassVar

import numpy as np
import yaml
from asdf.tags.core import NDArrayType
from numpy.typing import NDArray
from pydantic import BaseModel, ValidationInfo, field_validator


class AsdfPydanticModel(BaseModel):
    """

    ASDF Serialization and Deserialization:
        Serialize to ASDF yaml tree is done with the
        py:classmethod`AsdfPydanticModel.asdf_yaml_tree()` and deserialize to an
        AsdfPydanticModel object with py:meth`AsdfPydanticModel.parse_obj()`.
    """

    _tag: ClassVar[str]

    class Config:
        arbitrary_types_allowed = True

    def asdf_yaml_tree(self) -> dict:
        d = {}
        for field_key, v in self.__dict__.items():
            if field_key not in self.__fields__:
                continue

            if isinstance(v, AsdfPydanticModel):
                d[field_key] = v
            else:
                d[field_key] = self._get_value(
                    v,
                    to_dict=True,
                    by_alias=False,
                    include=None,
                    exclude=None,
                    exclude_unset=False,
                    exclude_defaults=False,
                    exclude_none=False,
                )

        return d

    @classmethod
    def schema_asdf(
        cls, *, metaschema: str = "http://stsci.edu/schemas/asdf/asdf-schema-1.0.0"
    ) -> str:
        """Get the ASDF schema definition for this model.

        Parameters
        ----------
        metaschema, optional
            A metaschema URI, by default "http://stsci.edu/schemas/asdf/asdf-schema-1.0.0".
            See https://asdf.readthedocs.io/en/stable/asdf/extending/schemas.html#anatomy-of-a-schema
            for more options.
        """  # noqa: E501
        # TODO: Function signature should follow BaseModel.schema() or
        # BaseModel.schema_json()
        header = textwrap.dedent(
            f"""
            %YAML 1.1
            ---
            $schema: {metaschema}
            id: {cls._tag}
            tag: tag:{cls._tag.split('://', maxsplit=2)[-1]}

            """
        )
        body = yaml.safe_dump(cls.model_json_schema())
        return header + body

    @field_validator("*", mode="before")
    @classmethod
    def _allow_asdf_NDArrayType_to_be_ndarray(
        cls, value: Any, info: ValidationInfo
    ) -> Any | NDArray:
        """Before Pydantic validation, convert ASDF `NDArrayType` to numpy `NDArray`."""
        if not isinstance(value, NDArrayType):
            return value

        return np.asarray(value)
