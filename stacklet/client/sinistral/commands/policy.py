from stacklet.client.sinistral.client import client_registry, ClientCommand, Client
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("policies")
class Policy(Client):
    """
    Policy Client
    """

    commands = PluginRegistry("commands")


@Policy.commands.register("list")
class ListPolicy(ClientCommand):
    command = "list"
    method = "get"
    path = "/policies"
    params = {}
