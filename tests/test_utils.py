import os

from unittest.mock import patch
from tempfile import NamedTemporaryFile

from stacklet.client.sinistral.utils import get_log_level, get_token
from stacklet.client.sinistral.context import StackletContext


def test_get_log_level():
    result = get_log_level(1)
    assert result == 40

    result = get_log_level(2)
    assert result == 30

    result = get_log_level(3)
    assert result == 20

    result = get_log_level(4)
    assert result == 10

    result = get_log_level(5)
    assert result == 0

    result = get_log_level(6)
    assert result == 0

    result = get_log_level(-1)
    assert result == 50


def test_get_token():
    temp = NamedTemporaryFile(delete=False)
    with open(temp.name, "w") as f:
        f.write("foo")
    with patch.object(StackletContext, "DEFAULT_CREDENTIALS", temp.name):
        token = get_token()
        assert token == "foo"
    os.unlink(temp.name)
