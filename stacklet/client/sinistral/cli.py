# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
import click
import jwt

from pathlib import Path

from stacklet.client.sinistral.cognito import CognitoClientAuth, CognitoUserManager
from stacklet.client.sinistral.commands import commands
from stacklet.client.sinistral.config import StackletConfig
from stacklet.client.sinistral.context import StackletContext
from stacklet.client.sinistral.utils import global_options

import stacklet.client.sinistral.output  # noqa
import stacklet.client.sinistral.client  # noqa


def main():
    cli(auto_envvar_prefix="SINISTRAL")


@click.group()
@global_options()
@click.pass_context
def cli(ctx, **params):
    """
    Sinistral CLI

    Configure your CLI

        $ sinistral configure

    Now login:

        $ sinistral login

    Your configuration file is saved to the directory: ~/.stacklet/sinistral/config.json
    and your credentials are stored at ~/.stacklet/sinistral/credentials.
    You may need to periodically login to refresh your authorization token.

    Run your first query:

        $ sinistral projects get-projects

    Specify different output types:

        $ sinistral projects get-projects --output json
    """
    pass  # defer to subcommands


@cli.command(short_help="Configure sinistral cli")
@click.option("--api", prompt="Sinistral API endpoint")
@click.option("--region", prompt="(user/pass auth) Cognito Region", default="")
@click.option(
    "--cognito-client-id",
    prompt="(SSO or user/pass auth) Cognito User Pool Client ID",
    default="",
)
@click.option(
    "--cognito-user-pool-id", prompt="(user/pass auth)Cognito User Pool ID", default=""
)
@click.option("--idp-id", prompt="(SSO) IDP ID", default="")
@click.option("--auth-url", prompt="(SSO, Project, or Org auth) Auth Url", default="")
@click.option(
    "--config-dir", prompt="Config directory", default="~/.stacklet/sinistral"
)
def configure(config_dir, **kwargs):
    """
    Interactively save a Stacklet Config file
    """
    config = StackletConfig(Path(config_dir))
    config.update(kwargs)
    config.write()

    click.echo(f"Saved config to {config.file_path}")


@cli.command()
@global_options()
@click.pass_context
def show(ctx, *args, **kwargs):
    """
    Show your config
    """
    with StackletContext(ctx) as context:
        id_token = context.get_id_token()
        if id_token:
            id_details = jwt.decode(id_token, options={"verify_signature": False})
            click.echo(context.fmt(id_details))
            click.echo()
        click.echo(context.fmt(context.config.to_dict()))


@cli.command(short_help="Login to Sinistral")
@click.option("--username", required=False)
@click.option("--password", hide_input=True, required=False)
@global_options()
@click.pass_context
def login(ctx, username, password, *args, **kwargs):
    """
    Login to Sinistral

        $ sinistral login

    Spawns a web browser to login via SSO or Cognito. To login with a Cognito user
    with username and password, simply pass those options into the CLI:

        $ sinistral login --username my-user

    If password is not passed in, your password will be prompted
    """
    with StackletContext(ctx) as context:
        if username and password:
            if not context.can_password_auth():
                ctx.fail("Cannot login with username & password with current config")

            if not username:
                username = click.prompt("Username")
            if not password:
                password = click.prompt("Password", hide_input=True)
            manager = CognitoUserManager.from_context(context)
            res = manager.login(
                user=username,
                password=password,
            )
            context.write_access_token(res)
            return

        if context.can_project_auth():
            client = CognitoClientAuth(ctx)
            token = client.get_access_token(
                context.config.auth_url,
                context.config.project_client_id,
                context.config.project_client_secret,
            )
            context.write_access_token(token)
            return

        if context.can_org_auth():
            client = CognitoClientAuth(ctx)
            token = client.get_access_token(
                context.config.auth_url,
                context.config.org_client_id,
                context.config.org_client_secret,
            )
            context.write_access_token(token)
            return

        if context.can_sso_auth():
            from stacklet.client.sinistral.vendored.auth import BrowserAuthenticator

            BrowserAuthenticator(
                authority_url=context.config.auth_url,
                client_id=context.config.cognito_client_id,
                idp_id=context.config.idp_id,
            )()
            return


for c in commands:
    cli.add_command(c)


if __name__ == "__main__":
    main()
