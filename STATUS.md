# STATUS

## What was built

A local-first Python CLI, `podcast-show-notes`, that drafts podcast show notes and episode
descriptions from recording notes.

- `podcast_show_notes/cli.py` — argparse CLI: input file (or stdin), optional Markdown output
  file, configurable `--endpoint`, `--model`, `--timeout`.
- `podcast_show_notes/config.py` — configuration from environment variables with sensible
  defaults: endpoint `http://localhost:11434/v1/chat/completions` (Ollama), model `llama3.2`,
  timeout 120s.
- `podcast_show_notes/client.py` — standard-library (urllib) OpenAI-compatible chat client;
  no external runtime dependencies, no API keys.
- `podcast_show_notes/generator.py` — builds the producer-style prompt, calls the client, and
  parses the free-form draft into title, summary, timestamps, description, keywords.
- `podcast_show_notes/export.py` — Markdown export including source recording notes.
- `tests/` — 12 tests, all mocking the LLM endpoint (no network, no model required).
- `pyproject.toml` — project metadata, console-script entry point, pytest dev dependency.
- `LICENSE` — MIT, copyright line exactly `Copyright (c) 2026 Asdale Dynamics, LLC`.
- `README.md` — usage, credits Asdale Dynamics, LLC.
- `STATUS.md` — this file.

Credits Asdale Dynamics, LLC (Indiana, formed Oct 2026) in the README and LICENSE, per the
project style (plain English, beginner-friendly, local-first, no secrets).

## How to run

Install:

```bash
pip install .
```

Draft from a recording-notes file:

```bash
podcast-show-notes recording-notes.txt -o show-notes.md
```

Read from stdin:

```bash
cat recording-notes.txt | podcast-show-notes > show-notes.md
```

Use a different local endpoint (Ollama, LM Studio, llama.cpp, etc.):

```bash
podcast-show-notes recording-notes.txt \
  --endpoint http://localhost:11434/v1/chat/completions \
  --model llama3.2 \
  -o show-notes.md
```

Or via environment variables:

```bash
export PODCAST_NOTES_ENDPOINT=http://localhost:11434/v1/chat/completions
export PODCAST_NOTES_MODEL=llama3.2
podcast-show-notes recording-notes.txt -o show-notes.md
```

Run tests (fully offline, endpoint mocked):

```bash
pytest
```

## Verification results

- `pytest`: 12 passed (client, generator, CLI, package import) — all endpoint calls mocked.
- `ruff check`: clean.
- `ruff format --check`: clean.
- `python3 -m py_compile`: all modules compile.
- `python3 -m podcast_show_notes.cli --help`: works.
- End-to-end smoke test against a fake local OpenAI-compatible HTTP server: produced correct
  Markdown (title, description, summary, timestamps, keywords, source notes, credit line),
  exit code 0.
- No Ollama instance was available in this environment, so the default Ollama endpoint was not
  exercised live; the client was verified against a fake server speaking the same protocol.

## Known gaps

- Live Ollama/default-endpoint run not verified in this environment (no Ollama server
  available). Point `--endpoint` at your local Ollama `http://localhost:11434/v1/chat/completions`
  and ensure the model (default `llama3.2`) is pulled (`ollama pull llama3.2`).
- `parse_draft` is best-effort: free-form LLM output that omits labeled sections falls back to
  defaults instead of failing.
- No packaging/publishing, no CI workflows, no remote repository (by design).
- Python >= 3.9.
