# Changelog

## 2.0.0

Typed release for the non-offensive helpers. Brute-force, exploit, bypass, hash-cracker, crawler, proxy, port-scan, and vulnerability-scanner modules are unchanged.

- Add pydantic v2 models: `Options`, `Response`, `PdfMetadata`, `AudioMetadata`, `ImageMetadata`, `WrittenFile`, and `MacVendor`.
- Metadata and lookup functions return those models. `model_dump()` and `model_dump_json()` are the dict and JSON forms. `render` uses them when given a model.
- Missing files raise `FileNotFoundError`. Unreadable files raise `ReadError`. Writers return `WrittenFile` instead of `None`, `True`, or `False`.
- Unknown MAC prefixes are `vendor=None` instead of `""`.
- Ship `unsafe/py.typed` and run mypy in strict mode on the typed modules. The unchanged attack and scanner trees are excluded.
- `urllib3` is `>=2.8.0,<3` and `requests` is `>=2.34.2,<3`. Snyk still reports the last 1.26 release, 1.26.20, and `urllib3` 2.8 requires Python 3.10, so 3.9 is no longer supported.
- `certifi` is at least 2026.10.23. `PyPDF2` is replaced by `pypdf>=6.21.4` because PyPDF2 has no fixed release.
- Pillow is not a dependency. Transitive pins for `charset-normalizer`, `idna`, and `soupsieve` are gone.
- `import unsafe` no longer ignores every warning.
- Audio edits copy the source file and keep its extension. `decrypt_caesar` defaults to a shift of 5.
