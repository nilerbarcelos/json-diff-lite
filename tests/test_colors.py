"""Tests for color formatting."""

from json_diff_lite.colors import Colors, colorize, format_change


class TestColorize:
    def test_colorize_green(self, monkeypatch):
        # Force color support
        monkeypatch.setattr("json_diff_lite.colors.supports_color", lambda: True)
        result = colorize("text", Colors.GREEN)
        assert result == f"{Colors.GREEN}text{Colors.RESET}"

    def test_colorize_red(self, monkeypatch):
        monkeypatch.setattr("json_diff_lite.colors.supports_color", lambda: True)
        result = colorize("text", Colors.RED)
        assert result == f"{Colors.RED}text{Colors.RESET}"

    def test_colorize_no_support(self, monkeypatch):
        monkeypatch.setattr("json_diff_lite.colors.supports_color", lambda: False)
        result = colorize("text", Colors.GREEN)
        assert result == "text"


class TestFormatChange:
    def test_addition_colored(self, monkeypatch):
        monkeypatch.setattr("json_diff_lite.colors.supports_color", lambda: True)
        result = format_change("+ key: 'value'", use_color=True)
        assert Colors.GREEN in result
        assert "+ key: 'value'" in result

    def test_removal_colored(self, monkeypatch):
        monkeypatch.setattr("json_diff_lite.colors.supports_color", lambda: True)
        result = format_change("- key: 'value'", use_color=True)
        assert Colors.RED in result
        assert "- key: 'value'" in result

    def test_modification_colored(self, monkeypatch):
        monkeypatch.setattr("json_diff_lite.colors.supports_color", lambda: True)
        result = format_change("~ key: 'old' -> 'new'", use_color=True)
        assert Colors.YELLOW in result
        assert "~ key: 'old' -> 'new'" in result

    def test_no_color_flag(self, monkeypatch):
        monkeypatch.setattr("json_diff_lite.colors.supports_color", lambda: True)
        result = format_change("+ key: 'value'", use_color=False)
        assert Colors.GREEN not in result
        assert result == "+ key: 'value'"

    def test_unknown_prefix(self, monkeypatch):
        monkeypatch.setattr("json_diff_lite.colors.supports_color", lambda: True)
        result = format_change("? something", use_color=True)
        assert result == "? something"
