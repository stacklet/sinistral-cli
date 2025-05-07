# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
"""
Handle configuration for the CLI
"""

import json

from pathlib import Path

import jsonschema

from stacklet.client.sinistral.exceptions import ConfigValidationException


class StackletConfig:
    CONFIG_FILE = "config.json"

    schema = {
        "type": "object",
        "properties": {
            "api_url": {"type": "string"},
            "cognito_user_pool_id": {"type": "string"},
            "cognito_client_id": {"type": "string"},
            "cognito_region": {"type": "string"},
            "idp_id": {"type": "string"},
            "auth_url": {"type": "string"},
            "project_client_id": {"type": "string"},
            "project_client_secret": {"type": "string"},
            "org_client_id": {"type": "string"},
            "org_client_secret": {"type": "string"},
        },
        "required": [
            "api_url",
        ],
        "anyOf": [
            # SSO auth flow
            {
                "required": [
                    "auth_url",
                    "cognito_client_id",
                ],
            },
            # Username + password auth flow
            {
                "required": [
                    "cognito_client_id",
                    "cognito_user_pool_id",
                    "cognito_region",
                ],
            },
            # Project Credentials auth flow
            {
                "required": [
                    "auth_url",
                    "project_client_id",
                    "project_client_secret",
                ],
            },
            # Org Credentials auth flow
            {
                "required": [
                    "auth_url",
                    "org_client_id",
                    "org_client_secret",
                ],
            },
        ],
    }

    def __init__(self, config_dir):
        self.config_dir = config_dir
        self.file_path = Path(config_dir).expanduser() / self.CONFIG_FILE
        for key in self.schema["properties"].keys():
            setattr(self, key, None)
        if self.file_path.exists():
            self.read()

    def update(self, data):
        for key in self.schema["properties"].keys():
            value = data.get(key)
            if not value and key == "cognito_region":
                # There was some inconsistency on region vs cognito_region
                # and we're now using cognito_region consistently. But also
                # support the older form for compatibility.
                value = data.get("region")
            if not value and key == "api_url":
                # Backward compatibility support for api vs api_url
                value = data.get("api")
            if value:
                setattr(self, key, value)

    def validate(self):
        try:
            jsonschema.validate(instance=self.to_dict(), schema=self.schema)
        except jsonschema.ValidationError as exc:
            # TODO: Clean up error reporting to be a bit more friendly,
            # especially around the different auth forms.
            raise ConfigValidationException.from_exc(exc)

    def read(self):
        self.update(json.loads(self.file_path.read_text()))

    def write(self):
        self.file_path.write_text(self.to_json())

    def to_dict(self):
        return {
            key: getattr(self, key)
            for key in self.schema["properties"].keys()
            if getattr(self, key)
        }

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True, indent=2)
