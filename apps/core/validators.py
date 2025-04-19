from typing import Protocol
import magic
from django.core.exceptions import ValidationError


class PFile(Protocol):
    def read(self, *args, **kwargs) -> bytes:
        ...


class FileTypeValidator:
    def __init__(self, allowed_types: list[str]):
        self._allowed_types = allowed_types

    def __call__(self, value):
        file_type_validator(value, self._allowed_types)


def file_type_validator(file_field: PFile, allowed_types: list[str]):
    file_type = magic.from_buffer(file_field.read(), mime=True)

    if file_type not in allowed_types:
        raise ValidationError(
            f"Unsupported file type. Only the following formats are are allowed: {','.join(allowed_types)}."
        )


def clean_document_fields(value: PFile):
    if value:
        file_type_validator(value, ["application/pdf"])


def clean_image_fields(value: PFile):
    if value:
        file_type_validator(
            value,
            [
                "image/jpg",
                "image/jpeg",
                "image/png",
                "image/webp",
            ],
        )
