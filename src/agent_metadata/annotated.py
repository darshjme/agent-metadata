"""Annotated wrapper — a value paired with its Metadata."""

from __future__ import annotations
from typing import Any

from .metadata import Metadata


class Annotated:
    """Wraps any value with a Metadata object for full provenance tracking."""

    def __init__(self, value: Any, metadata: Metadata | None = None) -> None:
        self._value = value
        self._metadata = metadata if metadata is not None else Metadata()

    # ------------------------------------------------------------------ #
    # Properties                                                           #
    # ------------------------------------------------------------------ #

    @property
    def value(self) -> Any:
        """The wrapped value."""
        return self._value

    @property
    def metadata(self) -> Metadata:
        """The associated Metadata object."""
        return self._metadata

    # ------------------------------------------------------------------ #
    # Core API                                                             #
    # ------------------------------------------------------------------ #

    def annotate(self, **kwargs: Any) -> "Annotated":
        """Return a new Annotated with extra metadata merged in."""
        extra = Metadata(**kwargs)
        merged = self._metadata.merge(extra)
        return Annotated(self._value, merged)

    def to_dict(self) -> dict[str, Any]:
        """Serialize value and metadata to a plain dict."""
        return {
            "value": self._value,
            "metadata": self._metadata.to_dict(),
        }

    # ------------------------------------------------------------------ #
    # Dunder helpers                                                       #
    # ------------------------------------------------------------------ #

    def __repr__(self) -> str:  # pragma: no cover
        return f"Annotated(value={self._value!r}, metadata={self._metadata!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Annotated):
            return NotImplemented
        return self._value == other._value and self._metadata == other._metadata
