# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
import pathlib
from unittest.mock import ANY, call, patch

import pytest
from click.testing import CliRunner


from .utils import (
    get_policies_for_collection_response,
    create_scan_response,
    get_mock_response,
)

from stacklet.client.sinistral.cli import cli
from stacklet.client.sinistral.context import StackletContext


@pytest.fixture(autouse=True)
def mock_rest():
    with patch("stacklet.client.sinistral.client.RestExecutor") as m:
        yield m()


@pytest.fixture
def runner():
    runner = CliRunner()

    def _invoke(*args):
        result = runner.invoke(cli, args)
        if result.exception and not isinstance(result.exception, SystemExit):
            # silent exceptions in tests are hard to debug; raise for visibility
            raise result.exception
        return result

    yield _invoke


@pytest.fixture
def mock_org_auth():
    with patch.object(StackletContext, "is_org_auth", True):
        yield


def test_run_command(runner):
    result = runner("run", "--help")
    assert "policy-dir" in result.output
    assert "project" in result.output


def test_passed(runner, mock_rest):
    path = str(pathlib.Path(__file__).parent.resolve()) + "/terraform/good"
    mock_rest.get.side_effect = [
        get_mock_response(json=get_policies_for_collection_response),
    ]
    mock_rest.post.side_effect = [
        get_mock_response(json=create_scan_response),
    ]

    result = runner("run", "--project", "foo", "-d", path)

    assert result.exit_code == 0, f"Command failed: {result.output}"
    assert mock_rest.post.call_args_list == [
        call("/scans", {}, {"project_name": "foo", "status": "PASSED", "results": []}),
    ]


def test_failed(runner, mock_rest):
    path = str(pathlib.Path(__file__).parent.resolve()) + "/terraform/bad"
    mock_rest.get.side_effect = [
        get_mock_response(json=get_policies_for_collection_response),
    ]
    mock_rest.post.side_effect = [
        get_mock_response(json=create_scan_response),
    ]

    result = runner("run", "--project", "foo", "-d", path)

    assert result.exit_code == 1
    assert mock_rest.post.call_args_list == [
        call(
            "/scans", {}, {"project_name": "foo", "status": "FAILED", "results": [ANY]}
        )
    ]
    scan_result = mock_rest.post.call_args[0][2]["results"][0]
    assert scan_result["policy"]["name"] == "check-tags"
    assert scan_result["resource"]["__tfmeta"]["path"] == "aws_sqs_queue.test_sqs"


def test_no_policies(runner, mock_rest):
    path = str(pathlib.Path(__file__).parent.resolve()) + "/terraform/good"
    mock_rest.get.side_effect = [
        get_mock_response(json=[]),
    ]

    result = runner("run", "--project", "foo", "-d", path)

    assert result.exit_code == 1
    assert not mock_rest.post.called


def test_api_error(runner, mock_rest):
    path = str(pathlib.Path(__file__).parent.resolve()) + "/terraform/good"
    mock_rest.get.side_effect = [
        Exception("test"),
    ]

    result = runner("run", "--project", "foo", "-d", path)

    assert result.exit_code == 1
    assert result.output.strip() == "test"
    assert not mock_rest.post.called


def test_project_auto_create(runner, mock_rest, mock_org_auth):
    path = str(pathlib.Path(__file__).parent.resolve()) + "/terraform/good"
    mock_rest.get.side_effect = [
        Exception("Project foo not found"),
        get_mock_response(json=get_policies_for_collection_response),
    ]
    mock_rest.post.side_effect = [
        get_mock_response(json=None),
        get_mock_response(json=create_scan_response),
    ]

    result = runner("run", "--project", "foo", "-d", path)

    assert result.exit_code == 0, f"Command failed: {result.output}"
    assert mock_rest.post.call_args_list == [
        call("/projects", {}, {"name": "foo", "groups": {"read": []}}),
        call("/scans", {}, {"project_name": "foo", "status": "PASSED", "results": []}),
    ]


def test_project_auto_create_non_org_auth(runner, mock_rest):
    path = str(pathlib.Path(__file__).parent.resolve()) + "/terraform/good"
    mock_rest.get.side_effect = [
        Exception("Project foo not found"),
        get_mock_response(json=get_policies_for_collection_response),
    ]
    mock_rest.post.side_effect = [
        get_mock_response(json=None),
        get_mock_response(json=create_scan_response),
    ]

    result = runner("run", "--project", "foo", "-d", path)

    assert result.exit_code == 1
    assert result.output.strip() == "Project foo not found"
