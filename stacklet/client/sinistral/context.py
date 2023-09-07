# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
from pathlib import Path

import click


class StackletContext:
    """
    CLI Execution Context
    """

    CREDENTIALS_FILE = "credentials"
    ID_FILE = "id"

    def __init__(self, click_context):
        self._click_context = click_context
        self.config = click_context.obj["config"]
        self.output = click_context.obj["output"]
        self.fmt = click_context.obj["formatter"]

        base_path = Path(self.config.config_dir).expanduser()
        self.access_token_path = base_path / self.CREDENTIALS_FILE
        self.id_token_path = base_path / self.ID_FILE

    def get_access_token(self):
        if self.access_token_path.exists():
            return self.access_token_path.read_text()
        else:
            return None

    def write_access_token(self, token):
        self.access_token_path.parent.mkdir(parents=True, exist_ok=True)
        self.access_token_path.write_text(token)

    def get_id_token(self):
        if self.id_token_path.exists():
            return self.id_token_path.read_text()
        else:
            return None

    def write_id_token(self, token):
        self.id_token_path.parent.mkdir(parents=True, exist_ok=True)
        self.id_token_path.write_text(token)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return

    def can_sso_login(self):
        return all(
            [
                self.config.auth_url,
                self.config.cognito_client_id,
            ]
        )


class StackletCredentialWriter:
    def write_id_token(self, token):
        context = StackletContext(click.get_current_context())
        context.write_id_token(token)

    def write_access_token(self, token):
        context = StackletContext(click.get_current_context())
        context.write_access_token(token)
