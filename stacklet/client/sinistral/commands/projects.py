# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
# This is a generated file, created by scripts/parse.py
from stacklet.client.sinistral.client import Client, ClientCommand, client_registry
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("projects")
class Projects(Client):
    """
    Projects Client
    """

    commands = PluginRegistry("commands")


@Projects.commands.register("list")
class List(ClientCommand):
    """
    List all projects
    """

    command = "list"
    method = "get"
    path = "/projects"
    params = {}
    query_params = {}
    payload_params = {}


@Projects.commands.register("create")
class Create(ClientCommand):
    """
    Create a project
    """

    command = "create"
    method = "post"
    path = "/projects"
    params = {}
    query_params = {}
    payload_params = {
        "schema": {
            "title": "AddProjectInput",
            "required": ["name"],
            "type": "object",
            "properties": {
                "name": {"title": "Name", "type": "string"},
                "collections": {
                    "title": "Collections",
                    "uniqueItems": True,
                    "type": "array",
                    "items": {"type": "string"},
                },
                "groups": {
                    "title": "Group",
                    "type": "object",
                    "properties": {
                        "read": {
                            "title": "Read",
                            "uniqueItems": True,
                            "type": "array",
                            "items": {"type": "string"},
                        }
                    },
                },
            },
        }
    }


@Projects.commands.register("get")
class Get(ClientCommand):
    """
    Get a project by name
    """

    command = "get"
    method = "get"
    path = "/projects/{name}"
    params = {"--name": {"required": True}}
    query_params = {"--include_default_collections": {"required": False}}
    payload_params = {}


@Projects.commands.register("update")
class Update(ClientCommand):
    """
    Update a project
    """

    command = "update"
    method = "put"
    path = "/projects/{name}"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {
        "schema": {
            "title": "UpdateProjectInput",
            "type": "object",
            "properties": {
                "collections": {
                    "title": "Collections",
                    "uniqueItems": True,
                    "type": "array",
                    "items": {"type": "string"},
                },
                "groups": {
                    "title": "Group",
                    "type": "object",
                    "properties": {
                        "read": {
                            "title": "Read",
                            "uniqueItems": True,
                            "type": "array",
                            "items": {"type": "string"},
                        }
                    },
                },
            },
        }
    }


@Projects.commands.register("delete")
class Delete(ClientCommand):
    """
    Delete a project
    """

    command = "delete"
    method = "delete"
    path = "/projects/{name}"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}


@Projects.commands.register("get-collections")
class GetCollections(ClientCommand):
    """
    Get policy collections for a project
    """

    command = "get_collections"
    method = "get"
    path = "/projects/{name}/collections"
    params = {"--name": {"required": True}}
    query_params = {"--include_defaults": {"required": False}}
    payload_params = {}


@Projects.commands.register("add-collections")
class AddCollections(ClientCommand):
    """
    Add policy collections to a project
    """

    command = "add_collections"
    method = "post"
    path = "/projects/{name}/collections"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {
        "schema": {
            "title": "AddCollectionsProjectInput",
            "required": ["collections"],
            "type": "object",
            "properties": {
                "collections": {
                    "title": "Collections",
                    "minItems": 1,
                    "uniqueItems": True,
                    "type": "array",
                    "items": {"type": "string"},
                }
            },
        }
    }


@Projects.commands.register("delete-collections")
class DeleteCollections(ClientCommand):
    """
    Delete policy collections from a project
    """

    command = "delete_collections"
    method = "delete"
    path = "/projects/{name}/collections"
    params = {"--name": {"required": True}}
    query_params = {"--collection": {"required": True}}
    payload_params = {}


@Projects.commands.register("get-policies")
class GetPolicies(ClientCommand):
    """
    Get policies for a project
    """

    command = "get_policies"
    method = "get"
    path = "/projects/{name}/policies"
    params = {"--name": {"required": True}}
    query_params = {"--include_defaults": {"required": False}}
    payload_params = {}


@Projects.commands.register("add-groups")
class AddGroups(ClientCommand):
    """
    Add groups to a project
    """

    command = "add_groups"
    method = "post"
    path = "/projects/{name}/groups/{group_type}"
    params = {"--name": {"required": True}, "--group_type": {"required": True}}
    query_params = {}
    payload_params = {
        "schema": {
            "title": "GroupNamesInput",
            "required": ["group_names"],
            "type": "object",
            "properties": {
                "group_names": {
                    "title": "Group Names",
                    "minItems": 1,
                    "uniqueItems": True,
                    "type": "array",
                    "items": {"type": "string"},
                }
            },
        }
    }


@Projects.commands.register("delete-groups")
class DeleteGroups(ClientCommand):
    """
    Delete groups from a project
    """

    command = "delete_groups"
    method = "delete"
    path = "/projects/{name}/groups/{group_type}"
    params = {"--name": {"required": True}, "--group_type": {"required": True}}
    query_params = {"--group_name": {"required": True}}
    payload_params = {}


@Projects.commands.register("get-credentials")
class GetCredentials(ClientCommand):
    """
    Get current Project Credentials.
    """

    command = "get_credentials"
    method = "get"
    path = "/projects/{name}/credentials"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}


@Projects.commands.register("regenerate-credentials")
class RegenerateCredentials(ClientCommand):
    """
    Regenerate and return Project Credentials.
    """

    command = "regenerate_credentials"
    method = "post"
    path = "/projects/{name}/credentials"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}


@Projects.commands.register("revoke-credentials")
class RevokeCredentials(ClientCommand):
    """
    Revoke any existing Project Credentials.
    """

    command = "revoke_credentials"
    method = "delete"
    path = "/projects/{name}/credentials"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}
