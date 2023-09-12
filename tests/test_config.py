# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
import json
import tempfile

import pytest

from stacklet.client.sinistral.config import StackletConfig
from stacklet.client.sinistral.exceptions import ConfigValidationException


def test_stacklet_config_empty():
    with tempfile.TemporaryDirectory() as temp:
        with open(f"{temp}/config.json", "w") as f:
            json.dump({}, f)

        with pytest.raises(ConfigValidationException):
            StackletConfig(temp).validate()


def test_stacklet_config_from_file():
    config = {
        "api": "https://api.sinistral.acme.org",
        "region": "us-east-1",
        "cognito_client_id": "foo",
        "cognito_user_pool_id": "bar",
        "idp_id": "baz",
        "auth_url": "https://auth.sinistral.acme.org",
    }
    config2 = dict(config)
    # test backward compatibility
    config2["api_url"] = config2.pop("api")
    config2["cognito_region"] = config2.pop("region")

    with tempfile.TemporaryDirectory() as temp:
        with open(f"{temp}/config.json", "w") as f:
            json.dump(config, f)

        stacklet_config = StackletConfig(temp)
        assert stacklet_config.to_dict() == config2
