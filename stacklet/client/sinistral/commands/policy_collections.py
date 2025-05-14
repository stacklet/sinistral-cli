# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
# This is a generated file, created by scripts/parse.py
from stacklet.client.sinistral.client import Client, ClientCommand, client_registry
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("policy-collections")
class PolicyCollections(Client):
    """
    PolicyCollections Client
    """

    commands = PluginRegistry("commands")


@PolicyCollections.commands.register("list")
class List(ClientCommand):
    """
    List all (or just defaults) policy collections
    """

    command = "list"
    method = "get"
    path = "/policy-collections"
    params = {}
    query_params = {"--only_defaults": {"required": False}}
    payload_params = {}


@PolicyCollections.commands.register("create")
class Create(ClientCommand):
    """
    Create a new policy collection
    """

    command = "create"
    method = "post"
    path = "/policy-collections"
    params = {}
    query_params = {}
    payload_params = {
        "schema": {
            "title": "PolicyCollectionInput",
            "required": ["name"],
            "type": "object",
            "properties": {
                "name": {"title": "Name", "minLength": 1, "type": "string"},
                "policies": {
                    "title": "Policies",
                    "uniqueItems": True,
                    "type": "array",
                    "items": {"type": "string"},
                    "default": [],
                },
                "is_default": {
                    "title": "Is Default",
                    "type": "boolean",
                    "default": False,
                },
            },
        }
    }


@PolicyCollections.commands.register("get")
class Get(ClientCommand):
    """
    Get a policy collection by name
    """

    command = "get"
    method = "get"
    path = "/policy-collections/{name}"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}


@PolicyCollections.commands.register("delete")
class Delete(ClientCommand):
    """
    Delete a policy collection
    """

    command = "delete"
    method = "delete"
    path = "/policy-collections/{name}"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}


@PolicyCollections.commands.register("update")
class Update(ClientCommand):
    """
    None
    """

    command = "update"
    method = "patch"
    path = "/policy-collections/{name}"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {
        "schema": {
            "title": "UpdatePolicyCollectionInput",
            "type": "object",
            "properties": {
                "is_default": {"title": "Is Default", "type": "boolean"},
                "policies": {
                    "title": "Policies",
                    "uniqueItems": True,
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
        }
    }


@PolicyCollections.commands.register("get-policies")
class GetPolicies(ClientCommand):
    """
    Get policies for a policy collection
    """

    command = "get_policies"
    method = "get"
    path = "/policy-collections/{name}/policies"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}


@PolicyCollections.commands.register("update-policies")
class UpdatePolicies(ClientCommand):
    """
    Update the policies for a policy collection
    """

    command = "update_policies"
    method = "put"
    path = "/policy-collections/{name}/policies"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {
        "schema": {
            "title": "UpdatePoliciesForCollectionInput",
            "required": ["policies"],
            "type": "object",
            "properties": {
                "policies": {
                    "title": "Policies",
                    "uniqueItems": True,
                    "type": "array",
                    "items": {"type": "string"},
                }
            },
        }
    }


@PolicyCollections.commands.register("add-policies")
class AddPolicies(ClientCommand):
    """
    Add policies to a policy collection
    """

    command = "add_policies"
    method = "post"
    path = "/policy-collections/{name}/policies"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {
        "schema": {
            "title": "AddPoliciesPolicyCollectionInput",
            "required": ["policies"],
            "type": "object",
            "properties": {
                "policies": {
                    "title": "Policies",
                    "minItems": 1,
                    "uniqueItems": True,
                    "type": "array",
                    "items": {"type": "string"},
                }
            },
        }
    }


@PolicyCollections.commands.register("delete-policies")
class DeletePolicies(ClientCommand):
    """
    Delete policies from a policy collection
    """

    command = "delete_policies"
    method = "delete"
    path = "/policy-collections/{name}/policies"
    params = {"--name": {"required": True}}
    query_params = {"--policy": {"required": True}}
    payload_params = {}
