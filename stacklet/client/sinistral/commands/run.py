import logging
import sys

from tempfile import TemporaryDirectory

import click
import yaml

from c7n_left.cli import run as left_run

# from stacklet.client.sinistral.commands.projects import _get as get_project
# from stacklet.client.sinistral.commands.policy_collection import (
#     _get_policies as get_policies,
# )
from stacklet.client.sinistral.output import SinistralFormat
from stacklet.client.sinistral.client import sinistral_client


log = logging.getLogger("sinistral.run")


class LeftWrapper(click.core.Command):
    """
    Wrapper for the c7n-left run command
    """

    def make_parser(self, ctx):
        for param in left_run.params:
            # skip policy dir as we pull policies from the collection
            # at runtime from sinistral
            if param == "policy_dir":
                param.required = False
            self.params.append(param)
        return super().make_parser(ctx)


@click.command(name="run", cls=LeftWrapper)
@click.option("--project", required=True)
@click.option("--dryrun", is_flag=True)
@click.pass_context
def run(ctx, *args, **kwargs):
    """
    Run a policy and report to sinistral
    """
    ctx.params["output"] = "sinistral"

    # afaics there's no way for us to pass this info into the output
    # string like we do for other c7n outputs, e.g. s3://foo, if
    # we did url lookup like sinistral://$project we could drop this
    SinistralFormat.project = ctx.params.pop("project")
    SinistralFormat.dryrun = ctx.params.pop("dryrun")
    SinistralFormat.cli_ctx = ctx

    sinistral = sinistral_client()

    projects_client = sinistral.client("projects")
    policy_collections_client = sinistral.client("policy-collections")

    results = []
    project_data = projects_client.get(name=SinistralFormat.project)
    for c in project_data["collections"]:
        policies = policy_collections_client.get_policies(name=c)
        raw_policies = [p["raw_policy"] for p in policies]
        with TemporaryDirectory() as tempdir:
            with open(f"{tempdir}/policy.yaml", "w+") as f:
                yaml.dump({"policies": raw_policies}, f)
                ctx.params["policy_dir"] = tempdir
                results.append(int(left_run.invoke(ctx)))

    sys.exit(int(sorted(results)[-1]))
