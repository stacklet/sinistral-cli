import click
import json

import jmespath

from c7n_left.output import Json, report_outputs, RichCli, JSONEncoder, MultiOutput

from stacklet.client.sinistral.executor import make_request


class SinistralFormat(Json):
    project = None
    dryrun = None
    cli_ctx = None

    def __init__(self, ctx, config):
        super().__init__(ctx, config)

    def on_execution_ended(self):
        formatted_results = [self.format_result(r) for r in self.results]
        if self.config.output_query:
            formatted_results = jmespath.search(
                self.config.output_query, formatted_results
            )

        status = None

        results = json.loads(
            json.dumps({"results": formatted_results}, cls=JSONEncoder)
        )["results"]

        if not results:
            status = "PASSED"

        if results:
            status = "FAILED"

        # sinistral expects a name for each resource, which we may not have for
        # data, provider terraform objects for example. hot fix here for now
        for r in results:
            if (
                r["resource"].get("name") is None
                and r["resource"]["__tfmeta"]["type"] != "resource"
            ):
                r["resource"]["name"] = r["resource"]["__tfmeta"]["path"]

        if not self.dryrun:
            payload = {
                "project_name": self.project,
                "results": results,
                "status": status,
            }
            res = make_request(self.cli_ctx, "post", "/scans", json=payload)
            click.echo(res)


@report_outputs.register("sinistral")
class SinistralOutput(MultiOutput):
    """
    Outputs to sinistral/rich cli
    """

    def __init__(self, ctx, config):
        super().__init__([SinistralFormat(ctx, config), RichCli(ctx, config)])
