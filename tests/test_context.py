# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
import tempfile
from unittest.mock import Mock

import pytest

from stacklet.client.sinistral.context import StackletContext
from stacklet.client.sinistral.config import StackletConfig
from stacklet.client.sinistral.exceptions import ConfigValidationException


def test_context():
    ctx = Mock(
        obj={
            "config": StackletConfig("tmp"),
            "output": "yaml",
            "formatter": None,
        }
    )
    ctx.obj["config"].update(
        {
            "api": "https://api.sinistral.acme.org",
            "region": "us-east-1",
            "cognito_client_id": "foo",
            "cognito_user_pool_id": "bar",
            "idp_id": "baz",
            "auth_url": "https://auth.sinistral.acme.org",
        }
    )
    context = StackletContext(ctx)
    assert isinstance(context.config, StackletConfig)
    with context:
        assert context.can_sso_auth() is True


def test_credential_write():
    with tempfile.TemporaryDirectory() as temp:
        ctx = Mock(
            obj={
                "config": StackletConfig(temp),
                "output": "yaml",
                "formatter": None,
            }
        )
        context = StackletContext(ctx)
        context.write_access_token("foo")
        assert context.get_access_token() == "foo"


def test_credential_write_no_parent_dirs():
    with tempfile.TemporaryDirectory() as temp:
        ctx = Mock(
            obj={
                "config": StackletConfig(f"{temp}/nonexistant"),
                "output": "yaml",
                "formatter": None,
            }
        )
        context = StackletContext(ctx)
        context.write_access_token("foo")
        assert context.get_access_token() == "foo"


def test_validate_config_when_context_entered():
    with tempfile.TemporaryDirectory() as temp:
        ctx = Mock(
            obj={
                "config": StackletConfig(f"{temp}/nonexistant"),
                "output": "yaml",
                "formatter": None,
            }
        )
        context = StackletContext(ctx)
        with pytest.raises(ConfigValidationException):
            with context:
                assert False, "shouldn't get here"
