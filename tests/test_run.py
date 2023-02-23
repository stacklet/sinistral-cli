import pathlib

from click.testing import CliRunner

from unittest.mock import patch

from .test_client import get_mock_response

from stacklet.client.sinistral.cli import cli
from stacklet.client.sinistral.executor import RestExecutor
from stacklet.client.sinistral.context import StackletContext


get_project_response = {
    "name": "foo",
    "collections": ["my-collection"],
    "groups": {
        "read": [
            "admin",
        ]
    },
    "client_id": "foobar",
    "created_at": "2022-12-16T00:33:39.893305+00:00",
    "updated_at": "2023-02-17T14:40:49.394311+00:00",
}

get_policy_collection_response = {
    "name": "my-collection",
    "policies": ["check-tags"],
    "created_at": "2023-01-23T20:25:50.517860+00:00",
    "updated_at": "2023-01-23T20:25:50.517868+00:00",
}

get_policies_for_collection_response = [
    {
        "name": "check-tags",
        "source_name": "csd-policies",
        "raw_policy": {
            "name": "check-tags",
            "description": "resources should be tagged",
            "resource": "terraform.aws_*",
            "metadata": {"severity": "HIGH"},
            "filters": [{"__tfmeta.type": "resource"}, {"tags.Environment": "absent"}],
        },
        "resource": "terraform.aws_*",
        "severity": "high",
        "created_at": "2022-12-14T19:11:18.528637+00:00",
        "updated_at": "2022-12-14T19:11:18.528637+00:00",
    }
]

create_scan_response = {
    "id": "278741d4-99a7-4ca7-80e2-1cbd49d8391b",
    "project_name": "foo",
    "status": "PASSED",
    "summary": {"HIGH": 0, "MEDIUM": 0, "LOW": 0},
    "trigger": "USER",
    "user_id": "foo@bar.com",
    "client_id": "none",
    "sort": 0,
    "created_at": "2023-02-23T00:28:53.921774+00:00",
}


def test_run_command():
    runner = CliRunner()
    result = runner.invoke(cli, ["run", "--help"])
    assert "policy-dir" not in result.output


@patch.object(StackletContext, "DEFAULT_CREDENTIALS", "/dev/null")
def test_submit_run():
    path = str(pathlib.Path(__file__).parent.resolve()) + "/terraform/good"
    runner = CliRunner()
    with patch.object(
        RestExecutor,
        "get",
        side_effect=[
            get_mock_response(json=get_project_response),
            get_mock_response(json=get_policies_for_collection_response),
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
            assert patched_post.mock_calls[0].args[2]["status"] == "PASSED"
            assert len(patched_post.mock_calls[0].args[2]["results"]) == 0


@patch.object(StackletContext, "DEFAULT_CREDENTIALS", "/dev/null")
def test_submit_run_fail():
    path = str(pathlib.Path(__file__).parent.resolve()) + "/terraform/bad"
    runner = CliRunner()
    with patch.object(
        RestExecutor,
        "get",
        side_effect=[
            get_mock_response(json=get_project_response),
            get_mock_response(json=get_policies_for_collection_response),
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
                patched_post.mock_calls[0].args[2]["results"][0]["policy"]["name"]
                == "check-tags"
            )
            assert (
                patched_post.mock_calls[0].args[2]["results"][0]["resource"][
                    "__tfmeta"
                ]["path"]
                == "aws_sqs_queue.test_sqs"
            )
