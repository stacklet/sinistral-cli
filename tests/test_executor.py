from unittest.mock import MagicMock

from stacklet.client.sinistral.executor import RestExecutor


def test_executor_init():
    mock_context = MagicMock()
    mock_context.config.api = "https://api.sinistral.acme.org"
    executor = RestExecutor(mock_context, "foobarbaz")
    assert "Authorization" in executor.session.headers
    assert executor.session.headers["Authorization"] == "Bearer foobarbaz"


def test_executor_get():
    mock_context = MagicMock()
    mock_context.config.api = "https://api.sinistral.acme.org"
    mock_session = MagicMock()

    executor = RestExecutor(mock_context, "foobarbaz")
    executor.session = mock_session
    executor.get("/foo", params={"bar": "baz"}, json={})

    mock_session.get.assert_called_once()
    mock_session.get.assert_called_once_with(
        "https://api.sinistral.acme.org/foo", params={"bar": "baz"}
    )


def test_executor_post():
    mock_context = MagicMock()
    mock_context.config.api = "https://api.sinistral.acme.org"
    mock_session = MagicMock()

    executor = RestExecutor(mock_context, "foobarbaz")
    executor.session = mock_session
    executor.post("/foo", params={"bar": "baz"}, json={"a": "b"})

    mock_session.post.assert_called_once()
    mock_session.post.assert_called_once_with(
        "https://api.sinistral.acme.org/foo", params={"bar": "baz"}, json={"a": "b"}
    )


def test_executor_put():
    mock_context = MagicMock()
    mock_context.config.api = "https://api.sinistral.acme.org"
    mock_session = MagicMock()

    executor = RestExecutor(mock_context, "foobarbaz")
    executor.session = mock_session
    executor.put("/foo", params={"bar": "baz"}, json={"a": "b"})

    mock_session.put.assert_called_once()
    mock_session.put.assert_called_once_with(
        "https://api.sinistral.acme.org/foo", params={"bar": "baz"}, json={"a": "b"}
    )


def test_executor_delete():
    mock_context = MagicMock()
    mock_context.config.api = "https://api.sinistral.acme.org"
    mock_session = MagicMock()

    executor = RestExecutor(mock_context, "foobarbaz")
    executor.session = mock_session
    executor.delete("/foo", params={"bar": "baz"}, json={"a": "b"})

    mock_session.delete.assert_called_once()
    mock_session.delete.assert_called_once_with(
        "https://api.sinistral.acme.org/foo", params={"bar": "baz"}, json={"a": "b"}
    )
