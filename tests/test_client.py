import json

from unittest.mock import MagicMock, patch

import click
import pytest

from .utils import get_mock_response

from stacklet.client.sinistral.client import (
    validate_list,
    validate_types,
    parse_jsonschema,
    sinistral_client,
)
from stacklet.client.sinistral.executor import RestExecutor


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
        res = client.get_projects()
        assert res == {"foo": "bar"}


def test_client_command_post():
    client = sinistral_client().client("projects")
    with patch.object(
        RestExecutor, "post", return_value=get_mock_response(json={"created": True})
    ):
        res = client.create_project(name="foo", collections=[], groups={})
        assert res == {"created": True}


def test_client_command_put():
    client = sinistral_client().client("projects")
    with patch.object(
        RestExecutor, "put", return_value=get_mock_response(json={"updated": True})
    ):
        res = client.update_project(name="foo", collections=[], groups={})
        assert res == {"updated": True}


def test_client_command_delete():
    client = sinistral_client().client("projects")
    with patch.object(
        RestExecutor, "delete", return_value=get_mock_response(json={"deleted": True})
    ):
        res = client.delete_project(name="foo")
        assert res == {"deleted": True}


def test_client_command_unauthorized():
    client = sinistral_client().client("projects")
    with patch.object(
        RestExecutor,
        "delete",
        return_value=get_mock_response(json={"message": "Unauthorized"}),
    ):
        with pytest.raises(Exception):
            client.delete_project(name="foo")


def test_client_command_other_error():
    client = sinistral_client().client("projects")
    with patch.object(
        RestExecutor,
        "delete",
        return_value=get_mock_response(json={"detail": "An Error Message"}),
    ):
        with pytest.raises(Exception):
            client.delete_project(name="foo")


def test_client_command_other_error_400():
    client = sinistral_client().client("projects")
    with patch.object(
        RestExecutor, "delete", return_value=get_mock_response(status_code=400, json={})
    ):
        with pytest.raises(Exception):
            client.delete_project(name="foo")


def test_client_command_other_error_500():
    client = sinistral_client().client("projects")
    with patch.object(
        RestExecutor, "delete", return_value=get_mock_response(status_code=500, json={})
    ):
        with pytest.raises(Exception):
            client.delete_project(name="foo")


def test_client_command_uses_query_params():
    client = sinistral_client().client("policy")
    with patch.object(
        RestExecutor, "get", return_value=get_mock_response(json={"a": "policy"})
    ) as patched:
        res = client.get_policies(pagesize=1)
        patched.assert_called_once_with("/policies", {"pageSize": 1}, {})
        assert res == {"a": "policy"}