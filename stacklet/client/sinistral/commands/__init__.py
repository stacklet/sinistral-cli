from click.core import Group, Command, Option

from .run import run

import stacklet.client.sinistral.commands.policy  # noqa
import stacklet.client.sinistral.commands.policy_sources  # noqa
import stacklet.client.sinistral.commands.policy_collections  # noqa
import stacklet.client.sinistral.commands.projects  # noqa
import stacklet.client.sinistral.commands.scans  # noqa
import stacklet.client.sinistral.commands.group  # noqa

from stacklet.client.sinistral.client import client_registry
from stacklet.client.sinistral.utils import default_options


commands = [run]


for k, v in client_registry.items():
    group = default_options()(Group(name=k, short_help=f"{k} command"))
    for i, j in v.commands.items():
        options = []
        if j.params:
            for name, params in j.params.items():
                option = Option([name], **params)
                options.append(option)
        command = Command(name=i, help=j.__doc__, callback=j.cli_run, params=options)
        command = default_options()(command)
        group.add_command(command)
        commands.append(group)
