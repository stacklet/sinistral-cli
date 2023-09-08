# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
import json
import os
import tempfile

from pathlib import Path

from unittest.mock import patch

import pytest


config = {
    "api": "https://api.sinistral.acme.org",
    "region": "us-east-1",
    "cognito_client_id": "foo",
    "cognito_user_pool_id": "bar",
    "idp_id": "baz",
    "auth_url": "https://auth.sinistral.acme.org",
}


@pytest.fixture(scope="session", autouse=True)
def config_fixture(request):
    with tempfile.TemporaryDirectory() as config_dir:
        Path(config_dir, "config.json").write_text(json.dumps(config))
        Path(config_dir, "credentials").write_text("foo")
        patched_env = patch.dict(os.environ, {"SINISTRAL_CONFIG": config_dir})
        patched_env.start()
        yield
        patched_env.stop()
