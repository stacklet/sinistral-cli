from stacklet.client.sinistral.client import client_registry, ClientCommand, Client
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("scans")
class Scans(Client):
    """
    Scans Client
    """

    commands = PluginRegistry("commands")


@Scans.commands.register("list")
class ListScans(ClientCommand):
    command = "list"
    method = "get"
    path = "/scans"
    params = {}


@Scans.commands.register("create")
class CreateScan(ClientCommand):
    command = "create"
    method = "get"
    path = "/scans"
    params = {
        "--project-name": {"required": True},
        "--results": {},
        "--status": {"required": True},
    }
