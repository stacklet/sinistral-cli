# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
import sys

from pathlib import Path

import click

from c7n_left.cli import dump as left_dump
from c7n_left.core import get_provider
from c7n_left.entry import initialize_iac


class LeftWrapper(click.core.Command):
    def make_parser(self, ctx):
        existing = {param.name for param in self.params}
        for param in left_dump.params:
            # make_parser runs on every invocation; the dump command is a
            # module-level singleton, so skip params already appended.
            if param.name not in existing:
                self.params.append(param)
        return super().make_parser(ctx)


@click.command(name="dump", cls=LeftWrapper)
@click.pass_context
def dump(ctx, *args, **kwargs):
    """Dump the IaC resource graph and input variables"""
    # c7n-left registers its IaC providers in its own cli group callback,
    # which is bypassed when invoking the dump subcommand directly.
    initialize_iac()
    if not ctx.params.get("directory"):
        ctx.params["directory"] = "."
    if get_provider(Path(ctx.params["directory"])) is None:
        raise click.UsageError(f"No supported IaC files found in {ctx.params['directory']}")
    sys.exit(left_dump.invoke(ctx))
