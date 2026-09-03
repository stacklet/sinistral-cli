# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
import pathlib

from unittest.mock import Mock, patch

from click.testing import CliRunner

from stacklet.client.sinistral.cli import cli
from stacklet.client.sinistral.context import StackletContext
from stacklet.client.sinistral.executor import RestExecutor

from .utils import (
    create_scan_response,
    get_mock_response,
    get_policies_for_project_response,
)


def test_run_command():
    runner = CliRunner()
    result = runner.invoke(cli, ["run", "--help"])
    assert "policy-dir" in result.output
    assert "project" in result.output


@patch.object(StackletContext, "_write_token", Mock())
def test_submit_run():
    path = str(pathlib.Path(__file__).parent.resolve()) + "/terraform/good"
    runner = CliRunner()
    with patch.object(
        RestExecutor,
        "get",
        side_effect=[
            get_mock_response(json=get_policies_for_project_response),
        ],
    ):
        with patch.object(
            RestExecutor,
            "post",
            side_effect=[
                get_mock_response(json=create_scan_response),
            ],
        ) as patched_post:
            result = runner.invoke(cli, ["run", "--project", "foo", "-d", path])
            if result.exception:
                # silent exceptions in tests are hard to debug; raise for visibility
                raise result.exception

            patched_post.assert_called_once()
            # path
            assert patched_post.mock_calls[0].args[0] == "/scans"
            # query params
            assert patched_post.mock_calls[0].args[1] == {}
            # payload
            assert patched_post.mock_calls[0].args[2]["project_name"] == "foo"
            assert patched_post.mock_calls[0].args[2]["status"] == "PASSED"
            assert len(patched_post.mock_calls[0].args[2]["results"]) == 0


@patch.object(StackletContext, "_write_token", Mock())
def test_submit_run_fail():
    path = str(pathlib.Path(__file__).parent.resolve()) + "/terraform/bad"
    runner = CliRunner()
    with patch.object(
        RestExecutor,
        "get",
        side_effect=[
            get_mock_response(json=get_policies_for_project_response),
        ],
    ):
        with patch.object(
            RestExecutor,
            "post",
            return_value=[
                get_mock_response(json=create_scan_response),
            ],
        ) as patched_post:
            runner.invoke(cli, ["run", "--project", "foo", "-d", path])
            patched_post.assert_called_once()
            # path
            assert patched_post.mock_calls[0].args[0] == "/scans"
            # query params
            assert patched_post.mock_calls[0].args[1] == {}
            # payload
            assert patched_post.mock_calls[0].args[2]["project_name"] == "foo"
            assert patched_post.mock_calls[0].args[2]["status"] == "FAILED"
            assert len(patched_post.mock_calls[0].args[2]["results"]) == 1
            assert (
                patched_post.mock_calls[0].args[2]["results"][0]["policy"]["name"] == "check-tags"
            )
            assert (
                patched_post.mock_calls[0].args[2]["results"][0]["resource"]["__tfmeta"]["path"]
                == "aws_sqs_queue.test_sqs"
            )


@patch.object(StackletContext, "_write_token", Mock())
def test_submit_run_nested_module_file_path():
    """Resources in a non-root module whose for_each is built from a
    path.module file read must still reach policy evaluation.

    Path-based functions used to resolve relative to the module directory,
    so composing them with the project-root-relative path.module produced a
    duplicated module prefix. The read returned null, the for_each expanded
    to nothing, and the resource never entered the graph, which made a
    non-compliant configuration report as a silent pass.
    """
    path = str(pathlib.Path(__file__).parent.resolve()) + "/terraform/nested-module"
    runner = CliRunner()
    with patch.object(
        RestExecutor,
        "get",
        side_effect=[
            get_mock_response(json=get_policies_for_project_response),
        ],
    ):
        with patch.object(
            RestExecutor,
            "post",
            return_value=get_mock_response(json=create_scan_response),
        ) as patched_post:
            result = runner.invoke(cli, ["run", "--project", "foo", "-d", path])
            # a policy violation exits non-zero, so SystemExit is expected here;
            # anything else is a real error, and silent exceptions in tests are
            # hard to debug, so raise for visibility
            if result.exception is not None and not isinstance(result.exception, SystemExit):
                raise result.exception

            patched_post.assert_called_once()
            payload = patched_post.mock_calls[0].args[2]
            # the whole point: a skipped resource leaves this PASSED with no results
            assert payload["status"] == "FAILED"
            assert len(payload["results"]) == 1
            resource = payload["results"][0]["resource"]
            # violations inside a module are reported against the module block,
            # with the expanded resource instances in refs
            assert resource["__tfmeta"]["path"] == "module.a"
            assert resource["__tfmeta"]["refs"] == ['module.a.aws_sqs_queue.x["queue-1"]']
