"""@annotate decorator — auto-captures latency and model tag."""

from __future__ import annotations
import functools
import time
from typing import Any, Callable

from .metadata import Metadata
from .annotated import Annotated


def annotate(
    model: str | None = None,
    track_cost: bool = False,
) -> Callable:
    """Decorator factory that captures latency_ms and optionally model tag.

    The wrapped function's return value:
    - If already an Annotated, its metadata is merged with latency/model.
    - Otherwise the return value is wrapped in a new Annotated.

    Args:
        model: Model name to tag on the output.
        track_cost: Reserved for future automatic cost tracking (no-op now).
    """

    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Annotated:
            start = time.perf_counter()
            result = fn(*args, **kwargs)
            elapsed_ms = (time.perf_counter() - start) * 1000

            extra: dict[str, Any] = {"latency_ms": elapsed_ms}
            if model is not None:
                extra["model"] = model

            if isinstance(result, Annotated):
                return result.annotate(**extra)
            else:
                return Annotated(result, Metadata(**extra))

        return wrapper

    return decorator
