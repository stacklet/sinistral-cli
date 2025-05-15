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
