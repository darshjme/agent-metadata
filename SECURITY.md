# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✅ Yes    |

## Reporting a Vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Instead, email the maintainers directly with:
- A description of the vulnerability
- Steps to reproduce
- Potential impact

We will acknowledge receipt within 48 hours and aim to release a fix within 7 days for critical issues.

## Scope

`agent-metadata` is a pure Python in-memory library with **zero external dependencies**. It does not:
- Make network requests
- Access the filesystem (beyond what you explicitly pass)
- Execute arbitrary code

The primary attack surface is **deserialization** — if you call `Metadata.from_dict()` or `Annotated` with untrusted user-supplied data, validate inputs before passing them to the library.
