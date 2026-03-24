# Contributing

Thank you for your interest in contributing to `agent-metadata`!

## Development Setup

```bash
git clone https://github.com/example/agent-metadata
cd agent-metadata
pip install -e ".[dev]"
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Guidelines

- **Zero dependencies** — keep `dependencies = []` in `pyproject.toml`.
- **Python ≥ 3.10** — use modern type hints (`X | Y`, `match`, etc.).
- **Tests first** — every public API change needs corresponding tests.
- **Type annotations** — all public functions must be fully annotated.
- **Docstrings** — module, class, and public method level.
- **Backwards compatibility** — do not remove or rename public APIs without a deprecation period.

## Pull Request Process

1. Fork, branch (`feat/my-feature` or `fix/my-bug`), commit.
2. Ensure `pytest` passes with 0 failures.
3. Update `CHANGELOG.md` under `[Unreleased]`.
4. Open a PR with a clear description of the change and motivation.

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
