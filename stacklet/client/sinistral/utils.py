# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
import logging

from functools import wraps

import click
from stacklet.client.sinistral.config import StackletConfig
from stacklet.client.sinistral.formatter import Formatter

_GLOBAL_OPTIONS = {
    # Config options
    "config": {
        "default": "~/.stacklet/sinistral",
        "help": "Directory containing the Sinistral config and token files",
        "envvar": ["STACKLET_CONFIG", "SINISTRAL_CONFIG"],
    },
    "auth_url": {
        "help": "Auth URL for most auth flows, except username & password",
    },
    "cognito_user_pool_id": {
        "help": "Cognito user pool ID for the username & password auth flow",
    },
    ("cognito_region", "region"): {
        "help": "Cognito region for the username & password auth flow",
    },
    "cognito_client_id": {
        "help": "Cognito client ID for the SSO, or username & password auth flows"
    },
    "project_client_id": {
        "help": "Project client ID for the Project Credentials auth flow",
    },
    "project_client_secret": {
        "help": "Project client secret for the Project Credentials auth flow",
    },
    "org_client_id": {
        "help": "Organization client ID for the Project Credentials auth flow",
    },
    "org_client_secret": {
        "help": "Organization client secret for the Project Credentials auth flow",
    },
    ("api_url", "api"): {"help": "URL for the Sinistral API endpoint"},
    # Output / format options
    "output": {
        "type": click.Choice(list(Formatter.registry.keys()), case_sensitive=False),
        "default": "yaml",
        "help": "Output format",
    },
    ("-v", "verbose"): {
        "count": True,
        "default": 0,
        "help": "Verbosity level, increase verbosity by appending v, e.g. -vvv",
    },
}

_PAGINATION_OPTIONS = {
    "first": {
        "help": "For use with pagination. Return the first n results.",
        "default": 20,
    },
    "last": {
        "help": "For use with pagination. Return the last n results. Overrides first.",
        "default": 0,
    },
    "before": {
        "help": "For use with pagination. Return the results before a given page cursor.",
        "default": "",
    },
    "after": {
        "help": "For use with pagination. Return the results after a given page curosr.",
        "default": "",
    },
}


def _normalize_opt_names(names):
    return [
        name if name.startswith("-") else f"--{name.replace('_', '-')}"
        for name in ([names] if isinstance(names, str) else names)
    ]


def wrap_command(func, options, required=False, prompt=False):
    for names, details in options.items():
        names = _normalize_opt_names(names)
        click.option(
            *names,
            required=required,
            prompt=prompt,
            **details,
        )(func)
    return func


def process_global_options(func):
    @wraps(func)
    def _process(*args, **kwargs):
        ctx = click.get_current_context()
        ctx.ensure_object(dict)

        logging.basicConfig()
        root_handler = logging.getLogger()
        v = ctx.params["verbose"]
        if v != 0:
            root_handler.setLevel(level=get_log_level(v))

        output = ctx.obj["output"] = ctx.params["output"]
        ctx.obj["formatter"] = Formatter.registry.get(output)()

        config_dir = ctx.params["config"]
        config = ctx.obj.get("config")
        if not config or config.config_dir != config_dir:
            config = ctx.obj["config"] = StackletConfig(config_dir)
        config.update(ctx.params)
        config.validate()

        for names in _GLOBAL_OPTIONS.keys():
            key = _normalize_opt_names(names)[-1]
            kwargs.pop(key.lstrip("-"), None)

        return func(*args, **kwargs)

    return _process


def global_options(process=True):
    def wrapper(cmd):
        if process:
            if hasattr(cmd, "callback"):
                # global_options decorated after click
                cmd.callback = process_global_options(cmd.callback)
            else:
                # global_options decorated before click (directly on func)
                cmd = process_global_options(cmd)
        wrap_command(cmd, _GLOBAL_OPTIONS)
        return cmd

    return wrapper


def get_log_level(verbose):
    level = 50 - (verbose * 10)
    if level < 0:
        level = 0
    elif level > 50:
        level = 50
    return level
