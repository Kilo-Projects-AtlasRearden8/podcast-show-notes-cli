# Podcast Show Notes CLI

A local-first Python CLI that drafts podcast show notes and episode descriptions
from your recording notes, using a configurable OpenAI-compatible endpoint
(default: Ollama on `localhost:11434`). No API keys, no cloud required — your
recording notes never leave your machine unless you point the endpoint
elsewhere.

Built and maintained by **Asdale Dynamics, LLC** (Indiana, formed October 2026),
the LLC behind Dylan Asdale's beginner-friendly AI books, guides, and practical
tools (dylanasdale.github.io).

## What it does

- Takes recording notes (from a file or stdin) and drafts:
  - an episode title,
  - a short summary,
  - a timestamped outline,
  - an episode description for podcast directories,
  - keywords/tags.
- Exports the result as Markdown to a file or stdout.
- Works with any OpenAI-compatible chat completions endpoint (Ollama, LM Studio,
  local llama.cpp servers, etc.) via `--endpoint` and `--model`, or the
  `PODCAST_NOTES_ENDPOINT` / `PODCAST_NOTES_MODEL` environment variables.

## Install

```bash
pip install .
```

or, to run without installing:

```bash
python -m podcast_show_notes.cli ...
```

## Usage

Draft from a recording-notes file and save Markdown:

```bash
podcast-show-notes recording-notes.txt -o show-notes.md
```

Read from stdin:

```bash
cat recording-notes.txt | podcast-show-notes > show-notes.md
```

Point at a different local endpoint:

```bash
podcast-show-notes recording-notes.txt \
  --endpoint http://localhost:1234/v1/chat/completions \
  --model mistral-7b-instruct \
  -o show-notes.md
```

Or with environment variables:

```bash
export PODCAST_NOTES_ENDPOINT=http://localhost:11434/v1/chat/completions
export PODCAST_NOTES_MODEL=llama3.2
podcast-show-notes recording-notes.txt -o show-notes.md
```

## Example output

`show-notes.md`:

```markdown
# Summer Garden Tips

## Episode Description

A friendly walk-through of beginner vegetable gardening, from soil to harvest.

## Summary

The host walks listeners through starting a summer garden, covering soil prep,
planting, watering, and common beginner mistakes in plain English.

## Timestamps

- 00:00 - Introduction
- 03:15 - Soil preparation
- 08:40 - Planting basics
- 14:20 - Watering schedule

## Keywords

gardening, vegetables, beginner

---

Drafted with the Podcast Show Notes CLI by Asdale Dynamics, LLC.
```

## Tests

```bash
pytest
```

Tests mock the LLM endpoint, so no running model or network access is needed.

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.
