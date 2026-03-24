"""Tests for MetadataStore class."""
import pytest
from agent_metadata import Annotated, Metadata, MetadataStore


def make_item(model="gpt-4", confidence=0.9, cost=0.005, value="result"):
    m = Metadata(model=model, confidence=confidence, cost_usd=cost)
    return Annotated(value, m)


# ── Basic CRUD ────────────────────────────────────────────────────────────────

def test_store_empty():
    s = MetadataStore()
    assert s.count == 0


def test_store_and_get():
    s = MetadataStore()
    item = make_item()
    s.store("k1", item)
    assert s.get("k1") is item


def test_store_count_increments():
    s = MetadataStore()
    s.store("a", make_item())
    s.store("b", make_item())
    assert s.count == 2


def test_store_get_missing_returns_none():
    s = MetadataStore()
    assert s.get("nonexistent") is None


def test_store_contains():
    s = MetadataStore()
    s.store("x", make_item())
    assert "x" in s
    assert "y" not in s


def test_store_overwrite():
    s = MetadataStore()
    a = make_item(model="old")
    b = make_item(model="new")
    s.store("k", a)
    s.store("k", b)
    assert s.get("k").metadata.get("model") == "new"
    assert s.count == 1


def test_store_type_error_on_non_annotated():
    s = MetadataStore()
    with pytest.raises(TypeError):
        s.store("k", "not an Annotated")


# ── Query ─────────────────────────────────────────────────────────────────────

def test_query_no_filters():
    s = MetadataStore()
    s.store("a", make_item(model="gpt-4"))
    s.store("b", make_item(model="claude-3"))
    assert len(s.query()) == 2


def test_query_by_model():
    s = MetadataStore()
    s.store("a", make_item(model="gpt-4"))
    s.store("b", make_item(model="claude-3"))
    results = s.query(model="gpt-4")
    assert len(results) == 1
    assert results[0].metadata.get("model") == "gpt-4"


def test_query_by_min_confidence():
    s = MetadataStore()
    s.store("high", make_item(confidence=0.95))
    s.store("low", make_item(confidence=0.4))
    results = s.query(min_confidence=0.8)
    assert len(results) == 1
    assert results[0].metadata.get("confidence") == 0.95


def test_query_by_max_cost():
    s = MetadataStore()
    s.store("cheap", make_item(cost=0.001))
    s.store("expensive", make_item(cost=0.1))
    results = s.query(max_cost=0.01)
    assert len(results) == 1
    assert results[0].metadata.get("cost_usd") == 0.001


def test_query_combined_filters():
    s = MetadataStore()
    s.store("match", make_item(model="gpt-4", confidence=0.9, cost=0.002))
    s.store("wrong_model", make_item(model="claude-3", confidence=0.9, cost=0.002))
    s.store("low_conf", make_item(model="gpt-4", confidence=0.5, cost=0.002))
    s.store("high_cost", make_item(model="gpt-4", confidence=0.9, cost=0.5))
    results = s.query(model="gpt-4", min_confidence=0.8, max_cost=0.01)
    assert len(results) == 1


def test_query_missing_field_excluded():
    """Items lacking the filtered field should be excluded."""
    s = MetadataStore()
    item_no_conf = Annotated("x", Metadata(model="gpt-4"))  # no confidence
    s.store("no_conf", item_no_conf)
    results = s.query(min_confidence=0.5)
    assert len(results) == 0
