from stacklet.client.sinistral.client import client_registry, ClientCommand, Client
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("projects")
class Projects(Client):
    """
    Projects Client
    """

    commands = PluginRegistry("commands")


@Projects.commands.register("list")
class ListProjects(ClientCommand):
    command = "list"
    method = "get"
    path = "/projects"
    params = {}


@Projects.commands.register("get")
class GetProject(ClientCommand):
    command = "get"
    method = "get"
    path = "/projects/{name}"
    params = {"--name": {"required": True}}
