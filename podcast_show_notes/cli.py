"""Command-line interface for drafting podcast show notes."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from .client import LLMClient, LLMError
from .config import Config
from .export import to_markdown
from .generator import draft_show_notes


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="podcast-show-notes",
        description="Draft podcast show notes and an episode description from recording notes.",
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="Path to a file with recording notes. Reads from stdin if omitted.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Write the Markdown show notes to this file instead of stdout.",
    )
    parser.add_argument(
        "--endpoint",
        default=None,
        help="OpenAI-compatible chat completions endpoint (default: localhost Ollama).",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model name to use (default: llama3.2).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=None,
        help="Request timeout in seconds (default: 120).",
    )
    return parser


def read_notes(input_path: str | None) -> str:
    if input_path:
        with open(input_path, "r", encoding="utf-8") as handle:
            return handle.read()
    return sys.stdin.read()


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        notes_text = read_notes(args.input)
    except OSError as exc:
        print(f"error: could not read input: {exc}", file=sys.stderr)
        return 1

    config = Config.from_env()
    if args.endpoint is not None:
        config.endpoint = args.endpoint
    if args.model is not None:
        config.model = args.model
    if args.timeout is not None:
        config.timeout_seconds = args.timeout

    client = LLMClient(
        endpoint=config.endpoint,
        model=config.model,
        timeout_seconds=config.timeout_seconds,
    )

    try:
        show_notes = draft_show_notes(client, notes_text)
    except LLMError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    markdown = to_markdown(show_notes, recording_notes=notes_text)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as handle:
                handle.write(markdown)
        except OSError as exc:
            print(f"error: could not write output: {exc}", file=sys.stderr)
            return 1
    else:
        sys.stdout.write(markdown)
        sys.stdout.write("\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
