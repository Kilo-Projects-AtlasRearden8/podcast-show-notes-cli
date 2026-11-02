"""Markdown export for show notes."""

from __future__ import annotations

from .generator import ShowNotes


def to_markdown(notes: ShowNotes, recording_notes: str | None = None) -> str:
    lines: list[str] = []
    lines.append(f"# {notes.title}")
    lines.append("")
    lines.append("## Episode Description")
    lines.append("")
    lines.append(notes.description)
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(notes.summary)
    lines.append("")
    if notes.timestamps:
        lines.append("## Timestamps")
        lines.append("")
        for stamp in notes.timestamps:
            lines.append(f"- {stamp}")
        lines.append("")
    if notes.keywords:
        lines.append("## Keywords")
        lines.append("")
        lines.append(", ".join(notes.keywords))
        lines.append("")
    if recording_notes:
        lines.append("## Recording Notes (source)")
        lines.append("")
        lines.append("```")
        lines.append(recording_notes.strip())
        lines.append("```")
        lines.append("")
    lines.append("---")
    lines.append("Drafted with the Podcast Show Notes CLI by Asdale Dynamics, LLC.")
    return "\n".join(lines)
