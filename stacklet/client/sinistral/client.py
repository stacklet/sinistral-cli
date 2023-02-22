import json
import sys

from jsonschema import validate
from functools import partial

import click

from stacklet.client.sinistral.context import StackletContext
from stacklet.client.sinistral.executor import RestExecutor
from stacklet.client.sinistral.formatter import Formatter
from stacklet.client.sinistral.utils import get_token

from stacklet.client.sinistral.registry import PluginRegistry


client_registry = PluginRegistry("clients")

type_maps = {"string": str, "float": float, "int": int, "number": int, "object": dict}


def validate_list(ctx, param, value):
    try:
        # when using the multiple argument on a click option, it returns the
        # kwargs as a tuple of list of characters so we reconstruct here
        return ["".join(v) for v in value]
    except Exception:
        raise click.BadParameter(f"{value} should be list")


def validate_types(types, schema, ctx, param, value):
    if len(types) == 1:
        if types[0] == "object":
            return validate_json(schema, ctx, param, value)

    for t in types:
        if t == "object":
            try:
                return validate_json(schema, ctx, param, value)
            except Exception:
                continue
        if isinstance(value, type_maps[t]):
            return value

    raise click.BadParameter(f"{value} should be one of {types}")


def validate_json(schema, ctx, param, value):
    try:
        value = json.loads(value)
        validate(value, schema)
        return value
    except Exception:
        raise click.BadParameter(
            f"{value} should be json encoded string and compatible with schema:\n{json.dumps(schema, indent=2)}"
        )


def parse_jsonschema(schema):
    """
    Parse the top level keys for a jsonschema
    """
    result = {}
    if not schema:
        return result
    for name, info in schema["properties"].items():
        result[name] = {}
        result[name]["help"] = info.get("title")
        if info.get("default"):
            result[name]["default"] = info["default"]
            result[name]["show_default"] = True
        if info.get("type") == "array":
            result[name]["type"] = list
            if info["items"]["type"] != "string":
                result[name]["type"] = str
                result[name]["callback"] = partial(validate_json, info)
            else:
                result[name]["multiple"] = True
                result[name]["callback"] = validate_list
        if info.get("type") == "object":
            result[name]["type"] = str
            result[name]["callback"] = partial(validate_json, info)

        if info.get("anyOf"):
            types = []
            for i in info["anyOf"]:
                types.append(i["type"])
            types = list(set(types))
            result[name]["callback"] = partial(validate_types, types, info)

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
        try:
            res = cls.run(**kwargs)
        except Exception as e:
            click.echo(e)
            sys.exit(1)
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

    def make_request(
        self, method, path, _json={}, output="raw", schema=None, q_params={}
    ):
        with self.ctx as context:
            token = get_token()
            executor = RestExecutor(context, token)
            func = getattr(executor, method)
            if isinstance(_json, str):
                _json = json.loads(_json)
            if schema:
                validate(_json, schema)
            res = func(path, q_params, _json).json()
            if isinstance(res, dict):
                if res.get("message") == "Unauthorized":
                    raise Exception("Unauthorized, check credentials")
                if res.get("detail"):
                    raise Exception(f"An error occured: {res['detail']}")
            fmt = Formatter.registry.get(output, "yaml")()
        return fmt(res)


def sinistral_client():
    import stacklet.client.sinistral.commands  # noqa

    ctx = StackletContext(raw_config={})
    return SinistralClient(ctx)
