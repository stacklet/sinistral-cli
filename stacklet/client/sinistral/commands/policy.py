from stacklet.client.sinistral.client import client_registry, ClientCommand, Client
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("Policy")
class Policy(Client):
    """
    Policy Client
    """

    commands = PluginRegistry("commands")


@Policy.commands.register("get-policies")
class GetPolicies(ClientCommand):
    """
    get_policies
    """

    command = "get_policies"
    method = "get"
    path = "/policies"
    params = {"--search": {}, "--lastKey": {}, "--pageSize": {}}


@Policy.commands.register("get-policy-by-name")
class GetPolicyByName(ClientCommand):
    """
    get_policy_by_name
    """

    command = "get_policy_by_name"
    method = "get"
    path = "/policies/{name}"
    params = {"--name": {}}
