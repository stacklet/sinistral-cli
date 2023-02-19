from stacklet.client.sinistral.client import client_registry, ClientCommand, Client
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("Group")
class Group(Client):
    """
    Group Client
    """

    commands = PluginRegistry("commands")


@Group.commands.register("admin-delete-group")
class AdminDeleteGroup(ClientCommand):
    """
    admin_delete_group
    """

    command = "admin_delete_group"
    method = "delete"
    path = "/group/{name}"
    params = {"--name": {}}
