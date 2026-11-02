from podcast_show_notes.cli import main


def _run(args, stdin_text=""):
    import sys
    from io import StringIO

    old_stdin, old_stdout = sys.stdin, sys.stdout
    sys.stdin = StringIO(stdin_text)
    sys.stdout = StringIO()
    try:
        code = main(args)
        output = sys.stdout.getvalue()
    finally:
        sys.stdin, sys.stdout = old_stdin, old_stdout
    return code, output


def test_cli_reads_from_stdin_and_writes_stdout(monkeypatch):
    class FakeClient:
        def chat(self, messages):
            class Response:
                content = (
                    "Episode Title: CLI Test\n"
                    "Summary: A summary.\n"
                    "Timestamps:\n00:00 - Start\n"
                    "Episode Description: A description.\n"
                    "Keywords: cli, test\n"
                )

            return Response()

    monkeypatch.setattr(
        "podcast_show_notes.cli.LLMClient",
        lambda *a, **k: FakeClient(),
    )

    code, output = _run([], stdin_text="the host talked about bees")
    assert code == 0
    assert "# CLI Test" in output
    assert "A description." in output
    assert "cli, test" in output
    assert "Asdale Dynamics, LLC" in output


def test_cli_writes_to_output_file(monkeypatch, tmp_path):
    class FakeClient:
        def chat(self, messages):
            class Response:
                content = (
                    "Episode Title: File Output\n"
                    "Summary: Summary text.\n"
                    "Timestamps:\n00:00 - Start\n"
                    "Episode Description: Desc text.\n"
                    "Keywords: one\n"
                )

            return Response()

    monkeypatch.setattr(
        "podcast_show_notes.cli.LLMClient",
        lambda *a, **k: FakeClient(),
    )

    out_file = tmp_path / "notes.md"
    code, _output = _run(
        [
            "--output",
            str(out_file),
            "--endpoint",
            "http://example.com/v1/chat/completions",
            "--model",
            "test-model",
        ],
        stdin_text="input notes",
    )
    assert code == 0
    content = out_file.read_text(encoding="utf-8")
    assert "# File Output" in content
    assert "Desc text." in content


def test_cli_reads_from_input_file(monkeypatch, tmp_path):
    class FakeClient:
        def chat(self, messages):
            class Response:
                content = (
                    "Episode Title: From File\n"
                    "Summary: S.\n"
                    "Timestamps:\n00:00 - Start\n"
                    "Episode Description: D.\n"
                    "Keywords: x\n"
                )

            return Response()

    monkeypatch.setattr(
        "podcast_show_notes.cli.LLMClient",
        lambda *a, **k: FakeClient(),
    )

    in_file = tmp_path / "recording.txt"
    in_file.write_text("notes from the field", encoding="utf-8")
    code, output = _run([str(in_file)])
    assert code == 0
    assert "# From File" in output
