# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
# This is a generated file, created by scripts/parse.py
from stacklet.client.sinistral.client import Client, ClientCommand, client_registry
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("org")
class Org(Client):
    """
    Org Client
    """

    commands = PluginRegistry("commands")


@Org.commands.register("get-credentials")
class GetCredentials(ClientCommand):
    """
    Get current Organization Credentials.
    """

    command = "get_credentials"
    method = "get"
    path = "/org/credentials"
    params = {}
    query_params = {}
    payload_params = {}


@Org.commands.register("regenerate-credentials")
class RegenerateCredentials(ClientCommand):
    """
    Create or regenerate and return Organization Credentials.
    """

    command = "regenerate_credentials"
    method = "post"
    path = "/org/credentials"
    params = {}
    query_params = {}
    payload_params = {}


@Org.commands.register("revoke-credentials")
class RevokeCredentials(ClientCommand):
    """
    Revoke existing Organization Credentials.
    """

    command = "revoke_credentials"
    method = "delete"
    path = "/org/credentials"
    params = {}
    query_params = {}
    payload_params = {}
