import json
import logging
import sys

from tempfile import TemporaryDirectory

import click
import jmespath
import yaml

from c7n_left.cli import run as left_run
from c7n_left.output import Json, report_outputs, RichCli, JSONEncoder

from stacklet.client.sinistral.executor import make_request
from stacklet.client.sinistral.commands.projects import _get as get_project
from stacklet.client.sinistral.commands.policy_collection import _get_policies as get_policies


log = logging.getLogger('sinistral.run')

global project, dryrun, ctx


@report_outputs.register('sinistral')
class SinistralOutput(Json):
    """
    Outputs to sinistral/rich cli
    """

    def __init__(self, ctx, config):
        super().__init__(ctx, config)
        self.rich_cli = RichCli(ctx, config)

    def on_execution_started(self, policies, graph):
        super().on_execution_started(policies, graph)
        self.rich_cli.on_execution_started(policies, graph)

    def on_results(self, results):
        super().on_results(results)
        self.rich_cli.on_results(results)

    def on_execution_ended(self):
        global project, dryrun, ctx

        self.rich_cli.on_execution_ended()
        formatted_results = [self.format_result(r) for r in self.results]
        if self.config.output_query:
            formatted_results = jmespath.search(
                self.config.output_query, formatted_results
            )

        status = None

        results = json.loads(
            json.dumps({"results": formatted_results}, cls=JSONEncoder))

        if not results:
            status = 'PASSED'

        if results:
            status = 'FAILED'

        # sinistral expects a name for each resource, which we may not have for
        # data, provider terraform objects for example. hot fix here for now
        for r in results['results']:
            if (
                r['resource'].get('name') is None
                and r['resource']['__tfmeta']['type'] != 'resource'
            ):
                r['resource']['name'] = r['resource']['__tfmeta']['path']

        if not dryrun:
            payload = {
                'project_name': project,
                'results': results['results'],
                'status': status
            }
            res = make_request(ctx, 'post', '/scans', json=payload)
            click.echo(res)


class LeftWrapper(click.core.Command):
    """
    Wrapper for the c7n-left run command
    """
    def make_parser(self, ctx):
        for param in left_run.params:
            # skip policy dir as we pull policies from the collection
            # at runtime from sinistral
            if param == 'policy_dir':
                param.required = False
            self.params.append(param)
        return super().make_parser(ctx)


@click.command(name='run', cls=LeftWrapper)
@click.option('--project', required=True)
@click.option('--dryrun', is_flag=True)
@click.pass_context
def run(_ctx, *args, **kwargs):
    """
    Run a policy and report to sinistral
    """
    global project, dryrun, ctx
    _ctx.params['output'] = 'sinistral'
    ctx = _ctx

    project = ctx.params.pop('project')
    dryrun = ctx.params.pop('dryrun')

    results = []

    project_data = get_project(ctx, project)
    for c in project_data['collections']:
        policies = get_policies(ctx, c)
        raw_policies = [p['raw_policy'] for p in policies]
        with TemporaryDirectory() as tempdir:
            with open(f'{tempdir}/policy.yaml', 'w+') as f:
                yaml.dump({'policies': raw_policies}, f)
                ctx.params['policy_dir'] = tempdir
                results.append(int(left_run.invoke(ctx)))

    sys.exit(int(sorted(results)[-1]))
