"""

## Adding existing ASDF tags as a field
Type annotation must be added to the field to specify the ASDF tag to use in the
ASDF schema. There are a few options to do this:

    - Use `AsdfTag` to specify the tag URI.
    - Use `WithAsdfSchema` and pass in a dictionary to extend the schema with
    additional properties. The key `"$ref"` can be used to specify the tag URI.

    from asdf_pydantic import AsdfPydanticModel
    from asdf_pydantic.schema import AsdfTag
    from astropy.table import Table

    class MyModel(AsdfPydanticModel):
        table: Annotated[Table, AsdfTag("http://stsci.edu/schemas/asdf.org/table/table-1.1.0")]

For more customization of the ASDF schema output, you can use `WithAsdfSchema` to
extend the schema with additional properties.

    # Changing the title of the field
    table: Annotated[
        Table,
        WithAsdfSchema({
            "title": "TABLE",
            "$ref": "http://stsci.edu/schemas/asdf.org/table/table-1.1.0"
        }),
    ]
"""

from typing import Literal, Optional

from pydantic import WithJsonSchema
from pydantic.json_schema import GenerateJsonSchema

DEFAULT_ASDF_SCHEMA_REF_TEMPLATE = "#/definitions/{model}"
DESIRED_ASDF_SCHEMA_KEY_ORDER = (
    "$schema",
    "id",
    "title",
    "type",
    "properties",
    "allOf",
    "anyOf",
    "required",
    "definitions",
)


class GenerateAsdfSchema(GenerateJsonSchema):
    """Generates ASDF-compatible schema from Pydantic's default JSON schema generator.

    ```{caution} Experimental
    This schema generator is not complete. It currently creates JSON 2020-12
    schema (despite `$schema` says it's `asdf-schema-1.0.0`) which are not
    compatible with ASDF.
    ```
    """

    # HACK: When we can support tree models, then not all schema should have tag
    schema_dialect = "http://stsci.edu/schemas/asdf/asdf-schema-1.0.0"

    def __init__(
        self,
        by_alias: bool = True,
        ref_template: str = DEFAULT_ASDF_SCHEMA_REF_TEMPLATE,
        tag_uri: Optional[str] = None,
    ):
        super().__init__(by_alias=by_alias, ref_template=ref_template)
        self.tag_uri = tag_uri

    def generate(self, schema, mode="validation"):
        json_schema = super().generate(schema, mode)  # noqa: F841

        if self.tag_uri:
            json_schema["$schema"] = self.schema_dialect
            json_schema["id"] = f"{self.tag_uri}/schema"

        # TODO: Convert jsonschema 2020-12 to ASDF schema
        if "$defs" in json_schema:
            json_schema["definitions"] = json_schema.pop("$defs")

        # Order keys
        json_schema = {
            **{
                key: json_schema[key]
                for key in DESIRED_ASDF_SCHEMA_KEY_ORDER
                if key in json_schema
            },
            **json_schema,  # Rest of the keys not in order list
        }

        return json_schema


class WithAsdfSchema(WithJsonSchema):
    def __init__(self, asdf_schema: dict, **kwargs):
        super().__init__(asdf_schema, **kwargs)


def AsdfTag(tag: str, mode: Literal["auto", "ref", "tag"] = "auto") -> WithAsdfSchema:
    if mode == "auto":
        parsed_mode = "tag" if tag.startswith("tag") else "ref"
    else:
        parsed_mode = mode

    if parsed_mode == "tag":
        return WithAsdfSchema({"tag": tag})
    else:
        return WithAsdfSchema({"$ref": tag})
