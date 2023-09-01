# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
import click
import json

import jmespath

from c7n_left.output import Json, report_outputs, RichCli, JSONEncoder, MultiOutput

from stacklet.client.sinistral.client import sinistral_client


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

        status = "PASSED" if not results else "FAILED"

        # sinistral expects a name for each resource, which we may not have for
        # data, provider terraform objects for example. hot fix here for now
        for r in results:
            r["resource"].setdefault("c7n:MatchedFilters", [])
            if not r["resource"].get("name"):
                r["resource"]["name"] = r["resource"]["__tfmeta"]["path"]
            if not r["policy"].get("metadata", {}).get("severity").lower() in (
                "high",
                "medium",
                "low",
                "unknown",
            ):
                r["policy"]["metadata"]["severity"] = "unknown"
        if self.dryrun:
            return

        sinistral = sinistral_client()
        scans_client = sinistral.client("scans")
        res = scans_client.create(
            project_name=self.project, results=results, status=status
        )
        if res.get("id"):
            click.echo(f'Results submitted: id:{res["id"]}')
            pass


@report_outputs.register("sinistral")
class SinistralOutput(MultiOutput):
    """
    Outputs to sinistral/rich cli
    """

    def __init__(self, ctx, config):
        super().__init__([SinistralFormat(ctx, config), RichCli(ctx, config)])
