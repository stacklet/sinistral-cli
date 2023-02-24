import json
import os
import tempfile

import pytest

from unittest.mock import patch
from stacklet.client.sinistral.config import StackletConfig
from stacklet.client.sinistral.exceptions import ConfigValidationException


def test_stacklet_config_empty():
    temp = tempfile.NamedTemporaryFile(delete=False)

    with open(temp.name, "w") as f:
        json.dump({}, f)

    with patch.dict(os.environ, {"STACKLET_CONFIG": temp.name}):
        with pytest.raises(ConfigValidationException):
            StackletConfig()

    os.unlink(temp.name)


def test_stacklet_config_from_file():
    temp = tempfile.NamedTemporaryFile(delete=False)

    config = {
        "api": "https://api.sinistral.acme.org",
        "region": "us-east-1",
        "cognito_client_id": "foo",
        "cognito_user_pool_id": "bar",
        "idp_id": "baz",
        "auth_url": "https://auth.sinistral.acme.org",
        "cubejs": "",
    }

    with open(temp.name, "w") as f:
        json.dump(config, f)

    with patch.dict(os.environ, {"STACKLET_CONFIG": temp.name}):
        stacklet_config = StackletConfig.from_file(temp.name)
        assert stacklet_config.to_json() == config

    os.unlink(temp.name)
