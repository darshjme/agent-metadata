"""MetadataStore — in-memory store with filtering/querying."""

from __future__ import annotations
from typing import Any

from .annotated import Annotated


class MetadataStore:
    """Thread-compatible in-memory store for Annotated outputs."""

    def __init__(self) -> None:
        self._store: dict[str, Annotated] = {}

    # ------------------------------------------------------------------ #
    # CRUD                                                                 #
    # ------------------------------------------------------------------ #

    def store(self, key: str, annotated: Annotated) -> None:
        """Store an Annotated output under *key*."""
        if not isinstance(annotated, Annotated):
            raise TypeError(f"Expected Annotated, got {type(annotated).__name__}")
        self._store[key] = annotated

    def get(self, key: str) -> Annotated | None:
        """Retrieve by key, or None if not found."""
        return self._store.get(key)

    # ------------------------------------------------------------------ #
    # Query                                                                #
    # ------------------------------------------------------------------ #

    def query(
        self,
        model: str | None = None,
        min_confidence: float | None = None,
        max_cost: float | None = None,
    ) -> list[Annotated]:
        """Return all Annotated items matching the given filters (AND logic)."""
        results: list[Annotated] = []
        for item in self._store.values():
            meta = item.metadata

            if model is not None and meta.get("model") != model:
                continue

            if min_confidence is not None:
                conf = meta.get("confidence")
                if conf is None or conf < min_confidence:
                    continue

            if max_cost is not None:
                cost = meta.get("cost_usd")
                if cost is None or cost > max_cost:
                    continue

            results.append(item)
        return results

    # ------------------------------------------------------------------ #
    # Properties                                                           #
    # ------------------------------------------------------------------ #

    @property
    def count(self) -> int:
        """Number of stored items."""
        return len(self._store)

    # ------------------------------------------------------------------ #
    # Dunder helpers                                                       #
    # ------------------------------------------------------------------ #

    def __repr__(self) -> str:  # pragma: no cover
        return f"MetadataStore(count={self.count})"

    def __contains__(self, key: str) -> bool:
        return key in self._store
