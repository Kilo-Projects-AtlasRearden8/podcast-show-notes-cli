"""Show notes and episode description generation."""

from __future__ import annotations

from dataclasses import dataclass

from .client import ChatMessage


@dataclass
class ShowNotes:
    title: str
    summary: str
    timestamps: list[str]
    description: str
    keywords: list[str]


DEFAULT_SYSTEM_PROMPT = (
    "You are a warm, practical podcast producer. Draft clear, beginner-friendly "
    "show notes and an episode description from the recording notes below. "
    "Never sound condescending. Write plain English, step by step where helpful. "
    "Do not invent facts not present in the notes."
)


SECTION_HEADERS = {
    "title": ("episode title", "title:"),
    "summary": ("summary",),
    "timestamps": ("timestamp", "key moment", "timestamps"),
    "description": ("description", "episode description"),
    "keywords": ("keyword", "tag"),
}


def build_messages(
    recording_notes: str, system_prompt: str = DEFAULT_SYSTEM_PROMPT
) -> list[dict[str, str]]:
    user_prompt = (
        "Recording notes:\n---\n" + recording_notes.strip() + "\n---\n\n"
        "Produce:\n"
        "1. A catchy but clear episode title.\n"
        "2. A short summary (2-4 sentences).\n"
        "3. A timestamped outline of key moments (format: MM:SS - topic).\n"
        "4. An episode description suitable for podcast directories (2-3 sentences).\n"
        "5. A short list of keywords/tags.\n"
        "Return only the drafted content, labeled clearly."
    )
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def _detect_section(line: str) -> str | None:
    lowered = line.lower()
    for section, keys in SECTION_HEADERS.items():
        if any(key in lowered for key in keys):
            return section
    return None


def _append_section(section: str, value: str, parts: dict[str, list[str]]) -> None:
    if section == "keywords":
        for part in value.replace(",", " ").split():
            if part and part not in parts["keywords"]:
                parts["keywords"].append(part)
    else:
        parts[section].append(value)


def parse_draft(draft: str) -> ShowNotes:
    """Best-effort parse of the LLM draft into structured show notes.

    The LLM is free-form, so this extracts what it can and sensibly defaults
    the rest instead of failing.
    """
    lines = draft.splitlines()
    title = ""
    parts: dict[str, list[str]] = {
        "summary": [],
        "timestamps": [],
        "description": [],
        "keywords": [],
    }
    section: str | None = None

    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        detected = _detect_section(line)
        if detected is not None:
            section = detected
            if ":" in line:
                value = line.split(":", 1)[1].strip()
                if value:
                    if section == "title":
                        if not title:
                            title = value
                    else:
                        _append_section(section, value, parts)
            continue

        if section == "title" and not title:
            title = line.strip("* ")
        elif section:
            _append_section(section, line, parts)

    if not title:
        title = "Podcast Episode"
    summary = " ".join(parts["summary"]).strip()
    description = " ".join(parts["description"]).strip()
    if not summary:
        summary = lines[0].strip() if draft else ""
    if not description:
        description = summary
    if not parts["timestamps"]:
        parts["timestamps"] = ["00:00 - Episode start"]

    return ShowNotes(
        title=title,
        summary=summary,
        timestamps=list(parts["timestamps"]),
        description=description,
        keywords=list(parts["keywords"]),
    )


def draft_show_notes(
    client, recording_notes: str, system_prompt: str = DEFAULT_SYSTEM_PROMPT
) -> ShowNotes:
    """Call the LLM client and parse the result into ShowNotes."""
    messages = build_messages(recording_notes, system_prompt)
    chat_messages = [
        ChatMessage(role=m["role"], content=m["content"]) for m in messages
    ]
    response = client.chat(chat_messages)
    return parse_draft(response.content)
