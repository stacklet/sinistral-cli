import json
import os
import tempfile

from unittest.mock import patch

from stacklet.client.sinistral.context import StackletContext

import pytest


config = {
    "api": "https://api.sinistral.acme.org",
    "region": "us-east-1",
    "cognito_client_id": "foo",
    "cognito_user_pool_id": "bar",
    "idp_id": "baz",
    "auth_url": "https://auth.sinistral.acme.org",
    "cubejs": "",
}


@pytest.fixture(scope="session", autouse=True)
def config_fixture(request):
    temp = tempfile.NamedTemporaryFile(delete=False)
    with open(temp.name, "w") as f:
        json.dump(config, f)

    temp_creds = tempfile.NamedTemporaryFile(delete=False)
    with open(temp_creds.name, "w") as f:
        f.write("foo")

    patched = patch.object(StackletContext, "DEFAULT_CONFIG", temp.name)
    patched.start()

    patched_creds = patch.object(
        StackletContext, "DEFAULT_CREDENTIALS", temp_creds.name
    )
    patched_creds.start()

    def unpatch():
        patched.stop()
        patched_creds.stop()
        os.unlink(temp.name)
        os.unlink(temp_creds.name)

    request.addfinalizer(unpatch)
