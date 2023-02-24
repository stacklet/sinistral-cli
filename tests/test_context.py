import json
import os
import tempfile

from stacklet.client.sinistral.context import StackletContext, StackletCredentialWriter
from stacklet.client.sinistral.config import StackletConfig


def test_context():
    config = {
        "api": "https://api.sinistral.acme.org",
        "region": "us-east-1",
        "cognito_client_id": "foo",
        "cognito_user_pool_id": "bar",
        "idp_id": "baz",
        "auth_url": "https://auth.sinistral.acme.org",
        "cubejs": "",
    }
    context = StackletContext(raw_config=config)
    assert isinstance(context.config, StackletConfig)
    with context:
        assert context.can_sso_login() is True


def test_context_from_file():
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

    context = StackletContext(config=temp.name)

    assert isinstance(context.config, StackletConfig)
    with context:
        assert context.can_sso_login() is True

    os.unlink(temp.name)


def test_context_from_file_default():
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

    context = StackletContext()
    assert isinstance(context.config, StackletConfig)
    with context:
        assert context.can_sso_login() is True

    os.unlink(temp.name)


def test_credential_writer():
    temp = tempfile.NamedTemporaryFile(delete=False)
    writer = StackletCredentialWriter("foo", temp.name)
    writer()
    with open(temp.name) as f:
        assert f.read() == "foo"
    os.unlink(temp.name)


def test_credential_writer_no_parent_dirs():
    non_existant_file = "/tmp/foo/bar/baz"
    assert os.path.exists(non_existant_file) is False
    writer = StackletCredentialWriter("foo", non_existant_file)
    writer()
    with open(non_existant_file) as f:
        assert f.read() == "foo"

    os.unlink(non_existant_file)
    os.rmdir(os.path.dirname(non_existant_file))
