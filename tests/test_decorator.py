"""Tests for @annotate decorator."""
import time
import pytest
from agent_metadata import Annotated, Metadata, annotate


# ── Basic wrapping ────────────────────────────────────────────────────────────

def test_decorator_wraps_plain_value():
    @annotate()
    def fn():
        return "hello"

    result = fn()
    assert isinstance(result, Annotated)
    assert result.value == "hello"


def test_decorator_adds_latency():
    @annotate()
    def fn():
        return "x"

    result = fn()
    assert result.metadata.get("latency_ms") is not None
    assert result.metadata.get("latency_ms") >= 0


def test_decorator_adds_model_tag():
    @annotate(model="gpt-4")
    def fn():
        return "response"

    result = fn()
    assert result.metadata.get("model") == "gpt-4"


def test_decorator_no_model_no_model_key():
    @annotate()
    def fn():
        return "x"

    result = fn()
    assert result.metadata.get("model") is None


def test_decorator_merges_existing_annotated():
    @annotate(model="gpt-4")
    def fn():
        return Annotated("data", Metadata(confidence=0.95, tokens=512))

    result = fn()
    assert isinstance(result, Annotated)
    assert result.value == "data"
    assert result.metadata.get("model") == "gpt-4"
    assert result.metadata.get("confidence") == 0.95
    assert result.metadata.get("tokens") == 512
    assert result.metadata.get("latency_ms") is not None


def test_decorator_preserves_fn_name():
    @annotate()
    def my_llm_call():
        return "output"

    assert my_llm_call.__name__ == "my_llm_call"


def test_decorator_passes_args():
    @annotate(model="claude-3")
    def greet(name: str):
        return f"Hello, {name}!"

    result = greet("Darshan")
    assert result.value == "Hello, Darshan!"
    assert result.metadata.get("model") == "claude-3"


def test_decorator_track_cost_flag_no_error():
    """track_cost=True must not raise even though it's currently a no-op."""
    @annotate(model="x", track_cost=True)
    def fn():
        return "ok"

    result = fn()
    assert result.value == "ok"


def test_decorator_latency_reasonably_fast():
    @annotate()
    def fast():
        return "fast"

    result = fast()
    # Should complete in < 500ms
    assert result.metadata.get("latency_ms") < 500


def test_decorator_latency_captures_real_duration():
    @annotate()
    def slow():
        time.sleep(0.05)
        return "slow"

    result = slow()
    assert result.metadata.get("latency_ms") >= 40  # at least 40ms
