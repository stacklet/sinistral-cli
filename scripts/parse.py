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
    result = {}

    if request_body:
        result["--json"] = {}

    if not params:
        return result

    for i in params:
        result.setdefault(f'--{i["name"]}', {})

    return result


def format_command(name, command, class_name, method, path, params):
    command = convert_to_snake(command)
    cli_command = command.replace('_', '-')
    return '''
@{name}.commands.register("{cli_command}")
class {class_name}(ClientCommand):
    """
    {command}
    """
    command = "{command}"
    method = "{method}"
    path = "{path}"
    params = {params}

    '''.format(
        name=name,
        cli_command=cli_command,
        command=command,
        class_name=class_name,
        path=path,
        method=method,
        params=json.dumps(params),
    )


def format_class(name):
    return '''
@client_registry.register('{name}')
class {name}(Client):
    """
    {name} Client
    """

    commands = PluginRegistry("commands")

'''.format(
        name=name
    )


def format_imports():
    return """from stacklet.client.sinistral.client import client_registry, ClientCommand, Client
from stacklet.client.sinistral.registry import PluginRegistry

"""


classes = {}


for path, v in openapi["paths"].items():
    for method, j in v.items():
        summary = j.get("summary")
        tags = j.get("tags", [])
        operation_id = j.get("operationId")
        request_body = j.get("requestBody")
        response = j.get("responses")
        parameters = j.get("parameters")

        if tags:
            name = tags[0].replace(" ", "")
        else:
            # it's not an actual command
            continue

        command = summary.replace(" ", "")
        params = parse_params(parameters, request_body)

        classes.setdefault(name, {})
        classes[name]["__class__"] = format_class(name)
        classes[name][command] = format_command(
            name=name,
            command=command,
            path=path,
            class_name=command,
            method=method,
            params=params,
        )


for k, v in classes.items():
    write_class = True
    with open(
        f"stacklet/client/sinistral/commands/{convert_to_snake(k)}.py", "w+"
    ) as f:
        if "__class__" in v:
            if write_class:
                f.writelines(format_imports())
                write_class = False
            for i, j in v.items():
                f.writelines(j)
    write_class = True
