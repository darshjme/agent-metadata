"""Tests for Metadata class."""
import pytest
from agent_metadata import Metadata


# ── Construction ──────────────────────────────────────────────────────────────

def test_metadata_empty():
    m = Metadata()
    assert m.to_dict() == {}
    assert len(m) == 0


def test_metadata_kwargs():
    m = Metadata(model="gpt-4", cost_usd=0.002, tokens=512)
    assert m.model == "gpt-4"
    assert m.cost_usd == 0.002
    assert m.tokens == 512


def test_metadata_builtin_properties_none():
    m = Metadata()
    assert m.model is None
    assert m.cost_usd is None
    assert m.tokens is None
    assert m.latency_ms is None
    assert m.confidence is None
    assert m.timestamp is None


# ── set / get ─────────────────────────────────────────────────────────────────

def test_metadata_set_fluent():
    m = Metadata()
    result = m.set("model", "claude-3").set("tokens", 100)
    assert result is m  # fluent returns self
    assert m.get("model") == "claude-3"
    assert m.get("tokens") == 100


def test_metadata_get_default():
    m = Metadata()
    assert m.get("nonexistent") is None
    assert m.get("nonexistent", "fallback") == "fallback"


def test_metadata_get_existing():
    m = Metadata(confidence=0.95)
    assert m.get("confidence") == 0.95


def test_metadata_contains():
    m = Metadata(model="llama-3")
    assert "model" in m
    assert "cost_usd" not in m


# ── merge ─────────────────────────────────────────────────────────────────────

def test_metadata_merge_returns_new():
    a = Metadata(model="gpt-4")
    b = Metadata(tokens=256)
    c = a.merge(b)
    assert c is not a
    assert c is not b


def test_metadata_merge_combines_fields():
    a = Metadata(model="gpt-4", cost_usd=0.01)
    b = Metadata(tokens=256, confidence=0.9)
    c = a.merge(b)
    assert c.get("model") == "gpt-4"
    assert c.get("cost_usd") == 0.01
    assert c.get("tokens") == 256
    assert c.get("confidence") == 0.9


def test_metadata_merge_other_wins_on_conflict():
    a = Metadata(model="gpt-4")
    b = Metadata(model="claude-3")
    c = a.merge(b)
    assert c.get("model") == "claude-3"


def test_metadata_merge_originals_unchanged():
    a = Metadata(model="gpt-4")
    b = Metadata(model="claude-3")
    a.merge(b)
    assert a.get("model") == "gpt-4"  # a unchanged


# ── serialisation ─────────────────────────────────────────────────────────────

def test_metadata_to_dict():
    m = Metadata(model="gemini-pro", latency_ms=312.5)
    d = m.to_dict()
    assert d == {"model": "gemini-pro", "latency_ms": 312.5}


def test_metadata_from_dict():
    d = {"model": "llama-3", "confidence": 0.88}
    m = Metadata.from_dict(d)
    assert m.get("model") == "llama-3"
    assert m.get("confidence") == 0.88


def test_metadata_roundtrip():
    original = Metadata(model="gpt-4o", tokens=1024, cost_usd=0.005, confidence=0.97)
    restored = Metadata.from_dict(original.to_dict())
    assert original == restored


# ── equality ──────────────────────────────────────────────────────────────────

def test_metadata_equality():
    a = Metadata(model="x", tokens=10)
    b = Metadata(model="x", tokens=10)
    assert a == b


def test_metadata_inequality():
    a = Metadata(model="x")
    b = Metadata(model="y")
    assert a != b


def test_metadata_eq_non_metadata():
    m = Metadata(model="x")
    assert m.__eq__("not metadata") is NotImplemented
