# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
import logging

from stacklet.client.sinistral.config import StackletConfig
from stacklet.client.sinistral.formatter import Formatter


def populate_context(ctx, **kwargs):
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


def get_log_level(verbose):
    level = 50 - (verbose * 10)
    if level < 0:
        level = 0
    elif level > 50:
        level = 50
    return level
