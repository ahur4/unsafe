![PyPI](https://img.shields.io/pypi/v/unsafe?style=for-the-badge)

# unsafe

Python helpers for cryptography, file metadata, and security testing. Version 2.0.0 types the non-offensive helpers and returns pydantic models from them. The existing brute-force, exploit, bypass, crawler, proxy, port-scan, and vulnerability-scanner modules are still in the package and were not changed. This README does not add usage instructions for those modules. Older snippets live in `example/` and still match that unchanged code.

Author: Ahur4

## Install

Python 3.10 or newer. Python 3.9 cannot install `urllib3` 2.8, which is the first release Snyk treats as not vulnerable.

```bash
pip install unsafe
```

From a checkout:

```bash
pip install -e ".[dev]"
python -c "import unsafe; print(unsafe.__version__)"
```

`pip install` reads `setup.py`. The version string itself lives in `unsafe/__version__.py`.

Runtime dependencies:

| Package | Constraint | Why it is here |
| --- | --- | --- |
| requests | `>=2.34.2,<3` | Imported by existing network and web modules. 2.34.2 needs Python 3.10 |
| urllib3 | `>=2.8.0,<3` | First 2.x release Snyk reports as not vulnerable. Needs Python 3.10 |
| pydantic | `>=2.10` | Models for config and the typed non-offensive results |
| certifi | `>=2026.10.23` | CA bundle used by requests |
| beautifulsoup4 | `>=4.12.3` | Imported while the web modules load |
| mutagen | `>=1.47.0` | Audio metadata |
| plum-py | `>=0.8.7` | JPEG EXIF parser |
| pypdf | `>=6.21.4` | PDF metadata. Replaces PyPDF2, which has no fixed release |
| PySocks | `>=1.7.1` | SOCKS proxy URLs in the existing proxy helper |

Pillow is not required. `charset-normalizer`, `idna`, and `soupsieve` are not pinned; the libraries above pull in compatible versions.

## Quickstart

```python
import unsafe
from unsafe.config import Options, set_options, use_options, render
from unsafe.http import request

print(unsafe.__version__)

set_options(Options(timeout=5, verbosity=1, output_format="json"))
print(render({"status": "ready"}))

with use_options(timeout=2):
    response = request("https://example.com")
print(response.status, response.text[:40])
```

`request` is a general HTTP client. Nothing else in the package calls it.

Encoding and digests:

```python
from unsafe import cryptography

secret = cryptography.encrypt_caesar("Abc xyz!")
assert cryptography.decrypt_caesar(secret) == "Abc xyz!"
print(cryptography.hash_sha256("abc"))
```

MAC vendor lookup uses a table shipped with the package. It does not contact the network. The return value is a `MacVendor` model. `vendor` is `None` when the prefix is unknown. Fewer than six hex digits raises `KeyError`.

```python
from unsafe import network

found = network.mac_address_lookup("00:00:5e:00:53:af")
print(found.vendor)
print(found.model_dump_json())
```

## Configuration

`unsafe.config.Options` is a frozen pydantic model. Invalid values raise `ValidationError` (a `ValueError`). Build a new one with `replace` or `use_options`. Header and proxy mappings replace the previous mapping; they are not merged, and later changes to the dict you passed in are ignored. `options.model_dump()` is a plain dict and `options.model_dump_json()` is JSON.

| Field | Default | Meaning |
| --- | --- | --- |
| `timeout` | `10.0` | Seconds for `unsafe.http.request` |
| `headers` | `{}` | Default request headers |
| `proxies` | `None` | urllib proxy map, for example `{"http": "http://127.0.0.1:8080"}`. Environment proxy variables are not read |
| `concurrency` | `1` | Worker count for `map_concurrent` |
| `verbosity` | `0` | `0` warning, `1` info, `2` or more debug, on the `unsafe` logger only |
| `output_format` | `"text"` | `"text"` or `"json"` for `render` |
| `max_attempts` | `3` | Total tries, including the first |
| `backoff_factor` | `0.5` | Base delay in seconds |
| `retry_statuses` | `429, 500, 502, 503, 504` | Status codes that can be retried |
| `retry_methods` | `GET, HEAD, OPTIONS` | Methods that use `max_attempts`. Others run once |

```python
from unsafe.config import Options, get_options, map_concurrent, render, set_options, use_options

set_options(Options(timeout=8, headers={"Accept": "application/json"}, verbosity=1))

with use_options(output_format="json", concurrency=4) as options:
    print(render({"ok": True}))
    print(map_concurrent(lambda value: value + 1, [1, 2, 3], options))

assert get_options().timeout == 8
```

`map_concurrent` preserves input order. With `concurrency` of 1 it runs in the caller. No other module calls it.

`render` prints mappings as `key: value` lines, sequences as one item per line, and JSON with sorted keys and an indent of 2 when the format is `json`. A pydantic model uses `model_dump_json(indent=2)` for JSON and `model_dump()` for text.

## HTTP retry

`unsafe.http.request(url, method="GET", *, data=None, headers=None, timeout=None, options=None)` sends one request.

- Per-call headers override option headers. The default `User-Agent` is `unsafe/` plus the package version when the caller did not set one.
- `data` must be `bytes` or `None`.
- The return value is a pydantic `Response`. A completed response is returned for every HTTP status, including 404 and a final 500. `status`, `headers`, `content`, and `text` expose it. `json_body()` parses the body. `model_dump()` and `model_dump_json()` include `text`; a UTF-8 body is a JSON string in the JSON form.
- Connection failures (`URLError`, `TimeoutError`, `OSError`) are retried only for methods in `retry_methods`. The last error is raised when the attempts are used up.
- Before retry number `n` (1 after the first failure, 2 after the second, and so on) the client waits `backoff_factor * 2 ** (n - 1)` seconds. A factor of 0.5 waits 0.5s, then 1s, then 2s. A factor of 0 does not sleep.
- POST, PUT, PATCH, and DELETE run once unless you put that method in `retry_methods`.

```python
from unsafe.config import Options
from unsafe.http import request

response = request(
    "https://example.com",
    options=Options(max_attempts=3, backoff_factor=0.5, timeout=5),
)
if response.status == 200:
    print(response.text)
```

Pass `transport` and `sleeper` only in tests. The default transport uses `urllib` and the proxy map on the options object.

## Typed results

These models are the success return types. A missing file raises `FileNotFoundError`. A file that exists but cannot be parsed raises `unsafe.ReadError`. Writers no longer return `None` or `False`.

| Function | Returns |
| --- | --- |
| `get_pdf_metadata` | `PdfMetadata` |
| `edit_pdf_metadata`, `del_pdf_metadata` | `WrittenFile` |
| `get_audio_metadata` | `AudioMetadata` |
| `edit_audio_metadata`, `del_audio_metadata` | `WrittenFile` |
| `get_image_metadata` | `ImageMetadata` |
| `edit_image_metadata`, `del_image_metadata` | `WrittenFile` |
| `mac_address_lookup` | `MacVendor` |
| `http.request` | `Response` |
| `config.Options` | the options model itself |

Metadata models store strings in `entries`. `document["title"]` reads that mapping. `document.model_dump()` and `document.model_dump_json()` are the plain dict and JSON forms. `render(document)` uses those when `output_format` is `text` or `json`.

An unknown MAC prefix is `MacVendor.vendor is None`, not an empty string.

## Forensics

Image helpers read and edit JPEG EXIF. `entries` is empty when the file has no EXIF. Edits and deletions modify that file and return `WrittenFile`.

```python
from unsafe import forensic

tags = forensic.get_image_metadata("photo.jpg")
print(tags.entries)
forensic.edit_image_metadata("photo.jpg", "image_description", "Hello")
forensic.del_image_metadata("photo.jpg")
```

PDF reads return `PdfMetadata`. Keys keep the leading slash, such as `/Title`. A file with no info dictionary has empty `entries`. `edit_pdf_metadata` and `del_pdf_metadata` write a new file under `output_PDF` next to the source and return `WrittenFile`. Keys may be passed with or without the leading slash. pypdf may still write its own `/Producer` entry.

```python
from unsafe import forensic

info = forensic.get_pdf_metadata("notes.pdf")
print(info["/Title"])
written = forensic.edit_pdf_metadata("notes.pdf", {"Author": "Ada"})
print(written.path)
```

Audio reads return `AudioMetadata`. Edits and deletions copy the file into `AUDIO_output` beside the source, keep the original extension, and return `WrittenFile`. The source file is not modified. ID3 files, including WAV, accept names such as `title` and `artist`. An unknown tag name raises `ValueError`.

```python
from unsafe import forensic

print(forensic.get_audio_metadata("clip.wav").model_dump())
written = forensic.edit_audio_metadata("clip.wav", {"title": "Hello"})
```

## Cryptography

These functions only transform the string you pass in.

| Encrypt | Decrypt |
| --- | --- |
| `encrypt_base64` | `decrypt_base64` |
| `encrypt_base32` | `decrypt_base32` |
| `encrypt_base16` | `decrypt_base16` |
| `encrypt_base85` | `decrypt_base85` |
| `encrypt_ascii85` | `decrypt_ascii85` |
| `encrypt_caesar(text, pointer=5)` | `decrypt_caesar(text, pointer=5)` |

Caesar shifts letters and leaves every other character in place. `pointer` must be an integer from 1 through 26.

Digests: `hash_md5`, `hash_sha1`, `hash_sha224`, `hash_sha256`, `hash_sha384`, `hash_sha512`, `hash_sha3_224`, `hash_sha3_256`, `hash_sha3_384`, `hash_sha3_512`, `hash_shake128(text, length=20)`, `hash_shake256(text, length=20)`. SHAKE `length` is the number of bytes passed to `hexdigest`.

`hash_cracker` is still exported and was not changed.

## Other modules

Names below are the public callables that already existed. Their code was not modified in 2.0.0, and this document does not show how to run them. `mac_address_lookup` is the exception: it now returns `MacVendor`.

- `unsafe.bruteforce`: `admin_finder`, `file_manager_finder`, `plugin_scanner`, `cloud_bypasser`
- `unsafe.exploits`: `CVE_2021_42013`, `CVE_2024_7313`, `CVE_2024_7339`, `CVE_2024_7928`
- `unsafe.network`: `port_scanner`, `proxy_tester`, `get_http_proxy`, `get_socks4_proxy`, `get_socks5_proxy`, `mac_address_lookup`
- `unsafe.web`: `search_browser`, `crawl_page`, `xss_scanner`, `sql_injection_scanner`

## Behavior changes in 2.0.0

Compared with 1.3, and with the unreleased 1.4 work on this branch:

- Metadata reads return pydantic models, not `dict` or `None`.
- Metadata writes return `WrittenFile` instead of `str`, `None`, `True`, or `False`.
- A missing metadata file raises `FileNotFoundError`. Image helpers used to raise `ValueError` for that case.
- A corrupt or unrecognized file raises `ReadError` instead of returning `None` or `False`.
- `mac_address_lookup` returns `MacVendor`. Unknown prefixes use `vendor=None` instead of `""`. Too-short values still raise `KeyError`.
- `import unsafe` no longer calls `warnings.filterwarnings("ignore")`.
- Audio edits copy the source beside the original file and keep its suffix.
- `decrypt_caesar` defaults `pointer` to 5.
- Minimum Python is 3.10.

## Tests

Tests use pytest and do not open network connections. HTTP coverage passes a fake transport or replaces `urllib.request.build_opener`.

```bash
pip install -e ".[dev]"
pytest
ruff check unsafe tests
mypy unsafe
```

The package ships `unsafe/py.typed`.

GitHub Actions (`.github/workflows/ci.yml`) runs Ruff and mypy on Python 3.12, and mypy plus pytest on 3.10, 3.11, and 3.12.

Ruff and mypy do not scan the unchanged brute-force, exploit, web, scanner, proxy, hash-cracker, EXIF-parser, or word-list sources. Those trees were left as they were so the checks do not require editing them. mypy also skips `mutagen` and `bs4`, which have no type stubs.

## License

MIT. See `LICENSE`.
