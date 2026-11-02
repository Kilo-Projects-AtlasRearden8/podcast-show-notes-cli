"""HTTP client for an OpenAI-compatible chat completions endpoint."""

from __future__ import annotations

import json
import urllib.request
from collections.abc import Iterable
from dataclasses import dataclass


@dataclass
class ChatMessage:
    role: str
    content: str


@dataclass
class ChatResponse:
    content: str


class LLMError(RuntimeError):
    """Raised when the LLM endpoint returns an error or invalid response."""


class LLMClient:
    """Small OpenAI-compatible chat client built on the standard library."""

    def __init__(
        self,
        endpoint: str,
        model: str,
        timeout_seconds: int,
        request=None,
    ) -> None:
        self.endpoint = endpoint
        self.model = model
        self.timeout_seconds = timeout_seconds
        self._request = request if request is not None else urllib.request.urlopen

    def chat(self, messages: Iterable[ChatMessage]) -> ChatResponse:
        payload = {
            "model": self.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": False,
            "temperature": 0.7,
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )
        try:
            with self._request(req, timeout=self.timeout_seconds) as response:
                body = response.read()
        except OSError as exc:
            raise LLMError(
                f"could not reach LLM endpoint {self.endpoint}: {exc}"
            ) from exc

        try:
            parsed = json.loads(body)
        except json.JSONDecodeError as exc:
            raise LLMError(f"invalid JSON from LLM endpoint: {exc}") from exc

        try:
            content = parsed["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMError(
                f"unexpected response shape from LLM endpoint: {exc}"
            ) from exc

        return ChatResponse(content=str(content))
