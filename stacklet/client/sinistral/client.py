import json

import click

from stacklet.client.sinistral.context import StackletContext
from stacklet.client.sinistral.executor import RestExecutor
from stacklet.client.sinistral.formatter import Formatter
from stacklet.client.sinistral.utils import get_token

from stacklet.client.sinistral.registry import PluginRegistry


client_registry = PluginRegistry("clients")


def parse_jsonschema(schema):
    """
    Parse the top level keys for a jsonschema
    """
    result = {}
    if not schema:
        return result
    for name, info in schema["properties"].items():
        result[name] = {}

    for req in schema.get("required", []):
        result[req]["required"] = True

    return result


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
    def handle_query_params(cls, kwargs):
        lower_map = {}
        q_params = {}
        # click passes the kwargs as lowercased version, without the '--'
        for k in cls.query_params.keys():
            lower_map = {k[2:].lower(): k[2:]}
        for k, v in kwargs.items():
            if k in lower_map:
                q_params[lower_map[k]] = v
        return q_params

    @classmethod
    def handle_json_payload(cls, kwargs):
        payload = {}
        if cls.payload_params:
            json_keys = parse_jsonschema(cls.payload_params["schema"])
            for k, v in kwargs.items():
                if k in json_keys:
                    payload[k] = v
        return payload

    @classmethod
    def run(cls, **kwargs):
        ctx = StackletContext(raw_config={})
        client = SinistralClient(ctx)

        payload = cls.handle_json_payload(kwargs)
        q_params = cls.handle_query_params(kwargs)

        res = client.make_request(
            method=cls.method,
            path=cls.path.format(**kwargs),
            _json=payload,
            schema=cls.payload_params.get("schema", {}),
            output=kwargs.get("output", "raw"),
            q_params=q_params,
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

    def make_request(self, method, path, _json={}, output="raw", schema=None, q_params={}):
        with StackletContext(self.ctx.config, self.ctx.config.to_json()) as context:
            token = get_token()
            executor = RestExecutor(context, token)
            func = getattr(executor, method)
            if isinstance(_json, str):
                _json = json.loads(_json)
            if schema:
                from jsonschema import validate

                validate(_json, schema)
            res = func(path, q_params, _json).json()
            if isinstance(res, dict) and res.get("message") == "Unauthorized":
                raise Exception("Unauthorized, check credentials")
            fmt = Formatter.registry.get(output, "yaml")()
        return fmt(res)


def sinistral_client():
    import stacklet.client.sinistral.commands  # noqa

    ctx = StackletContext(raw_config={})
    return SinistralClient(ctx)
