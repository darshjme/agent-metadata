"""Tests for Annotated class."""
import pytest
from agent_metadata import Annotated, Metadata


# ── Construction ──────────────────────────────────────────────────────────────

def test_annotated_stores_value():
    a = Annotated("hello")
    assert a.value == "hello"


def test_annotated_default_metadata_is_empty():
    a = Annotated(42)
    assert isinstance(a.metadata, Metadata)
    assert len(a.metadata) == 0


def test_annotated_custom_metadata():
    m = Metadata(model="gpt-4", tokens=100)
    a = Annotated("result", m)
    assert a.metadata.get("model") == "gpt-4"


def test_annotated_none_value():
    a = Annotated(None)
    assert a.value is None


def test_annotated_complex_value():
    data = {"key": [1, 2, 3]}
    a = Annotated(data)
    assert a.value == data


# ── annotate() ────────────────────────────────────────────────────────────────

def test_annotated_annotate_returns_new():
    a = Annotated("x", Metadata(model="old"))
    b = a.annotate(confidence=0.9)
    assert b is not a


def test_annotated_annotate_merges_metadata():
    a = Annotated("x", Metadata(model="gpt-4"))
    b = a.annotate(confidence=0.95, tokens=512)
    assert b.metadata.get("model") == "gpt-4"
    assert b.metadata.get("confidence") == 0.95
    assert b.metadata.get("tokens") == 512


def test_annotated_annotate_preserves_value():
    a = Annotated("original")
    b = a.annotate(model="gemini")
    assert b.value == "original"


def test_annotated_annotate_chain():
    a = Annotated("data")
    result = a.annotate(model="x").annotate(tokens=10).annotate(confidence=0.8)
    assert result.metadata.get("model") == "x"
    assert result.metadata.get("tokens") == 10
    assert result.metadata.get("confidence") == 0.8


# ── to_dict ───────────────────────────────────────────────────────────────────

def test_annotated_to_dict_structure():
    m = Metadata(model="claude-3", cost_usd=0.001)
    a = Annotated("answer", m)
    d = a.to_dict()
    assert "value" in d
    assert "metadata" in d
    assert d["value"] == "answer"
    assert d["metadata"]["model"] == "claude-3"


def test_annotated_to_dict_empty_metadata():
    a = Annotated(99)
    d = a.to_dict()
    assert d["value"] == 99
    assert d["metadata"] == {}


# ── equality ──────────────────────────────────────────────────────────────────

def test_annotated_equality():
    m = Metadata(model="x")
    a = Annotated("v", m)
    b = Annotated("v", Metadata(model="x"))
    assert a == b


def test_annotated_inequality_value():
    a = Annotated("x")
    b = Annotated("y")
    assert a != b


def test_annotated_eq_non_annotated():
    a = Annotated("x")
    assert a.__eq__("not annotated") is NotImplemented
