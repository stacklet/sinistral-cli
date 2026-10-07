# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
import json
import pathlib
import subprocess
import sys


TERRAFORM_DIR = pathlib.Path(__file__).parent.resolve() / "terraform" / "good"


def run_dump(*args, cwd=None):
    # Run in a fresh interpreter: c7n-left registers its IaC providers via
    # import side effects, so in-process tests could pass only because an
    # earlier test happened to register them.
    return subprocess.run(
        [
            sys.executable,
            "-c",
            "from stacklet.client.sinistral.cli import cli; cli()",
            "dump",
            *args,
        ],
        check=False,
        capture_output=True,
        text=True,
        cwd=cwd,
    )


def test_dump_directory():
    result = run_dump("-d", str(TERRAFORM_DIR))
    assert result.returncode == 0, result.stderr
    assert "aws_sqs_queue" in json.loads(result.stdout)["graph"]


def test_dump_defaults_to_current_directory():
    result = run_dump(cwd=TERRAFORM_DIR)
    assert result.returncode == 0, result.stderr
    assert "aws_sqs_queue" in json.loads(result.stdout)["graph"]


def test_dump_without_iac_files(tmp_path):
    result = run_dump("-d", str(tmp_path))
    assert result.returncode != 0
    assert "No supported IaC files found" in result.stderr + result.stdout
