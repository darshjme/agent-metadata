# Changelog

All notable changes to `agent-metadata` are documented here.

## [0.1.0] — 2024-03-24

### Added
- `Metadata` — key-value metadata container with built-in fields (`model`, `cost_usd`, `tokens`, `latency_ms`, `confidence`, `timestamp`).
- `Annotated` — wraps any Python value with a `Metadata` object for full provenance tracking.
- `MetadataStore` — in-memory store with `query()` filtering by model, confidence, and cost.
- `@annotate` decorator — auto-captures `latency_ms` and optionally tags `model` on function return values.
- Zero-dependency design (Python ≥ 3.10 only).
- 22 pytest tests with full coverage of all public APIs.
