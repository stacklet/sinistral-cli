# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
import json

from unittest.mock import MagicMock, patch

import click
import pytest

from stacklet.client.sinistral.client import (
    parse_jsonschema,
    sinistral_client,
    validate_list,
    validate_types,
)
from stacklet.client.sinistral.context import StackletContext
from stacklet.client.sinistral.executor import RestExecutor

from .utils import get_mock_response


@pytest.fixture(autouse=True, scope="module")
def mock_current_context():
    with patch("click.get_current_context") as ctx:
        ctx().obj = {
            "output": "raw",
            "formatter": None,
            "config": MagicMock(
                project_client_id=None,
                project_client_secret=None,
                org_client_id=None,
                org_client_secret=None,
            ),
        }
        yield ctx


@pytest.fixture(autouse=True, scope="module")
def mock_access_token():
    with patch.object(StackletContext, "_ACCESS_TOKEN", new="token"):
        yield


@pytest.fixture()
def empty_access_token():
    with patch.object(StackletContext, "_ACCESS_TOKEN", new=None):
        yield


@pytest.fixture()
def mock_project_creds(mock_current_context):
    mock_config = MagicMock(
        project_client_id="client-id",
        project_client_secret="client-secret",
        org_client_id=None,
        org_client_secret=None,
    )
    with patch.dict(mock_current_context().obj, config=mock_config):
        with patch.object(StackletContext, "do_project_auth", return_value="token"):
            with patch.object(StackletContext, "do_org_auth", return_value=None):
                yield


@pytest.fixture()
def mock_org_creds(mock_current_context):
    mock_config = MagicMock(
        project_client_id=None,
        project_client_secret=None,
        org_client_id="client-id",
        org_client_secret="client-secret",
    )
    with patch.dict(mock_current_context().obj, config=mock_config):
        with patch.object(StackletContext, "do_project_auth", return_value=None):
            with patch.object(StackletContext, "do_org_auth", return_value="token"):
                yield


sample_schema = {
    "$id": "https://example.com/person.schema.json",
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Person",
    "type": "object",
    "properties": {
        "firstName": {
            "title": "first name",
            "type": "string",
            "description": "The person's first name.",
        },
        "lastName": {"type": "string", "description": "The person's last name."},
        "sibling_names": {"type": "array", "items": {"type": "string"}},
        "age": {
            "description": "Age in years which must be equal to or greater than zero.",
            "type": "integer",
            "minimum": 0,
            "default": 21,
        },
    },
    "required": ["firstName", "lastName", "age"],
}


def test_validate_list():
    ctx = MagicMock()
    res = validate_list(
        ctx,
        "",
        [
            (
                "f",
                "o",
                "o",
            ),
            ("b", "a", "r"),
        ],
    )
    assert res == ["foo", "bar"]


def test_validate_list_malformed():
    ctx = MagicMock()
    with pytest.raises(click.BadParameter):
        validate_list(ctx, "", 1)
    pass


def test_validate_types():
    ctx = MagicMock()
    res = validate_types(["string", "number"], {}, ctx, "", 1)
    assert res == 1

    ctx = MagicMock()
    res = validate_types(["integer", "string"], {}, ctx, "", 1)
    assert res == 1


def test_validate_types_bad_parameter():
    ctx = MagicMock()
    with pytest.raises(click.BadParameter):
        validate_types(["int", "string"], {}, ctx, "", 1.0)


def test_validate_types_object_string():
    ctx = MagicMock()
    res = validate_types(["object", "string"], sample_schema, ctx, "", "asdf")
    assert res == "asdf"


def test_validate_types_json():
    ctx = MagicMock()
    res = validate_types(
        ["object"],
        sample_schema,
        ctx,
        "",
        json.dumps({"firstName": "foo", "lastName": "bar", "age": 21}),
    )
    assert isinstance(res, dict)
    assert res["firstName"] == "foo"
    assert res["lastName"] == "bar"
    assert res["age"] == 21


def test_validate_types_json_malformed():
    ctx = MagicMock()
    with pytest.raises(click.BadParameter):
        validate_types(["object"], sample_schema, ctx, "", "foo")


def test_parse_jsonschema():
    parsed = parse_jsonschema(sample_schema)
    assert parsed == {
        "age": {"default": 21, "help": None, "required": True, "show_default": True},
        "firstName": {"help": "first name", "required": True},
        "lastName": {"help": None, "required": True},
        "sibling_names": {
            "callback": validate_list,
            "help": None,
            "multiple": True,
            "type": list,
        },
    }


def test_parse_jsonschema_no_schema():
    parsed = parse_jsonschema(None)
    assert parsed == {}

    parsed = parse_jsonschema({})
    assert parsed == {}


def test_sinistral_client_fake():
    with pytest.raises(Exception):
        sinistral_client().client("fake")


def test_sinistral_client_clients_instantiated():
    client = sinistral_client().client("projects")

    assert len(client.commands.keys()) != 0

    # assert all the commands are available on the client
    for c in client.commands.keys():
        assert hasattr(client, c.replace("-", "_"))

    with pytest.raises(AttributeError):
        client.some_non_existant_command()
        pass


def test_client_command_get():
    client = sinistral_client().client("projects")
    with patch.object(
        RestExecutor, "get", return_value=get_mock_response(json={"foo": "bar"})
    ):
        res = client.list()
        assert res == {"foo": "bar"}


def test_client_command_post():
    client = sinistral_client().client("projects")
    with patch.object(
        RestExecutor, "post", return_value=get_mock_response(json={"created": True})
    ):
        res = client.create(name="foo", collections=[], groups={})
        assert res == {"created": True}


def test_client_command_put():
    client = sinistral_client().client("projects")
    with patch.object(
        RestExecutor, "put", return_value=get_mock_response(json={"updated": True})
    ):
        res = client.update(name="foo", collections=[], groups={})
        assert res == {"updated": True}


def test_client_command_delete():
    client = sinistral_client().client("projects")
    with patch.object(
        RestExecutor, "delete", return_value=get_mock_response(json={"deleted": True})
    ):
        res = client.delete(name="foo")
        assert res == {"deleted": True}


def test_client_command_unauthorized():
    client = sinistral_client().client("projects")
    with patch.object(
        RestExecutor,
        "delete",
        return_value=get_mock_response(json={"message": "Unauthorized"}),
    ):
        with pytest.raises(Exception):
            client.delete(name="foo")


def test_client_command_auto_project_auth(empty_access_token, mock_project_creds):
    client = sinistral_client().client("projects")
    with patch.object(
        RestExecutor, "get", return_value=get_mock_response(json={"foo": "bar"})
    ):
        res = client.list()
        assert res == {"foo": "bar"}
        assert StackletContext.do_project_auth.called
        assert not StackletContext.do_org_auth.called


def test_client_command_auto_org_auth(empty_access_token, mock_org_creds):
    client = sinistral_client().client("projects")
    with patch.object(
        RestExecutor, "get", return_value=get_mock_response(json={"foo": "bar"})
    ):
        res = client.list()
        assert res == {"foo": "bar"}
        assert not StackletContext.do_project_auth.called
        assert StackletContext.do_org_auth.called


def test_client_command_other_error():
    client = sinistral_client().client("projects")
    with patch.object(
        RestExecutor,
        "delete",
        return_value=get_mock_response(json={"detail": "An Error Message"}),
    ):
        with pytest.raises(Exception):
            client.delete(name="foo")


def test_client_command_other_error_400():
    client = sinistral_client().client("projects")
    with patch.object(
        RestExecutor, "delete", return_value=get_mock_response(status_code=400, json={})
    ):
        with pytest.raises(Exception):
            client.delete(name="foo")


def test_client_command_other_error_500():
    client = sinistral_client().client("projects")
    with patch.object(
        RestExecutor, "delete", return_value=get_mock_response(status_code=500, json={})
    ):
        with pytest.raises(Exception):
            client.delete(name="foo")


def test_client_command_uses_query_params():
    client = sinistral_client().client("policy")
    with patch.object(
        RestExecutor, "get", return_value=get_mock_response(json={"a": "policy"})
    ) as patched:
        res = client.list(pagesize=1)
        patched.assert_called_once_with("/policies", {"pageSize": 1}, {})
        assert res == {"a": "policy"}


@pytest.mark.parametrize("severity", ["HIGH", "high"])
def test_client_command_scan_create(severity):
    client = sinistral_client().client("scans")
    with patch.object(
        RestExecutor, "post", return_value=get_mock_response(json={"id": "new-scan"})
    ) as patched:
        scan_payload = {
            "project_name": "foo",
            "status": "PASSED",
            "results": [
                {
                    "policy": {
                        "name": "foo",
                        "resource": ["foo", "bar"],
                        "description": "foo",
                        "filters": [],
                        "mode": {},
                        "metadata": {"severity": f"{severity}"},
                    },
                    "resource": {
                        "id": "foo",
                        "__tfmeta": {
                            "filename": "foo/bar/baz",
                            "label": "foo",
                            "line_end": 1,
                            "line_start": 1,
                            "path": "foo/bar/baz",
                            "type": "resource",
                            "src_dir": "foo/bar",
                        },
                    },
                    "file_path": "foo/bar/baz",
                    "file_line_start": 1,
                    "file_line_end": 1,
                    "code_block": [["foo"]],
                }
            ],
        }
        res = client.create(**scan_payload, collections=[], groups={})
        patched.assert_called_once_with("/scans", {}, scan_payload)
        assert res == {"id": "new-scan"}
