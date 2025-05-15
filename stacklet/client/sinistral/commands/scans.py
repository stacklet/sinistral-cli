# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
# This is a generated file, created by scripts/parse.py
from stacklet.client.sinistral.client import Client, ClientCommand, client_registry
from stacklet.client.sinistral.registry import PluginRegistry


@client_registry.register("scans")
class Scans(Client):
    """
    Scans Client
    """

    commands = PluginRegistry("commands")


@Scans.commands.register("list")
class List(ClientCommand):
    """
    List all scans
    """

    command = "list"
    method = "get"
    path = "/scans"
    params = {}
    query_params = {
        "--start": {"required": False},
        "--end": {"required": False},
        "--trigger": {"required": False},
        "--status": {"required": False},
        "--search": {"required": False},
        "--lastKey": {"required": False},
        "--pageSize": {"required": False},
        "--sort": {"required": False},
    }
    payload_params = {}


@Scans.commands.register("create")
class Create(ClientCommand):
    """
    Create a scan
    """

    command = "create"
    method = "post"
    path = "/scans"
    params = {}
    query_params = {}
    payload_params = {
        "schema": {
            "title": "ScanInput",
            "required": ["project_name", "status"],
            "type": "object",
            "properties": {
                "project_name": {
                    "title": "Project Name",
                    "minLength": 1,
                    "type": "string",
                },
                "results": {
                    "title": "Results",
                    "type": "array",
                    "items": {
                        "title": "ScanResultInput",
                        "required": [
                            "policy",
                            "resource",
                            "file_path",
                            "file_line_start",
                            "file_line_end",
                            "code_block",
                        ],
                        "type": "object",
                        "properties": {
                            "policy": {
                                "title": "ScanResultPolicy",
                                "required": [
                                    "name",
                                    "resource",
                                    "description",
                                    "filters",
                                    "mode",
                                ],
                                "type": "object",
                                "properties": {
                                    "name": {"title": "Name", "type": "string"},
                                    "resource": {
                                        "title": "Resource",
                                        "anyOf": [
                                            {"type": "string"},
                                            {
                                                "type": "array",
                                                "items": {"type": "string"},
                                            },
                                        ],
                                    },
                                    "description": {
                                        "title": "Description",
                                        "type": "string",
                                    },
                                    "metadata": {
                                        "title": "ScanResultPolicyMetadata",
                                        "type": "object",
                                        "properties": {
                                            "severity": {
                                                "title": "Severity",
                                                "type": "string",
                                                "description": "Severity of a policy violation.",
                                                "pattern": "(?i)^(critical|high|medium|low|unknown)$",  # noqa: E501
                                            }
                                        },
                                    },
                                    "filters": {
                                        "title": "Filters",
                                        "type": "array",
                                        "items": {},
                                    },
                                    "mode": {
                                        "title": "Mode",
                                        "type": "object",
                                        "additionalProperties": {"type": "string"},
                                    },
                                },
                            },
                            "resource": {
                                "title": "ScanResultResource",
                                "required": ["id", "__tfmeta"],
                                "type": "object",
                                "properties": {
                                    "id": {"title": "Id", "type": "string"},
                                    "name": {"title": "Name", "type": "string"},
                                    "__tfmeta": {
                                        "title": "ScanResultResourceTfMeta",
                                        "required": [
                                            "filename",
                                            "label",
                                            "line_end",
                                            "line_start",
                                            "path",
                                            "type",
                                            "src_dir",
                                        ],
                                        "type": "object",
                                        "properties": {
                                            "filename": {
                                                "title": "Filename",
                                                "type": "string",
                                            },
                                            "label": {
                                                "title": "Label",
                                                "type": "string",
                                            },
                                            "line_end": {
                                                "title": "Line End",
                                                "type": "integer",
                                            },
                                            "line_start": {
                                                "title": "Line Start",
                                                "type": "integer",
                                            },
                                            "path": {"title": "Path", "type": "string"},
                                            "type": {"title": "Type", "type": "string"},
                                            "src_dir": {
                                                "title": "Src Dir",
                                                "type": "string",
                                            },
                                        },
                                    },
                                    "c7n:MatchedFilters": {
                                        "title": "C7N:Matchedfilters",
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                },
                            },
                            "file_path": {"title": "File Path", "type": "string"},
                            "file_line_start": {
                                "title": "File Line Start",
                                "type": "integer",
                            },
                            "file_line_end": {
                                "title": "File Line End",
                                "type": "integer",
                            },
                            "code_block": {
                                "title": "Code Block",
                                "type": "array",
                                "items": {
                                    "type": "array",
                                    "items": {
                                        "anyOf": [
                                            {"type": "integer"},
                                            {"type": "string"},
                                        ]
                                    },
                                },
                            },
                        },
                    },
                    "default": [],
                },
                "status": {
                    "title": "ScanStatus",
                    "enum": ["PASSED", "FAILED", "ERROR"],
                    "type": "string",
                    "description": "An enumeration.",
                },
                "ci_info": {
                    "oneOf": [
                        {"type": "null"},
                        {
                            "type": "object",
                            "properties": {
                                "service": {
                                    "title": "Service",
                                    "type": "string",
                                },
                                "build_url": {
                                    "title": "BuildUrl",
                                    "type": "string",
                                },
                                "build_code": {
                                    "title": "BuildCode",
                                    "type": "string",
                                },
                                "job_code": {
                                    "title": "JobCode",
                                    "type": "string",
                                },
                                "pull_request_number": {
                                    "title": "PRNumber",
                                    "type": "string",
                                },
                                "branch": {
                                    "title": "Branch",
                                    "type": "string",
                                },
                                "commit_sha": {
                                    "title": "CommitSHA",
                                    "type": "string",
                                },
                                "repo": {
                                    "title": "Repo",
                                    "type": "string",
                                },
                                "repo_url": {
                                    "title": "RepoUrl",
                                    "type": "string",
                                },
                            },
                        },
                    ],
                },
            },
        }
    }


@Scans.commands.register("get")
class Get(ClientCommand):
    """
    Get a scan by id
    """

    command = "get"
    method = "get"
    path = "/scans/{id}"
    params = {"--id": {"required": True}}
    query_params = {}
    payload_params = {}


@Scans.commands.register("get-results")
class GetResults(ClientCommand):
    """
    Get scan results by scan id
    """

    command = "get_results"
    method = "get"
    path = "/scans/{id}/results"
    params = {"--id": {"required": True}}
    query_params = {}
    payload_params = {}
