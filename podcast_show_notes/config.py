"""Configuration for the podcast show notes generator."""

from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_ENDPOINT = "http://localhost:11434/v1/chat/completions"
DEFAULT_MODEL = "llama3.2"
DEFAULT_TIMEOUT_SECONDS = 120


@dataclass
class Config:
    endpoint: str
    model: str
    timeout_seconds: int

    @classmethod
    def from_env(cls) -> Config:
        return cls(
            endpoint=os.environ.get("PODCAST_NOTES_ENDPOINT", DEFAULT_ENDPOINT),
            model=os.environ.get("PODCAST_NOTES_MODEL", DEFAULT_MODEL),
            timeout_seconds=int(
                os.environ.get("PODCAST_NOTES_TIMEOUT", str(DEFAULT_TIMEOUT_SECONDS))
            ),
        )
