import click

from stacklet.client.sinistral.context import StackletContext
from stacklet.client.sinistral.executor import RestExecutor
from stacklet.client.sinistral.formatter import Formatter
from stacklet.client.sinistral.utils import get_token

from stacklet.client.sinistral.registry import PluginRegistry


client_registry = PluginRegistry("clients")


class Client(object):
    def __getattr__(self, attr):
        replaced = attr.replace("_", "-")
        if replaced in self.commands.keys():
            return self.commands.get(replaced).run
        raise AttributeError(replaced)


class ClientCommand:
    help = "A Sinistral Command"
    command = None
    method = None
    path = None
    params = {}

    @classmethod
    def cli_run(cls, **kwargs):
        res = cls.run(**kwargs)
        click.echo(res)

    @classmethod
    def run(cls, **kwargs):
        ctx = StackletContext(raw_config={})
        client = SinistralClient(ctx)
        res = client.make_request(
            cls.method,
            cls.path.format(**kwargs),
            json=kwargs.get('json', {}),
            output=kwargs.get("output", "raw"),
        )
        return res


class SinistralClient:
    def __init__(self, ctx):
        self.ctx = ctx

    def client(self, name):
        client = client_registry.get(name)
        if name:
            return client()
        raise Exception(f"{name} client not found")

    def make_request(self, method, path, json={}, output="raw"):
        with StackletContext(self.ctx.config, self.ctx.config.to_json()) as context:
            token = get_token()
            executor = RestExecutor(context, token)
            func = getattr(executor, method)
            res = func(path, json).json()
            if isinstance(res, dict) and res.get("message") == "Unauthorized":
                raise Exception("Unauthorized, check credentials")
            fmt = Formatter.registry.get(output, "yaml")()
        return fmt(res)


def sinistral_client():
    import stacklet.client.sinistral.commands  # noqa

    ctx = StackletContext(raw_config={})
    return SinistralClient(ctx)
