# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
import sys

import click

from c7n_left.cli import dump as left_dump


class LeftWrapper(click.core.Command):
    def make_parser(self, ctx):
        for param in left_dump.params:
            self.params.append(param)
        return super().make_parser(ctx)


@click.command(name="dump", cls=LeftWrapper)
@click.pass_context
def dump(ctx, *args, **kwargs):
    """Dump the IaC resource graph and input variables"""
    sys.exit(left_dump.invoke(ctx))
