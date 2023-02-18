from stacklet.client.sinistral.utils import default_options, click_group_entry
from stacklet.client.sinistral.executor import make_request

import click


@click.group(short_help="Projects command")
@default_options()
@click.pass_context
def projects(*args, **kwargs):
    click_group_entry(*args, **kwargs)


def _list(ctx, raw=True):
    result = make_request(ctx, "get", "/projects", raw=raw)
    return result


@projects.command()
@click.pass_context
def list(ctx, *args, **kwargs):
    click.echo(_list(ctx, raw=False))


def _get(ctx, name, raw=True):
    result = make_request(ctx, "get", f"/projects/{name}", raw=raw)
    return result


@projects.command()
@click.option("--name", required=True)
@click.pass_context
def get(ctx, *args, **kwargs):
    click.echo(_get(ctx, kwargs["name"], raw=False))
