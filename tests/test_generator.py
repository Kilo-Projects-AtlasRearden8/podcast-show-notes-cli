from podcast_show_notes.generator import (
    DEFAULT_SYSTEM_PROMPT,
    build_messages,
    draft_show_notes,
    parse_draft,
)


def test_build_messages_includes_system_and_user():
    messages = build_messages("the host talked about gardening for ten minutes")
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == DEFAULT_SYSTEM_PROMPT
    assert messages[1]["role"] == "user"
    assert "gardening" in messages[1]["content"]


def test_parse_draft_extracts_sections():
    draft = (
        "Episode Title: Garden Talk\n"
        "Summary: A chat about tomatoes.\n"
        "Timestamps:\n"
        "00:00 - Intro\n"
        "05:30 - Tomatoes\n"
        "Episode Description: Listen and learn.\n"
        "Keywords: gardening, tomatoes\n"
    )
    notes = parse_draft(draft)
    assert notes.title == "Garden Talk"
    assert "tomatoes" in notes.summary.lower()
    assert "00:00 - Intro" in notes.timestamps
    assert "Listen and learn" in notes.description
    assert "gardening" in notes.keywords


def test_parse_draft_handles_minimal_output():
    notes = parse_draft("Just some freeform thoughts about the episode.")
    assert notes.title == "Podcast Episode"
    assert notes.timestamps == ["00:00 - Episode start"]
    assert notes.description


def test_draft_show_notes_uses_client():
    class FakeClient:
        def chat(self, messages):
            class Response:
                content = (
                    "Episode Title: Mocked Episode\n"
                    "Summary: This was mocked.\n"
                    "Timestamps:\n00:00 - Start\n"
                    "Episode Description: A mocked episode.\n"
                    "Keywords: test\n"
                )

            return Response()

    notes = draft_show_notes(FakeClient(), "recording notes here")
    assert notes.title == "Mocked Episode"
    assert notes.description == "A mocked episode."
    assert notes.keywords == ["test"]
