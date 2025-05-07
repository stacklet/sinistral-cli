import json
import re

from jsonref import replace_refs


with open("scripts/openapi.json", "r") as f:
    openapi = replace_refs(json.load(f))


def convert_to_snake(name):
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    _name = pattern.sub("_", name).lower()
    if _name == name:
        return name.lower()
    return _name


def parse_params(params, request_body):
    path_result = {}
    query_result = {}
    payload_result = {}

    if request_body:
        payload_result["schema"] = request_body["content"]["application/json"]["schema"]

    if not params:
        return path_result, query_result, payload_result

    for i in params:
        if i["in"] == "path":
            path_result.setdefault(f'--{i["name"]}', {"required": bool(i["required"])})
        if i["in"] == "query":
            query_result.setdefault(f'--{i["name"]}', {"required": bool(i["required"])})

    return path_result, query_result, payload_result


def format_command(
    name,
    command,
    class_name,
    method,
    path,
    path_params,
    query_params,
    payload_params,
    summary,
):
    command = convert_to_snake(command)
    cli_command = command.replace("_", "-")
    return '''
@{name}.commands.register("{cli_command}")
class {class_name}(ClientCommand):
    """
    {summary}
    """
    command = "{command}"
    method = "{method}"
    path = "{path}"
    params = {path_params}
    query_params = {query_params}
    payload_params = {payload_params}

    '''.format(
        name=name,
        cli_command=cli_command,
        command=command,
        class_name=class_name,
        path=path,
        method=method,
        path_params=path_params,
        query_params=query_params,
        payload_params=payload_params,
        summary=summary,
    )


def format_class(name):
    client_name = convert_to_snake(name).replace("_", "-")
    return '''
@client_registry.register('{client_name}')
class {name}(Client):
    """
    {name} Client
    """

    commands = PluginRegistry("commands")

'''.format(name=name, client_name=client_name)


def format_imports():
    return """# This is a generated file, created by scripts/parse.py
from stacklet.client.sinistral.client import client_registry, ClientCommand, Client
from stacklet.client.sinistral.registry import PluginRegistry

"""


if __name__ == "__main__":
    classes = {}

    for path, v in openapi["paths"].items():
        for method, j in v.items():
            summary = j.get("summary")
            tags = j.get("tags", [])
            operation_id = j.get("operationId")
            request_body = j.get("requestBody")
            response = j.get("responses")
            parameters = j.get("parameters")
            description = j.get("description")

            if tags:
                name = tags[0].replace(" ", "")
            else:
                # it's not an actual command
                continue

            command = summary.replace(" ", "")
            path_params, query_params, payload_params = parse_params(parameters, request_body)

            classes.setdefault(name, {})
            classes[name]["__class__"] = format_class(name)
            classes[name][command] = format_command(
                name=name,
                command=command,
                path=path,
                class_name=command,
                method=method,
                path_params=path_params,
                query_params=query_params,
                payload_params=payload_params,
                summary=description,
            )

    for k, v in classes.items():
        write_class = True
        with open(f"stacklet/client/sinistral/commands/{convert_to_snake(k)}.py", "w+") as f:
            f.writelines(
                [
                    "# Copyright Stacklet, Inc.\n",
                    "# SPDX-License-Identifier: Apache-2.0\n",
                ]
            )
            if "__class__" in v:
                if write_class:
                    f.writelines(format_imports())
                    write_class = False
                for i, j in v.items():
                    f.writelines(j)
        write_class = True
