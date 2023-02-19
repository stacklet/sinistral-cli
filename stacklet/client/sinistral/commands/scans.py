from stacklet.client.sinistral.client import client_registry, ClientCommand, Client
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("scans")
class Scans(Client):
    """
    Scans Client
    """

    commands = PluginRegistry("commands")


@Scans.commands.register("get-scans")
class GetScans(ClientCommand):
    """
    get_scans
    """

    command = "get_scans"
    method = "get"
    path = "/scans"
    params = {
        "--start": {},
        "--end": {},
        "--trigger": {},
        "--status": {},
        "--search": {},
        "--lastKey": {},
        "--pageSize": {},
        "--sort": {},
    }


@Scans.commands.register("create-scan")
class CreateScan(ClientCommand):
    """
    create_scan
    """

    command = "create_scan"
    method = "post"
    path = "/scans"
    params = {"--json": {}}


@Scans.commands.register("get-scan")
class GetScan(ClientCommand):
    """
    get_scan
    """

    command = "get_scan"
    method = "get"
    path = "/scans/{id}"
    params = {"--id": {}}


@Scans.commands.register("get-scan-results")
class GetScanResults(ClientCommand):
    """
    get_scan_results
    """

    command = "get_scan_results"
    method = "get"
    path = "/scans/{id}/results"
    params = {"--id": {}}
