# Copyright Stacklet, Inc.
# SPDX-License-Identifier: Apache-2.0
import importlib.util

from pathlib import Path

import pytest
import tomlkit

from click.testing import CliRunner


SCRIPT = Path(__file__).parent.parent / "scripts" / "upgrade.py"


@pytest.fixture
def upgrade_cli():
    spec = importlib.util.spec_from_file_location("upgrade", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.cli


def write_pyproject(path, version):
    (path / "pyproject.toml").write_text(f'[project]\nversion = "{version}"\n')


def read_version(path):
    return tomlkit.loads((path / "pyproject.toml").read_text())["project"]["version"]


@pytest.mark.parametrize(
    "current,flag,expected",
    [
        ("0.5.39", "--bump-patch", "0.5.40"),
        ("0.5.39", "--bump-minor", "0.6.0"),
        ("0.5.39", "--bump-major", "1.0.0"),
        ("0.5.39.1", "--bump-patch", "0.5.40"),
        ("0.5.39.1", "--bump-minor", "0.6.0"),
        ("0.5.39.1", "--bump-major", "1.0.0"),
    ],
)
def test_upgrade_bumps_version(upgrade_cli, tmp_path, monkeypatch, current, flag, expected):
    write_pyproject(tmp_path, current)
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(upgrade_cli, ["upgrade", flag])

    assert result.exit_code == 0, result.output
    assert f"{current} -> {expected}" in result.output
    assert read_version(tmp_path) == expected


@pytest.mark.parametrize("flags", [[], ["--bump-patch", "--bump-minor"]])
def test_upgrade_requires_exactly_one_flag(upgrade_cli, tmp_path, monkeypatch, flags):
    write_pyproject(tmp_path, "0.5.39")
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(upgrade_cli, ["upgrade", *flags])

    assert result.exit_code == 1
    assert "Only one of --bump-patch/minor/major may be selected" in result.output
    assert read_version(tmp_path) == "0.5.39"
