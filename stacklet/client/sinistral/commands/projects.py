# This is a generated file, created by scripts/parse.py
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
    Get Projects
    """

    command = "get_projects"
    method = "get"
    path = "/projects"
    params = {}
    query_params = {}
    payload_params = {}


@Projects.commands.register("create-project")
class CreateProject(ClientCommand):
    """
    Create Project
    """

    command = "create_project"
    method = "post"
    path = "/projects"
    params = {}
    query_params = {}
    payload_params = {
        "schema": {
            "title": "AddProjectInput",
            "required": ["name"],
            "type": "object",
            "properties": {
                "name": {"title": "Name", "type": "string"},
                "collections": {
                    "title": "Collections",
                    "uniqueItems": True,
                    "type": "array",
                    "items": {"type": "string"},
                },
                "groups": {
                    "title": "Group",
                    "type": "object",
                    "properties": {
                        "read": {
                            "title": "Read",
                            "uniqueItems": True,
                            "type": "array",
                            "items": {"type": "string"},
                        }
                    },
                },
            },
        }
    }


@Projects.commands.register("get-project-by-name")
class GetProjectByName(ClientCommand):
    """
    Get Project By Name
    """

    command = "get_project_by_name"
    method = "get"
    path = "/projects/{name}"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}


@Projects.commands.register("update-project")
class UpdateProject(ClientCommand):
    """
    Update Project
    """

    command = "update_project"
    method = "put"
    path = "/projects/{name}"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {
        "schema": {
            "title": "UpdateProjectInput",
            "type": "object",
            "properties": {
                "collections": {
                    "title": "Collections",
                    "uniqueItems": True,
                    "type": "array",
                    "items": {"type": "string"},
                },
                "groups": {
                    "title": "Group",
                    "type": "object",
                    "properties": {
                        "read": {
                            "title": "Read",
                            "uniqueItems": True,
                            "type": "array",
                            "items": {"type": "string"},
                        }
                    },
                },
            },
        }
    }


@Projects.commands.register("delete-project")
class DeleteProject(ClientCommand):
    """
    Delete Project
    """

    command = "delete_project"
    method = "delete"
    path = "/projects/{name}"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}


@Projects.commands.register("get-collections-for-project")
class GetCollectionsForProject(ClientCommand):
    """
    Get Collections For Project
    """

    command = "get_collections_for_project"
    method = "get"
    path = "/projects/{name}/collections"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}


@Projects.commands.register("add-collections-to-project")
class AddCollectionsToProject(ClientCommand):
    """
    Add Collections To Project
    """

    command = "add_collections_to_project"
    method = "post"
    path = "/projects/{name}/collections"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {
        "schema": {
            "title": "AddCollectionsProjectInput",
            "required": ["collections"],
            "type": "object",
            "properties": {
                "collections": {
                    "title": "Collections",
                    "minItems": 1,
                    "uniqueItems": True,
                    "type": "array",
                    "items": {"type": "string"},
                }
            },
        }
    }


@Projects.commands.register("remove-collections-from-project")
class RemoveCollectionsFromProject(ClientCommand):
    """
    Remove Collections From Project
    """

    command = "remove_collections_from_project"
    method = "delete"
    path = "/projects/{name}/collections"
    params = {"--name": {"required": True}}
    query_params = {"--collection": {"required": True}}
    payload_params = {}


@Projects.commands.register("get-policies-for-project")
class GetPoliciesForProject(ClientCommand):
    """
    Get Policies For Project
    """

    command = "get_policies_for_project"
    method = "get"
    path = "/projects/{name}/policies"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}


@Projects.commands.register("add-groups-to-group-type")
class AddGroupsToGroupType(ClientCommand):
    """
    Add Groups To Group Type
    """

    command = "add_groups_to_group_type"
    method = "post"
    path = "/projects/{name}/groups/{group_type}"
    params = {"--name": {"required": True}, "--group_type": {"required": True}}
    query_params = {}
    payload_params = {
        "schema": {
            "title": "GroupNamesInput",
            "required": ["group_names"],
            "type": "object",
            "properties": {
                "group_names": {
                    "title": "Group Names",
                    "minItems": 1,
                    "uniqueItems": True,
                    "type": "array",
                    "items": {"type": "string"},
                }
            },
        }
    }


@Projects.commands.register("remove-groups-from-group-type")
class RemoveGroupsFromGroupType(ClientCommand):
    """
    Remove Groups From Group Type
    """

    command = "remove_groups_from_group_type"
    method = "delete"
    path = "/projects/{name}/groups/{group_type}"
    params = {"--name": {"required": True}, "--group_type": {"required": True}}
    query_params = {"--group_name": {"required": True}}
    payload_params = {}
