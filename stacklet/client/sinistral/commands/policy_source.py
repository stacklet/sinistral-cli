from stacklet.client.sinistral.client import client_registry, ClientCommand, Client
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("policy-sources")
class PolicySources(Client):
    """
    Policy Sources Client
    """

    commands = PluginRegistry("commands")


@PolicySources.commands.register("list")
class ListPolicy(ClientCommand):
    command = "list"
    method = "get"
    path = "/policy-sources"
    params = {}
