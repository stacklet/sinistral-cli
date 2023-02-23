# This is a generated file, created by scripts/parse.py
from stacklet.client.sinistral.client import client_registry, ClientCommand, Client
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("policy-sources")
class PolicySources(Client):
    """
    PolicySources Client
    """

    commands = PluginRegistry("commands")


@PolicySources.commands.register("get-policy-sources")
class GetPolicySources(ClientCommand):
    """
    Get Policy Sources
    """

    command = "get_policy_sources"
    method = "get"
    path = "/policy-sources"
    params = {}
    query_params = {}
    payload_params = {}


@PolicySources.commands.register("create-policy-source")
class CreatePolicySource(ClientCommand):
    """
    Create Policy Source
    """

    command = "create_policy_source"
    method = "post"
    path = "/policy-sources"
    params = {}
    query_params = {}
    payload_params = {
        "schema": {
            "title": "PolicySourceInput",
            "required": ["name", "url"],
            "type": "object",
            "properties": {
                "name": {"title": "Name", "type": "string"},
                "url": {
                    "title": "Url",
                    "maxLength": 65536,
                    "minLength": 1,
                    "type": "string",
                    "format": "uri",
                },
                "extensions": {
                    "title": "Extensions",
                    "minItems": 1,
                    "type": "array",
                    "items": {"type": "string"},
                    "default": [".yml", ".yaml"],
                },
                "paths": {
                    "title": "Paths",
                    "type": "array",
                    "items": {"type": "string"},
                },
                "branch": {"title": "Branch", "type": "string"},
                "auth": {
                    "title": "Auth",
                    "anyOf": [
                        {
                            "title": "RepositoryAuthToken",
                            "required": ["username", "token"],
                            "type": "object",
                            "properties": {
                                "username": {"title": "Username", "type": "string"},
                                "token": {
                                    "title": "Token",
                                    "type": "string",
                                    "format": "password",
                                    "writeOnly": True,
                                },
                            },
                        },
                        {
                            "title": "RepositoryAuthSSH",
                            "required": ["username", "ssh_key"],
                            "type": "object",
                            "properties": {
                                "username": {"title": "Username", "type": "string"},
                                "ssh_key": {
                                    "title": "Ssh Key",
                                    "type": "string",
                                    "format": "password",
                                    "writeOnly": True,
                                },
                                "ssh_passphrase": {
                                    "title": "Ssh Passphrase",
                                    "type": "string",
                                    "format": "password",
                                    "writeOnly": True,
                                },
                            },
                        },
                    ],
                },
            },
        }
    }


@PolicySources.commands.register("get-policy-source-by-name")
class GetPolicySourceByName(ClientCommand):
    """
    Get Policy Source By Name
    """

    command = "get_policy_source_by_name"
    method = "get"
    path = "/policy-sources/{name}"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}


@PolicySources.commands.register("delete-policy-source-by-name")
class DeletePolicySourceByName(ClientCommand):
    """
    Delete Policy Source By Name
    """

    command = "delete_policy_source_by_name"
    method = "delete"
    path = "/policy-sources/{name}"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}


@PolicySources.commands.register("update-policy-source")
class UpdatePolicySource(ClientCommand):
    """
    Update Policy Source
    """

    command = "update_policy_source"
    method = "patch"
    path = "/policy-sources/{name}"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {
        "schema": {
            "title": "UpdatePolicySource",
            "type": "object",
            "properties": {
                "url": {
                    "title": "Url",
                    "maxLength": 65536,
                    "minLength": 1,
                    "type": "string",
                    "format": "uri",
                },
                "paths": {
                    "title": "Paths",
                    "type": "array",
                    "items": {"type": "string"},
                },
                "extensions": {
                    "title": "Extensions",
                    "minItems": 1,
                    "type": "array",
                    "items": {"type": "string"},
                },
                "branch": {"title": "Branch", "type": "string"},
                "auth": {
                    "title": "Auth",
                    "anyOf": [
                        {
                            "title": "RepositoryAuthToken",
                            "required": ["username", "token"],
                            "type": "object",
                            "properties": {
                                "username": {"title": "Username", "type": "string"},
                                "token": {
                                    "title": "Token",
                                    "type": "string",
                                    "format": "password",
                                    "writeOnly": True,
                                },
                            },
                        },
                        {
                            "title": "RepositoryAuthSSH",
                            "required": ["username", "ssh_key"],
                            "type": "object",
                            "properties": {
                                "username": {"title": "Username", "type": "string"},
                                "ssh_key": {
                                    "title": "Ssh Key",
                                    "type": "string",
                                    "format": "password",
                                    "writeOnly": True,
                                },
                                "ssh_passphrase": {
                                    "title": "Ssh Passphrase",
                                    "type": "string",
                                    "format": "password",
                                    "writeOnly": True,
                                },
                            },
                        },
                    ],
                },
            },
        }
    }


@PolicySources.commands.register("get-policies-for-source")
class GetPoliciesForSource(ClientCommand):
    """
    Get Policies For Source
    """

    command = "get_policies_for_source"
    method = "get"
    path = "/policy-sources/{name}/policies"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}


@PolicySources.commands.register("scan-policy-source")
class ScanPolicySource(ClientCommand):
    """
    Scan Policy Source
    """

    command = "scan_policy_source"
    method = "post"
    path = "/policy-sources/{name}/scans"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}
