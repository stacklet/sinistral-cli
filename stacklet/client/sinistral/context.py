# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
from pathlib import Path

import click

from stacklet.client.sinistral.cognito import CognitoClientAuth


class StackletContext:
    """
    CLI Execution Context
    """

    CREDENTIALS_FILE = "credentials"
    ID_FILE = "id"

    # cache access token
    _ACCESS_TOKEN = None

    def __init__(self, click_context):
        self._click_context = click_context
        self.config = click_context.obj["config"]
        self.output = click_context.obj["output"]
        self.fmt = click_context.obj["formatter"]

        base_path = Path(self.config.config_dir).expanduser()
        self.access_token_path = base_path / self.CREDENTIALS_FILE
        self.id_token_path = base_path / self.ID_FILE

    def get_access_token(self):
        if StackletContext._ACCESS_TOKEN:
            return StackletContext._ACCESS_TOKEN
        access_token = None
        if self.access_token_path.exists():
            access_token = self.access_token_path.read_text()
        elif self.can_project_auth():
            access_token = self.do_project_auth()
        elif self.can_org_auth():
            access_token = self.do_org_auth()
        StackletContext._ACCESS_TOKEN = access_token
        return access_token

    def _write_token(self, token_path, token):
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(token)

    def write_access_token(self, token):
        StackletContext._ACCESS_TOKEN = token
        self._write_token(self.access_token_path, token)

    def get_id_token(self):
        if self.id_token_path.exists():
            return self.id_token_path.read_text()
        else:
            return None

    def write_id_token(self, token):
        self._write_token(self.id_token_path, token)

    def __enter__(self):
        # validate the config only when the context is entered, to allow click
        # to fully process command line options
        self.config.validate()
        return self

    def __exit__(self, type, value, traceback):
        return

    def can_password_auth(self):
        return all(
            [
                self.config.cognito_client_id,
                self.config.cognito_user_pool_id,
                self.config.cognito_region,
            ]
        )

    def can_sso_auth(self):
        return all(
            [
                self.config.auth_url,
                self.config.cognito_client_id,
            ]
        )

    def can_project_auth(self):
        return all(
            [
                self.config.project_client_id,
                self.config.project_client_secret,
            ]
        )

    def do_project_auth(self) -> str:
        client = CognitoClientAuth(self._click_context)
        token = client.get_access_token(
            self.config.auth_url,
            self.config.project_client_id,
            self.config.project_client_secret,
        )
        return token

    def can_org_auth(self):
        return all(
            [
                self.config.org_client_id,
                self.config.org_client_secret,
            ]
        )

    def do_org_auth(self) -> str:
        client = CognitoClientAuth(self._click_context)
        token = client.get_access_token(
            self.config.auth_url,
            self.config.org_client_id,
            self.config.org_client_secret,
        )
        return token


class StackletCredentialWriter:
    def write_id_token(self, token):
        context = StackletContext(click.get_current_context())
        context.write_id_token(token)

    def write_access_token(self, token):
        context = StackletContext(click.get_current_context())
        context.write_access_token(token)
