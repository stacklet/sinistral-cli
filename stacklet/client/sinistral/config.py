# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
"""
Handle configuration for the CLI
"""
import json
import os

from jsonschema import validate
from stacklet.client.sinistral.exceptions import ConfigValidationException

MISSING = "missing"
DEFAULT_PATH = "~/.stacklet/sinistral/config.json"


class StackletConfig:
    schema = {
        "type": "object",
        "properties": {
            "api": {"type": "string"},
            "cognito_user_pool_id": {"type": "string"},
            "cognito_client_id": {"type": "string"},
            "region": {"type": "string"},
            "idp_id": {"type": "string"},
            "auth_url": {"type": "string"},
        },
        "required": [
            "api",
            "cognito_user_pool_id",
            "cognito_client_id",
            "region",
            "auth_url",
        ],
    }

    def __init__(
        self,
        api=None,
        cognito_user_pool_id=None,
        cognito_client_id=None,
        region=None,
        idp_id=None,
        auth_url=None,
    ):
        self.api = api
        self.cognito_user_pool_id = cognito_user_pool_id
        self.cognito_client_id = cognito_client_id
        self.region = region
        self.idp_id = idp_id
        self.auth_url = auth_url

        if not all(
            [self.api, self.cognito_user_pool_id, self.cognito_client_id, self.region]
        ):
            raise ConfigValidationException

    def to_json(self):
        return dict(
            api=self.api,
            cognito_user_pool_id=self.cognito_user_pool_id,
            cognito_client_id=self.cognito_client_id,
            region=self.region,
            idp_id=self.idp_id,
            auth_url=self.auth_url,
        )

    @classmethod
    def validate(cls, instance):
        validate(instance=instance, schema=cls.schema)

    @classmethod
    def from_file(cls, filename):
        with open(os.path.expanduser(filename), "r") as f:
            res = json.load(f)
        cls.validate(res)
        return cls(**res)
