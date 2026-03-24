"""Metadata container for agent outputs."""

from __future__ import annotations
from datetime import datetime, timezone
from typing import Any


# Built-in field names
BUILTIN_FIELDS = {"model", "cost_usd", "tokens", "latency_ms", "confidence", "timestamp"}


class Metadata:
    """Key-value metadata container with built-in fields for agent provenance."""

    def __init__(self, **kwargs: Any) -> None:
        self._data: dict[str, Any] = {}
        for key, value in kwargs.items():
            self._data[key] = value

    # ------------------------------------------------------------------ #
    # Core API                                                             #
    # ------------------------------------------------------------------ #

    def set(self, key: str, value: Any) -> "Metadata":
        """Set a metadata field. Returns self for fluent chaining."""
        self._data[key] = value
        return self

    def get(self, key: str, default: Any = None) -> Any:
        """Get a metadata field value, or *default* if not present."""
        return self._data.get(key, default)

    def merge(self, other: "Metadata") -> "Metadata":
        """Return a new Metadata with fields from both (other wins on conflict)."""
        merged = dict(self._data)
        merged.update(other._data)
        return Metadata(**merged)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dict."""
        return dict(self._data)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Metadata":
        """Deserialize from a plain dict."""
        return cls(**data)

    # ------------------------------------------------------------------ #
    # Convenience accessors for built-in fields                           #
    # ------------------------------------------------------------------ #

    @property
    def model(self) -> str | None:
        return self._data.get("model")

    @property
    def cost_usd(self) -> float | None:
        return self._data.get("cost_usd")

    @property
    def tokens(self) -> int | None:
        return self._data.get("tokens")

    @property
    def latency_ms(self) -> float | None:
        return self._data.get("latency_ms")

    @property
    def confidence(self) -> float | None:
        return self._data.get("confidence")

    @property
    def timestamp(self) -> str | None:
        return self._data.get("timestamp")

    # ------------------------------------------------------------------ #
    # Dunder helpers                                                       #
    # ------------------------------------------------------------------ #

    def __repr__(self) -> str:  # pragma: no cover
        return f"Metadata({self._data!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Metadata):
            return NotImplemented
        return self._data == other._data

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __len__(self) -> int:
        return len(self._data)
