from stacklet.client.sinistral.client import client_registry, ClientCommand, Client
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("PolicyCollections")
class PolicyCollections(Client):
    """
    PolicyCollections Client
    """

    commands = PluginRegistry("commands")


@PolicyCollections.commands.register("get-policy-collections")
class GetPolicyCollections(ClientCommand):
    """
    get_policy_collections
    """

    command = "get_policy_collections"
    method = "get"
    path = "/policy-collections"
    params = {}


@PolicyCollections.commands.register("create-policy-collection")
class CreatePolicyCollection(ClientCommand):
    """
    create_policy_collection
    """

    command = "create_policy_collection"
    method = "post"
    path = "/policy-collections"
    params = {"--json": {}}


@PolicyCollections.commands.register("get-policy-collection-by-name")
class GetPolicyCollectionByName(ClientCommand):
    """
    get_policy_collection_by_name
    """

    command = "get_policy_collection_by_name"
    method = "get"
    path = "/policy-collections/{name}"
    params = {"--name": {}}


@PolicyCollections.commands.register("delete-policy-collection")
class DeletePolicyCollection(ClientCommand):
    """
    delete_policy_collection
    """

    command = "delete_policy_collection"
    method = "delete"
    path = "/policy-collections/{name}"
    params = {"--name": {}}


@PolicyCollections.commands.register("get-policies-for-collection")
class GetPoliciesForCollection(ClientCommand):
    """
    get_policies_for_collection
    """

    command = "get_policies_for_collection"
    method = "get"
    path = "/policy-collections/{name}/policies"
    params = {"--name": {}}


@PolicyCollections.commands.register("update-policies-for-collection")
class UpdatePoliciesForCollection(ClientCommand):
    """
    update_policies_for_collection
    """

    command = "update_policies_for_collection"
    method = "put"
    path = "/policy-collections/{name}/policies"
    params = {"--json": {}, "--name": {}}


@PolicyCollections.commands.register("add-policies-to-collection")
class AddPoliciesToCollection(ClientCommand):
    """
    add_policies_to_collection
    """

    command = "add_policies_to_collection"
    method = "post"
    path = "/policy-collections/{name}/policies"
    params = {"--json": {}, "--name": {}}


@PolicyCollections.commands.register("remove-policies-from-collection")
class RemovePoliciesFromCollection(ClientCommand):
    """
    remove_policies_from_collection
    """

    command = "remove_policies_from_collection"
    method = "delete"
    path = "/policy-collections/{name}/policies"
    params = {"--name": {}, "--policy": {}}
