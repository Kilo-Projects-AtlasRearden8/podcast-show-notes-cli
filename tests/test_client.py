import json
from unittest.mock import patch

import pytest

from podcast_show_notes.client import ChatMessage, LLMClient, LLMError


def _fake_response(payload, status=200, reason="OK"):
    class FakeResponse:
        def __init__(self):
            self.status = status
            self.reason = reason

        def read(self):
            return json.dumps(payload).encode("utf-8")

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    return FakeResponse()


def test_chat_posts_openai_payload_and_returns_content():
    captured = {}

    def fake_request(req, timeout=None):
        captured["url"] = req.full_url
        captured["method"] = req.method
        captured["headers"] = dict(req.header_items())
        captured["body"] = json.loads(req.data)
        return _fake_response(
            {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "Here are your show notes.",
                        }
                    }
                ]
            }
        )

    client = LLMClient(
        endpoint="http://localhost:11434/v1/chat/completions",
        model="llama3.2",
        timeout_seconds=30,
        request=fake_request,
    )
    response = client.chat([ChatMessage(role="user", content="draft notes for me")])

    assert response.content == "Here are your show notes."
    assert captured["method"] == "POST"
    assert any(key.lower() == "content-type" for key in captured["headers"])
    assert captured["body"]["model"] == "llama3.2"
    assert captured["body"]["stream"] is False
    assert captured["body"]["messages"][0] == {
        "role": "user",
        "content": "draft notes for me",
    }


def test_chat_raises_on_connection_error():
    def boom(req, timeout=None):
        raise OSError("connection refused")

    client = LLMClient(
        endpoint="http://localhost:11434/v1/chat/completions",
        model="llama3.2",
        timeout_seconds=5,
        request=boom,
    )
    with pytest.raises(LLMError, match="could not reach LLM endpoint"):
        client.chat([ChatMessage(role="user", content="hi")])


def test_chat_raises_on_invalid_json():
    class RawResponse:
        def read(self):
            return b"not json {"

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    def bad_json(req, timeout=None):
        return RawResponse()

    client = LLMClient(
        endpoint="http://localhost:11434/v1/chat/completions",
        model="llama3.2",
        timeout_seconds=5,
        request=bad_json,
    )
    with pytest.raises(LLMError, match="invalid JSON"):
        client.chat([ChatMessage(role="user", content="hi")])


def test_chat_raises_on_unexpected_shape():
    def weird_shape(req, timeout=None):
        return _fake_response({"choices": []})

    client = LLMClient(
        endpoint="http://localhost:11434/v1/chat/completions",
        model="llama3.2",
        timeout_seconds=5,
        request=weird_shape,
    )
    with pytest.raises(LLMError, match="unexpected response shape"):
        client.chat([ChatMessage(role="user", content="hi")])


@patch("podcast_show_notes.client.urllib.request.urlopen")
def test_chat_uses_urllib_by_default(mock_urlopen):
    mock_urlopen.return_value = _fake_response(
        {"choices": [{"message": {"content": "ok"}}]}
    )
    client = LLMClient(
        endpoint="http://localhost:11434/v1/chat/completions",
        model="llama3.2",
        timeout_seconds=5,
    )
    assert client.chat([ChatMessage(role="user", content="hi")]).content == "ok"
    mock_urlopen.assert_called_once()
    _args, kwargs = mock_urlopen.call_args
    assert kwargs.get("timeout") == 5
