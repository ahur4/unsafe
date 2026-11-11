# Changelog

## 1.4.0

Maintenance release. Brute-force, exploit, bypass, hash-cracker, crawler, proxy, port-scan, and vulnerability-scanner modules are unchanged.

- Publish the version from `unsafe/__version__.py` and stop ignoring every warning on import.
- Read `README.md` as UTF-8 during packaging, and install only the `unsafe` packages.
- Upgrade `certifi` to at least 2026.10.23 and `requests` so the HTTP stack installs cleanly. `urllib3` is `>=2.8.0,<3`. The last 1.26 release, 1.26.20, is still vulnerable, so the 1.26 line is not used.
- Replace `PyPDF2` with `pypdf>=6.21.4`. PyPDF2 has no fixed release for its known issues. Minimum Python is 3.9 because that pypdf line requires it.
- Drop the unused Pillow pin and stop pinning transitive packages (`charset-normalizer`, `idna`, `soupsieve`).
- Add `unsafe.config.Options` for timeout, headers, proxies, concurrency, verbosity, output format, and retry settings.
- Add `unsafe.http.request`, a standalone client with exponential backoff. It is not used by the existing feature modules. Only GET, HEAD, and OPTIONS are retried unless `retry_methods` says otherwise.
- Return plain dictionaries from PDF metadata reads. A PDF with no info dictionary returns `{}`; a read error still returns `None`.
- Write audio-metadata edits to a real copy beside the source file, preserving its extension. String tags such as `title` work on ID3 files, including WAV.
- `decrypt_caesar` now defaults to a shift of 5, the same default as `encrypt_caesar`.
- Document that an unknown MAC prefix returns an empty string.
- Add a pytest suite and a GitHub Actions workflow that lints and tests.
