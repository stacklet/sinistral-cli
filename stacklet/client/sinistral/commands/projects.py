from stacklet.client.sinistral.client import client_registry, ClientCommand, Client
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("projects")
class Projects(Client):
    """
    Projects Client
    """

    commands = PluginRegistry("commands")


@Projects.commands.register("get-projects")
class GetProjects(ClientCommand):
    """
    get_projects
    """

    command = "get_projects"
    method = "get"
    path = "/projects"
    params = {}


@Projects.commands.register("create-project")
class CreateProject(ClientCommand):
    """
    create_project
    """

    command = "create_project"
    method = "post"
    path = "/projects"
    params = {"--json": {}}


@Projects.commands.register("get-project-by-name")
class GetProjectByName(ClientCommand):
    """
    get_project_by_name
    """

    command = "get_project_by_name"
    method = "get"
    path = "/projects/{name}"
    params = {"--name": {}}


@Projects.commands.register("update-project")
class UpdateProject(ClientCommand):
    """
    update_project
    """

    command = "update_project"
    method = "put"
    path = "/projects/{name}"
    params = {"--json": {}, "--name": {}}


@Projects.commands.register("delete-project")
class DeleteProject(ClientCommand):
    """
    delete_project
    """

    command = "delete_project"
    method = "delete"
    path = "/projects/{name}"
    params = {"--name": {}}


@Projects.commands.register("get-collections-for-project")
class GetCollectionsForProject(ClientCommand):
    """
    get_collections_for_project
    """

    command = "get_collections_for_project"
    method = "get"
    path = "/projects/{name}/collections"
    params = {"--name": {}}


@Projects.commands.register("add-collections-to-project")
class AddCollectionsToProject(ClientCommand):
    """
    add_collections_to_project
    """

    command = "add_collections_to_project"
    method = "post"
    path = "/projects/{name}/collections"
    params = {"--json": {}, "--name": {}}


@Projects.commands.register("remove-collections-from-project")
class RemoveCollectionsFromProject(ClientCommand):
    """
    remove_collections_from_project
    """

    command = "remove_collections_from_project"
    method = "delete"
    path = "/projects/{name}/collections"
    params = {"--name": {}, "--collection": {}}


@Projects.commands.register("get-policies-for-project")
class GetPoliciesForProject(ClientCommand):
    """
    get_policies_for_project
    """

    command = "get_policies_for_project"
    method = "get"
    path = "/projects/{name}/policies"
    params = {"--name": {}}


@Projects.commands.register("add-groups-to-group-type")
class AddGroupsToGroupType(ClientCommand):
    """
    add_groups_to_group_type
    """

    command = "add_groups_to_group_type"
    method = "post"
    path = "/projects/{name}/groups/{group_type}"
    params = {"--json": {}, "--name": {}, "--group_type": {}}


@Projects.commands.register("remove-groups-from-group-type")
class RemoveGroupsFromGroupType(ClientCommand):
    """
    remove_groups_from_group_type
    """

    command = "remove_groups_from_group_type"
    method = "delete"
    path = "/projects/{name}/groups/{group_type}"
    params = {"--name": {}, "--group_type": {}, "--group_name": {}}
