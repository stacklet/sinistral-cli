import click
import json
import jwt
import os

from stacklet.client.sinistral.cognito import CognitoUserManager
from stacklet.client.sinistral.commands import commands
from stacklet.client.sinistral.config import StackletConfig, DEFAULT_PATH
from stacklet.client.sinistral.context import StackletContext
from stacklet.client.sinistral.formatter import Formatter
from stacklet.client.sinistral.utils import click_group_entry, default_options

import stacklet.client.sinistral.output  # noqa
import stacklet.client.sinistral.client  # noqa


@click.group()
@default_options()
@click.pass_context
def cli(*args, **kwargs):
    """
    Sinistral CLI

    Configure your CLI

        $ sinistral configure

    Now login:

        $ sinistral login

    Your configuration file is saved to the directory: ~/.stacklet/sinistral/config.json and your credentials
    are stored at ~/.stacklet/sinistral/credentials. You may need to periodically login to refresh your
    authorization token.

    Run your first query:

        $ sinistral projects get-projects

    Specify different output types:

        $ sinistral projects get-projects --output json
    """
    click_group_entry(*args, **kwargs)


@cli.command(short_help="Configure sinistral cli")
@click.option("--api", prompt="Sinistral API endpoint")
@click.option("--region", prompt="Cognito Region")
@click.option("--cognito-client-id", prompt="Cognito User Pool Client ID")
@click.option("--cognito-user-pool-id", prompt="Cognito User Pool ID")
@click.option("--idp-id", prompt="(SSO) IDP ID", default="")
@click.option("--auth-url", prompt="(SSO) Auth Url", default="")
@click.option("--location", prompt="Config File Location", default=DEFAULT_PATH)  # noqa
@click.pass_context
def configure(
    ctx,
    api,
    region,
    cognito_client_id,
    cognito_user_pool_id,
    idp_id,
    auth_url,
    location,
):
    """
    Interactively save a Stacklet Config file
    """
    config = {
        "api": api,
        "region": region,
        "cognito_client_id": cognito_client_id,
        "cognito_user_pool_id": cognito_user_pool_id,
        "idp_id": idp_id,
        "auth_url": auth_url,
    }

    StackletConfig.validate(config)

    if not os.path.exists(location):
        dirs = location.rsplit("/", 1)[0]
        os.makedirs(os.path.expanduser(dirs), exist_ok=True)

    with open(os.path.expanduser(location), "w+") as f:
        f.write(json.dumps(config))
    click.echo(f"Saved config to {location}")


@cli.command()
@click.pass_context
def show(ctx):
    """
    Show your config
    """
    with StackletContext(ctx.obj["config"], ctx.obj["raw_config"]) as context:
        fmt = Formatter.registry.get(ctx.obj["output"])()
        if os.path.exists(os.path.expanduser(StackletContext.DEFAULT_ID)):
            with open(os.path.expanduser(StackletContext.DEFAULT_ID), "r") as f:
                id_details = jwt.decode(f.read(), options={"verify_signature": False})
            click.echo(fmt(id_details))
            click.echo()
        click.echo(fmt(context.config.to_json()))


@cli.command(short_help="Login to Sinistral")
@click.option("--username", required=False)
@click.option("--password", hide_input=True, required=False)
@click.pass_context
def login(ctx, username, password):
    """
    Login to Sinistral

        $ sinistral login

    Spawns a web browser to login via SSO or Cognito. To login with a Cognito user
    with username and password, simply pass those options into the CLI:

        $ sinistral login --username my-user

    If password is not passed in, your password will be prompted
    """
    with StackletContext(ctx.obj["config"], ctx.obj["raw_config"]) as context:
        # sso login
        if context.can_sso_login() and not any([username, password]):
            from stacklet.client.sinistral.vendored.auth import BrowserAuthenticator

            BrowserAuthenticator(
                authority_url=context.config.auth_url,
                client_id=context.config.cognito_client_id,
                idp_id=context.config.idp_id,
            )()
            return
        elif not context.can_sso_login() and not any([username, password]):
            click.echo(
                "To login with SSO ensure that your configuration includes "
                + "auth_url, and cognito_client_id values."
            )
            raise Exception()

        # handle login with username/password
        if not username:
            username = click.prompt("Username")
        if not password:
            password = click.prompt("Password", hide_input=True)
        manager = CognitoUserManager.from_context(context)
        res = manager.login(
            user=username,
            password=password,
        )
        if not os.path.exists(
            os.path.dirname(os.path.expanduser(StackletContext.DEFAULT_CREDENTIALS))
        ):
            os.makedirs(
                os.path.dirname(os.path.expanduser(StackletContext.DEFAULT_CREDENTIALS))
            )
        with open(
            os.path.expanduser(StackletContext.DEFAULT_CREDENTIALS), "w+"
        ) as f:  # noqa
            f.write(res)


for c in commands:
    cli.add_command(c)


if __name__ == "__main__":
    cli()
