# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
import os

from pytest import MonkeyPatch
from stacklet.client.sinistral.output import SinistralFormat
from unittest.mock import MagicMock, patch


@patch("stacklet.client.sinistral.output.sinistral_client")
def test_output(patched_client):
    mock_context = MagicMock()
    mock_config = MagicMock()
    mock_config.dryrun = False
    mock_config.project = None
    s_format = SinistralFormat(mock_context, mock_config)
    s_format.results = []
    s_format.config.output_query = None

    envvars = {
        "GITHUB_SERVER_URL": "https://github.com",
        "GITHUB_REPOSITORY": "stacklet/sinistral-cli",
        "GITHUB_SHA": "abc123",
        "GITHUB_REF": "refs/pull/1337/merge",
        "GITHUB_HEAD_REF": "stacklet-dev/test-branch",
        "GITHUB_ACTIONS": "true",
        "GITHUB_RUN_ID": "1337",
    }
    with MonkeyPatch.context() as mp:
        for k, v in envvars.items():
            mp.setenv(k, v)

        s_format.on_execution_ended()

    # client instantiated
    assert patched_client.mock_calls[0].args == ()
    assert patched_client().mock_calls[0].args == ("scans",)

    # create scan called
    assert patched_client().client().create.mock_calls[0].kwargs == {
        "project_name": None,
        "results": [],
        "status": "PASSED",
        "ci_info": {
            "branch": "stacklet-dev/test-branch",
            "build_code": "1337",
            "build_url": "https://github.com/stacklet/sinistral-cli/actions/runs/1337",
            "commit_sha": "abc123",
            "job_code": "",
            "pull_request_number": "1337",
            "service": "github-actions",
        },
    }


@patch("stacklet.client.sinistral.output.sinistral_client")
def test_output_dryrun(patched_client):
    mock_context = MagicMock()
    mock_config = MagicMock()

    s_format = SinistralFormat(mock_context, mock_config)
    s_format.dryrun = True
    s_format.results = []
    s_format.config.output_query = None

    s_format.on_execution_ended()

    # client not instantiated
    assert patched_client.mock_calls == []
