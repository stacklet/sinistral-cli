# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
# This is a generated file, created by scripts/parse.py
from stacklet.client.sinistral.client import Client, ClientCommand, client_registry
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("policy-sources")
class PolicySources(Client):
    """
    PolicySources Client
    """

    commands = PluginRegistry("commands")


@PolicySources.commands.register("list")
class List(ClientCommand):
    """
    List all policy sources
    """

    command = "list"
    method = "get"
    path = "/policy-sources"
    params = {}
    query_params = {}
    payload_params = {}


@PolicySources.commands.register("create")
class Create(ClientCommand):
    """
    Create a new policy source
    """

    command = "create"
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


@PolicySources.commands.register("get")
class Get(ClientCommand):
    """
    Get a policy source by name
    """

    command = "get"
    method = "get"
    path = "/policy-sources/{name}"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}


@PolicySources.commands.register("delete")
class Delete(ClientCommand):
    """
    Delete a policy source by name
    """

    command = "delete"
    method = "delete"
    path = "/policy-sources/{name}"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}


@PolicySources.commands.register("update")
class Update(ClientCommand):
    """
    Update a policy source
    """

    command = "update"
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


@PolicySources.commands.register("policies")
class Policies(ClientCommand):
    """
    Get all policies for a source
    """

    command = "policies"
    method = "get"
    path = "/policy-sources/{name}/policies"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}


@PolicySources.commands.register("scan")
class Scan(ClientCommand):
    """
    Scan a policy source
    """

    command = "scan"
    method = "post"
    path = "/policy-sources/{name}/scans"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}
