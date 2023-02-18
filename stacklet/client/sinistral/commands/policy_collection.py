from stacklet.client.sinistral.client import client_registry, ClientCommand, Client
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("policy-collections")
class PolicyCollection(Client):
    """
    Policy Collection Client
    """

    commands = PluginRegistry("commands")


@PolicyCollection.commands.register("list")
class ListPolicyCollection(ClientCommand):
    command = "list"
    method = "get"
    path = "/policy-collections"
    params = {}


@PolicyCollection.commands.register("get")
class GetPolicyCollection(ClientCommand):
    command = "get"
    method = "get"
    path = "/policy-collections/{name}"
    params = {"--name": {"required": True}}


@PolicyCollection.commands.register("get-policies")
class GetPoliciesPolicyCollection(ClientCommand):
    command = "get_policies"
    method = "get"
    path = "/policy-collections/{name}/policies"
    params = {"--name": {"required": True}}
