from podcast_show_notes.export import to_markdown
from podcast_show_notes.generator import ShowNotes


def test_to_markdown_includes_all_sections():
    notes = ShowNotes(
        title="Bee Episode",
        summary="A summary about bees.",
        timestamps=["00:00 - Intro", "02:30 - Bees"],
        description="Learn about bees.",
        keywords=["bees", "nature"],
    )
    markdown = to_markdown(notes, recording_notes="the host talked about bees")
    assert "# Bee Episode" in markdown
    assert "## Episode Description" in markdown
    assert "Learn about bees." in markdown
    assert "## Summary" in markdown
    assert "A summary about bees." in markdown
    assert "## Timestamps" in markdown
    assert "- 00:00 - Intro" in markdown
    assert "- 02:30 - Bees" in markdown
    assert "## Keywords" in markdown
    assert "bees, nature" in markdown
    assert "## Recording Notes (source)" in markdown
    assert "the host talked about bees" in markdown
    assert "Asdale Dynamics, LLC" in markdown


def test_to_markdown_without_source_notes():
    notes = ShowNotes(
        title="Minimal",
        summary="S.",
        timestamps=["00:00 - Start"],
        description="D.",
        keywords=[],
    )
    markdown = to_markdown(notes)
    assert "Recording Notes" not in markdown
    assert "Asdale Dynamics, LLC" in markdown


def test_parse_draft_multi_line_section_content():
    from podcast_show_notes.generator import parse_draft

    draft = (
        "Episode Title: Multi Line\n"
        "Summary: First sentence.\n"
        "Second sentence continues here.\n"
        "Timestamps:\n"
        "00:00 - Start\n"
        "01:30 - Middle\n"
        "Episode Description: A description.\n"
        "Keywords: one, two, three\n"
    )
    notes = parse_draft(draft)
    assert notes.title == "Multi Line"
    assert "First sentence." in notes.summary
    assert "Second sentence continues here." in notes.summary
    assert "00:00 - Start" in notes.timestamps
    assert "01:30 - Middle" in notes.timestamps
    assert "A description." in notes.description
    assert notes.keywords == ["one", "two", "three"]
