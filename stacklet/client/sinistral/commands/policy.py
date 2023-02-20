from stacklet.client.sinistral.client import client_registry, ClientCommand, Client
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("policy")
class Policy(Client):
    """
    Policy Client
    """

    commands = PluginRegistry("commands")


@Policy.commands.register("get-policies")
class GetPolicies(ClientCommand):
    """
    Get Policies
    """

    command = "get_policies"
    method = "get"
    path = "/policies"
    params = {}
    query_params = {
        "--search": {"required": False},
        "--lastKey": {"required": False},
        "--pageSize": {"required": False},
    }
    payload_params = {}


@Policy.commands.register("get-policy-by-name")
class GetPolicyByName(ClientCommand):
    """
    Get Policy By Name
    """

    command = "get_policy_by_name"
    method = "get"
    path = "/policies/{name}"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}
