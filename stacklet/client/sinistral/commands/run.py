# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
import logging
import sys

from tempfile import TemporaryDirectory

import click
import yaml

from c7n.config import Config
from c7n_left.cli import get_config
from c7n_left.cli import run as left_run
from c7n_left.output import MultiOutput, get_reporter

from stacklet.client.sinistral.client import sinistral_client
from stacklet.client.sinistral.output import SinistralFormat


log = logging.getLogger("sinistral.run")


class LeftWrapper(click.core.Command):
    """
    Wrapper for the c7n-left run command
    """

    def make_parser(self, ctx):
        for param in left_run.params:
            if param.name == "policy_dir":
                # skip policy dir as we pull policies from the collection
                # at runtime from sinistral
                param.required = False
            if param.name == "directory":
                # directory to scan is required, though, or it blows up
                # during arg parsing
                param.required = True
            self.params.append(param)
        return super().make_parser(ctx)


@click.command(name="run", cls=LeftWrapper)
@click.option("--project", required=False, help="Either project or policy dir must be set.")
@click.option("--dryrun", is_flag=True)
@click.pass_context
def run(ctx, project, dryrun, *args, **kwargs):
    """
    Run a policy and report to sinistral
    """

    if project and ctx.params.get("policy_dir"):
        raise click.UsageError("Either project or policy directory must be specified")

    if project is None:
        if ctx.params.get("policy_dir"):
            ctx.params.pop("project")
            ctx.params.pop("dryrun")
            sys.exit(int(left_run.invoke(ctx)))
        raise click.UsageError("Either project or policy directory must be specified")

    ctx.obj["output"] = "raw"  # formatter (used in SinistralClient.make_request)

    # Setup sinistral output format

    # pop parameters specific to sinistral format
    project = ctx.params.pop("project")
    dryrun = ctx.params.pop("dryrun")
    config = get_config(**ctx.params)
    s_config = Config.empty(**config)
    s_config.update({"project": project, "dryrun": dryrun})

    formatter = SinistralFormat(None, s_config)
    ctx.params["reporter"] = MultiOutput([get_reporter(config), formatter])

    sinistral = sinistral_client()

    projects_client = sinistral.client("projects")
    try:
        policies = projects_client.get_policies(name=project, include_defaults=True)
    except Exception as e:
        click.echo(f"Unable to get project: {e}", err=True)
        sys.exit(1)

    if not policies:
        click.echo("Project has no policy collections", err=True)
        sys.exit(1)

    raw_policies = [p["raw_policy"] for p in policies]
    results = []
    with TemporaryDirectory() as tempdir:
        with open(f"{tempdir}/policy.yaml", "w+") as f:
            yaml.dump({"policies": raw_policies}, f)
            ctx.params["policy_dir"] = tempdir
            results.append(int(left_run.invoke(ctx)))
    sys.exit(int(sorted(results)[-1]))
