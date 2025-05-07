# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
# This is a generated file, created by scripts/parse.py
from stacklet.client.sinistral.client import Client, ClientCommand, client_registry
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("policy")
class Policy(Client):
    """
    Policy Client
    """

    commands = PluginRegistry("commands")


@Policy.commands.register("list")
class List(ClientCommand):
    """
    List all policies
    """

    command = "list"
    method = "get"
    path = "/policies"
    params = {}
    query_params = {
        "--search": {"required": False},
        "--lastKey": {"required": False},
        "--pageSize": {"required": False},
    }
    payload_params = {}


@Policy.commands.register("get")
class Get(ClientCommand):
    """
    Get a policy by name
    """

    command = "get"
    method = "get"
    path = "/policies/{name}"
    params = {"--name": {"required": True}}
    query_params = {}
    payload_params = {}
