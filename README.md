# Podcast Show Notes CLI

A friendly, local-first Python CLI that turns your podcast recording notes into
clean show notes and an episode description. It talks to a local
OpenAI-compatible endpoint (Ollama by default) — no API keys, no cloud, nothing
leaves your machine unless you point it elsewhere.

Made with care by **Asdale Dynamics, LLC** (Indiana, formed October 2026), the
LLC behind Dylan Asdale's beginner-friendly AI books and guides
(dylanasdale.github.io). Dylan is a registered nurse turned AI author who writes
AI explainers "like a friend would": plain English, step by step, never
condescending. This tool is built in that same spirit.

## What it does

Give it a file of rough recording notes (or paste them in), and it drafts:

- A catchy but clear episode title
- A short, warm summary (2–4 sentences)
- A timestamped outline of key moments (MM:SS — topic)
- An episode description ready for podcast directories
- A short list of keywords/tags

Then it writes everything out as a Markdown file you can paste into your show
notes, your podcast host, or your blog.

## Install

```bash
pip install .
```

That installs the `podcast-show-notes` command. You can also run it without
installing:

```bash
python -m podcast_show_notes ...
```

## Use it, step by step

### 1. Write down your recording notes

Save whatever you scribbled during recording to a plain text file, for example
`recording-notes.txt`:

```
The host welcomed listeners and talked about starting a summer garden.
We covered soil preparation, picking easy vegetables, and a watering
schedule that won't overwhelm a beginner. Listener question about tomatoes
at the end.
```

### 2. Draft the show notes

Run the CLI, pointing it at your notes file and asking for a Markdown output:

```bash
podcast-show-notes recording-notes.txt -o show-notes.md
```

If you'd rather see the result right in the terminal, leave off `-o`:

```bash
podcast-show-notes recording-notes.txt
```

### 3. Use a different local model or endpoint (optional)

By default the CLI talks to Ollama at `http://localhost:11434/v1/chat/completions`
using the `llama3.2` model. If you're running LM Studio, llama.cpp, or another
OpenAI-compatible server, point the CLI at it:

```bash
podcast-show-notes recording-notes.txt \
  --endpoint http://localhost:1234/v1/chat/completions \
  --model mistral-7b-instruct \
  -o show-notes.md
```

You can also set the endpoint and model once with environment variables:

```bash
export PODCAST_NOTES_ENDPOINT=http://localhost:11434/v1/chat/completions
export PODCAST_NOTES_MODEL=llama3.2
podcast-show-notes recording-notes.txt -o show-notes.md
```

## What the output looks like

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

## Recording Notes (source)

```
The host welcomed listeners and talked about starting a summer garden.
We covered soil preparation, picking easy vegetables, and a watering
schedule that won't overwhelm a beginner. Listener question about tomatoes
at the end.
```

---
Drafted with the Podcast Show Notes CLI by Asdale Dynamics, LLC.
```

## Test it

The test suite mocks the LLM endpoint, so you don't need a running model or any
network access:

```bash
pytest
```

All tests run offline.

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.
