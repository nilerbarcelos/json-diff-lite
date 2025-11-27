"""Tests for the CLI."""

import json
import tempfile
from pathlib import Path

import pytest

from json_diff_lite.cli import main


class TestCLI:
    def test_no_differences(self, monkeypatch, capsys):
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "file1.json"
            file2 = Path(tmpdir) / "file2.json"

            data = {"name": "test", "value": 42}
            file1.write_text(json.dumps(data))
            file2.write_text(json.dumps(data))

            monkeypatch.setattr("sys.argv", ["json-diff-lite", str(file1), str(file2)])
            result = main()

            captured = capsys.readouterr()
            assert result == 0
            assert "No differences found" in captured.out

    def test_with_differences(self, monkeypatch, capsys):
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "file1.json"
            file2 = Path(tmpdir) / "file2.json"

            file1.write_text(json.dumps({"name": "old"}))
            file2.write_text(json.dumps({"name": "new"}))

            monkeypatch.setattr("sys.argv", ["json-diff-lite", str(file1), str(file2)])
            result = main()

            captured = capsys.readouterr()
            assert result == 1
            assert "~ name:" in captured.out
            assert "'old'" in captured.out
            assert "'new'" in captured.out

    def test_quiet_mode_no_diff(self, monkeypatch, capsys):
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "file1.json"
            file2 = Path(tmpdir) / "file2.json"

            data = {"name": "test"}
            file1.write_text(json.dumps(data))
            file2.write_text(json.dumps(data))

            monkeypatch.setattr("sys.argv", ["json-diff-lite", "-q", str(file1), str(file2)])
            result = main()

            captured = capsys.readouterr()
            assert result == 0
            assert captured.out == ""

    def test_quiet_mode_with_diff(self, monkeypatch, capsys):
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "file1.json"
            file2 = Path(tmpdir) / "file2.json"

            file1.write_text(json.dumps({"a": 1}))
            file2.write_text(json.dumps({"a": 2}))

            monkeypatch.setattr("sys.argv", ["json-diff-lite", "-q", str(file1), str(file2)])
            result = main()

            captured = capsys.readouterr()
            assert result == 1
            assert captured.out == ""

    def test_file_not_found(self, monkeypatch, capsys):
        monkeypatch.setattr("sys.argv", ["json-diff-lite", "nonexistent.json", "other.json"])
        result = main()

        captured = capsys.readouterr()
        assert result == 2
        assert "File not found" in captured.err

    def test_invalid_json(self, monkeypatch, capsys):
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "file1.json"
            file2 = Path(tmpdir) / "file2.json"

            file1.write_text("not valid json")
            file2.write_text("{}")

            monkeypatch.setattr("sys.argv", ["json-diff-lite", str(file1), str(file2)])
            result = main()

            captured = capsys.readouterr()
            assert result == 2
            assert "Invalid JSON" in captured.err

    def test_version(self, monkeypatch, capsys):
        monkeypatch.setattr("sys.argv", ["json-diff-lite", "-v"])
        result = main()

        captured = capsys.readouterr()
        assert result == 0
        assert "json-diff-lite" in captured.out
        assert "0." in captured.out  # Just check it's a version number
