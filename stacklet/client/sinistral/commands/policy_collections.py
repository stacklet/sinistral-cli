# This is a generated file, created by scripts/parse.py
from stacklet.client.sinistral.client import client_registry, ClientCommand, Client
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("policy-collections")
class PolicyCollections(Client):
    """
    PolicyCollections Client
    """

    commands = PluginRegistry("commands")


@PolicyCollections.commands.register("get-policy-collections")
class GetPolicyCollections(ClientCommand):
    """
    Get Policy Collections
    """

    command = "get_policy_collections"
    method = "get"
    path = "/policy-collections"
    params = {}
    query_params = {}
    payload_params = {}


@PolicyCollections.commands.register("create-policy-collection")
class CreatePolicyCollection(ClientCommand):
    """
    Create Policy Collection
    """

    command = "create_policy_collection"
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
            },
        }
    }


@PolicyCollections.commands.register("get-policy-collection-by-name")
class GetPolicyCollectionByName(ClientCommand):
    """
    Get Policy Collection By Name
    """

    command = "get_policy_collection_by_name"
    method = "get"
    path = "/policy-collections/{name}"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}


@PolicyCollections.commands.register("delete-policy-collection")
class DeletePolicyCollection(ClientCommand):
    """
    Delete Policy Collection
    """

    command = "delete_policy_collection"
    method = "delete"
    path = "/policy-collections/{name}"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}


@PolicyCollections.commands.register("get-policies-for-collection")
class GetPoliciesForCollection(ClientCommand):
    """
    Get Policies For Collection
    """

    command = "get_policies_for_collection"
    method = "get"
    path = "/policy-collections/{name}/policies"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}


@PolicyCollections.commands.register("update-policies-for-collection")
class UpdatePoliciesForCollection(ClientCommand):
    """
    Update Policies For Collection
    """

    command = "update_policies_for_collection"
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


@PolicyCollections.commands.register("add-policies-to-collection")
class AddPoliciesToCollection(ClientCommand):
    """
    Add Policies To Collection
    """

    command = "add_policies_to_collection"
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


@PolicyCollections.commands.register("remove-policies-from-collection")
class RemovePoliciesFromCollection(ClientCommand):
    """
    Remove Policies From Collection
    """

    command = "remove_policies_from_collection"
    method = "delete"
    path = "/policy-collections/{name}/policies"
    params = {"--name": {"required": True}}
    query_params = {"--policy": {"required": True}}
    payload_params = {}
