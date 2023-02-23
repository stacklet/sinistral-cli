# This is a generated file, created by scripts/parse.py
from stacklet.client.sinistral.client import client_registry, ClientCommand, Client
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("group")
class Group(Client):
    """
    Group Client
    """

    commands = PluginRegistry("commands")


@Group.commands.register("admin-delete-group")
class AdminDeleteGroup(ClientCommand):
    """
    Admin Delete Group
    """

    command = "admin_delete_group"
    method = "delete"
    path = "/group/{name}"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}
