# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
from jsonschema import ValidationError


class ConfigValidationException(ValidationError):
    @classmethod
    def from_exc(cls, exc):
        return cls(
            message=exc.message,
            validator=exc.validator,
            path=exc.path,
            cause=exc.cause,
            context=exc.context,
            validator_value=exc.validator_value,
            instance=exc.instance,
            schema=exc.schema,
            schema_path=exc.schema_path,
            parent=exc.parent,
        )


class InvalidInputException(Exception):
    pass
