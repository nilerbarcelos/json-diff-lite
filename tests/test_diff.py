"""Tests for json_diff_lite."""

import pytest
from json_diff_lite import diff


class TestPrimitives:
    def test_string_modification(self):
        result = diff({"name": "Ana"}, {"name": "Ana Maria"})
        assert result == ["~ name: 'Ana' -> 'Ana Maria'"]

    def test_number_modification(self):
        result = diff({"age": 30}, {"age": 31})
        assert result == ["~ age: 30 -> 31"]

    def test_boolean_modification(self):
        result = diff({"active": True}, {"active": False})
        assert result == ["~ active: True -> False"]

    def test_null_modification(self):
        result = diff({"value": None}, {"value": "something"})
        assert result == ["~ value: None -> 'something'"]


class TestDictOperations:
    def test_key_addition(self):
        result = diff({"name": "Ana"}, {"name": "Ana", "age": 31})
        assert result == ["+ age: 31"]

    def test_key_removal(self):
        result = diff({"name": "Ana", "nickname": "Aninha"}, {"name": "Ana"})
        assert result == ["- nickname: 'Aninha'"]

    def test_no_changes(self):
        obj = {"name": "Ana", "age": 30}
        result = diff(obj, obj.copy())
        assert result == []


class TestNestedDicts:
    def test_nested_modification(self):
        a = {"address": {"street": "Rua A", "number": 100}}
        b = {"address": {"street": "Rua B", "number": 100}}
        result = diff(a, b)
        assert result == ["~ address.street: 'Rua A' -> 'Rua B'"]

    def test_nested_addition(self):
        a = {"address": {"street": "Rua A"}}
        b = {"address": {"street": "Rua A", "city": "SP"}}
        result = diff(a, b)
        assert result == ["+ address.city: 'SP'"]

    def test_deep_nesting(self):
        a = {"level1": {"level2": {"level3": "old"}}}
        b = {"level1": {"level2": {"level3": "new"}}}
        result = diff(a, b)
        assert result == ["~ level1.level2.level3: 'old' -> 'new'"]


class TestLists:
    def test_list_item_modification(self):
        result = diff({"items": [1, 2, 3]}, {"items": [1, 2, 4]})
        assert result == ["~ items[2]: 3 -> 4"]

    def test_list_item_addition(self):
        result = diff({"items": [1, 2]}, {"items": [1, 2, 3]})
        assert result == ["+ items[2]: 3"]

    def test_list_item_removal(self):
        result = diff({"items": [1, 2, 3]}, {"items": [1, 2]})
        assert result == ["- items[2]: 3"]

    def test_empty_list_to_filled(self):
        result = diff({"items": []}, {"items": [1]})
        assert result == ["+ items[0]: 1"]


class TestTypeChanges:
    def test_dict_to_list(self):
        result = diff({"data": {"a": 1}}, {"data": [1, 2]})
        assert result == ["~ data: {'a': 1} -> [1, 2]"]

    def test_string_to_number(self):
        result = diff({"value": "42"}, {"value": 42})
        assert result == ["~ value: '42' -> 42"]


class TestComplexScenarios:
    def test_multiple_changes(self):
        a = {"name": "Ana", "age": 30, "city": "SP"}
        b = {"name": "Ana Maria", "age": 31}
        result = diff(a, b)
        assert "~ age: 30 -> 31" in result
        assert "- city: 'SP'" in result
        assert "~ name: 'Ana' -> 'Ana Maria'" in result

    def test_nested_list_in_dict(self):
        a = {"users": [{"name": "Ana"}]}
        b = {"users": [{"name": "Bob"}]}
        result = diff(a, b)
        assert result == ["~ users[0].name: 'Ana' -> 'Bob'"]
