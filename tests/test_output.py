# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
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

    s_format.on_execution_ended()

    # client instantiated
    assert patched_client.mock_calls[0].args == ()
    assert patched_client().mock_calls[0].args == ("scans",)

    # create scan called
    assert patched_client().client().create.mock_calls[0].kwargs == {
        "project_name": None,
        "results": [],
        "status": "PASSED",
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
