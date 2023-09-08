# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
# This is a generated file, created by scripts/parse.py
from stacklet.client.sinistral.client import client_registry, ClientCommand, Client
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("org")
class Org(Client):
    """
    Org Client
    """

    commands = PluginRegistry("commands")


@Org.commands.register("get-client-id")
class GetClientId(ClientCommand):
    """
    Get the the Org Client ID for use with the Org auth flow (admin only).
    """

    command = "get-client-id"
    method = "get"
    path = "/org/credentials"
    params = {}
    query_params = {}
    payload_params = {}


@Org.commands.register("regenerate-credentials")
class RegenCreds(ClientCommand):
    """
    Regenerate the Org credentials for use with the Org
    auth flow, and return the credentials.
    """

    command = "regenerate_credentials"
    method = "post"
    path = "/org/credentials"
    params = {}
    query_params = {}
    payload_params = {}
