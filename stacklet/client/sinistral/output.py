# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
import json

from urllib.parse import urlparse

import click
import jmespath

from c7n_left.output import Json, JSONEncoder, MultiOutput, RichCli, report_outputs
from codecov_cli.helpers.ci_adapters import get_ci_adapter

from stacklet.client.sinistral.client import sinistral_client


class SinistralFormat(Json):
    project = None
    dryrun = None

    def __init__(self, ctx, config):
        super().__init__(ctx, config)
        if self.config.project and self.project is None:
            self.project = self.config.project
        if self.config.dryrun and self.dryrun is None:
            self.dryrun = self.config.dryrun

    def get_ci_info(self):
        properties_to_access = [
            "service",
            "build_url",
            "build_code",
            "job_code",
            "pull_request_number",
            "branch",
            "commit_sha",
            "slug",
        ]

        key_map = {"slug": "repo"}

        adapter = get_ci_adapter()
        data = {}
        for prop in properties_to_access:
            result = getattr(adapter, f"_get_{prop}")()

            if result is None:
                result = ""

            key = key_map.get(prop, prop)
            data[key] = result

        # code-cov currently doesn't have a generic way to get the service
        # url, so for now I'm going to parse out build_url but I plan on
        # contributing the service URL code to them because they already
        # know how to do it.  They use it to generate `build_url`.
        if data["build_url"] is not None:
            build_url = data["build_url"]
            parsed_url = urlparse(build_url)
            data["repo_url"] = f"{parsed_url.scheme}://{parsed_url.netloc}/{data['repo']}"
        else:
            data["repo_url"] = ""

        return data

    def on_execution_ended(self):
        formatted_results = [self.format_result(r) for r in self.results]
        if self.config.output_query:
            formatted_results = jmespath.search(self.config.output_query, formatted_results)

        status = None

        results = json.loads(json.dumps({"results": formatted_results}, cls=JSONEncoder))["results"]

        status = "PASSED" if not results else "FAILED"

        # sinistral expects a name for each resource, which we may not have for
        # data, provider terraform objects for example. hot fix here for now
        for r in results:
            r["resource"].setdefault("c7n:MatchedFilters", [])
            if not r["resource"].get("name"):
                r["resource"]["name"] = r["resource"]["__tfmeta"]["path"]

            metadata = r["policy"].get("metadata", {})
            severity = metadata.get("severity", "").lower()

            if severity not in (
                "critical",
                "high",
                "medium",
                "low",
                "unknown",
            ):
                metadata.update({"severity": "unknown"})
                r["policy"]["metadata"] = metadata

        if self.dryrun:
            return

        sinistral = sinistral_client()
        scans_client = sinistral.client("scans")
        ci_info = self.get_ci_info()

        # We don't need to record CI info for local runs.
        if ci_info["service"] == "local":
            ci_info = None

        res = scans_client.create(
            project_name=self.project,
            results=results,
            status=status,
            ci_info=ci_info,
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
