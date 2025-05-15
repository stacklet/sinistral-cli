# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
from click.core import Command, Group, Option

import stacklet.client.sinistral.commands.group  # noqa
import stacklet.client.sinistral.commands.org  # noqa
import stacklet.client.sinistral.commands.policy  # noqa
import stacklet.client.sinistral.commands.policy_collections  # noqa
import stacklet.client.sinistral.commands.policy_sources  # noqa
import stacklet.client.sinistral.commands.projects  # noqa
import stacklet.client.sinistral.commands.scans  # noqa

from stacklet.client.sinistral.client import client_registry, parse_jsonschema

from .dump import dump
from .run import run


commands = [run, dump]


# Instantiate commands out of clients
for k, v in client_registry.items():
    group = Group(name=k, short_help=f"{k} command")
    for i, j in v.commands.items():
        options = []
        if j.params:
            for name, params in j.params.items():
                option = Option([name.replace("_", "-")], **params)
                options.append(option)
        if j.query_params:
            for name, params in j.query_params.items():
                option = Option([name.replace("_", "-")], **params)
                options.append(option)
        if "schema" in j.payload_params:
            for name, _params in parse_jsonschema(j.payload_params["schema"]).items():
                option = Option([f"--{name.replace('_', '-')}"], **_params)
                options.append(option)
        command = Command(name=i, help=j.__doc__, callback=j.cli_run, params=options)
        group.add_command(command)
        commands.append(group)
