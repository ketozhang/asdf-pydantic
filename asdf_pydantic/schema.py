from typing import Optional

from pydantic.json_schema import GenerateJsonSchema

DEFAULT_ASDF_SCHEMA_REF_TEMPLATE = "#/definitions/{model}"


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
            json_schema["id"] = self.tag_uri
            json_schema["tag"] = f"tag:{self.tag_uri.split('://', maxsplit=2)[-1]}"

        # TODO: Convert jsonschema 2020-12 to ASDF schema
        return json_schema
