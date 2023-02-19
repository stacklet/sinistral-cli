from stacklet.client.sinistral.client import client_registry, ClientCommand, Client
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("PolicySources")
class PolicySources(Client):
    """
    PolicySources Client
    """

    commands = PluginRegistry("commands")


@PolicySources.commands.register("get-policy-sources")
class GetPolicySources(ClientCommand):
    """
    get_policy_sources
    """

    command = "get_policy_sources"
    method = "get"
    path = "/policy-sources"
    params = {}


@PolicySources.commands.register("create-policy-source")
class CreatePolicySource(ClientCommand):
    """
    create_policy_source
    """

    command = "create_policy_source"
    method = "post"
    path = "/policy-sources"
    params = {"--json": {}}


@PolicySources.commands.register("get-policy-source-by-name")
class GetPolicySourceByName(ClientCommand):
    """
    get_policy_source_by_name
    """

    command = "get_policy_source_by_name"
    method = "get"
    path = "/policy-sources/{name}"
    params = {"--name": {}}


@PolicySources.commands.register("delete-policy-source-by-name")
class DeletePolicySourceByName(ClientCommand):
    """
    delete_policy_source_by_name
    """

    command = "delete_policy_source_by_name"
    method = "delete"
    path = "/policy-sources/{name}"
    params = {"--name": {}}


@PolicySources.commands.register("update-policy-source")
class UpdatePolicySource(ClientCommand):
    """
    update_policy_source
    """

    command = "update_policy_source"
    method = "patch"
    path = "/policy-sources/{name}"
    params = {"--json": {}, "--name": {}}


@PolicySources.commands.register("get-policies-for-source")
class GetPoliciesForSource(ClientCommand):
    """
    get_policies_for_source
    """

    command = "get_policies_for_source"
    method = "get"
    path = "/policy-sources/{name}/policies"
    params = {"--name": {}}


@PolicySources.commands.register("scan-policy-source")
class ScanPolicySource(ClientCommand):
    """
    scan_policy_source
    """

    command = "scan_policy_source"
    method = "post"
    path = "/policy-sources/{name}/scans"
    params = {"--name": {}}
