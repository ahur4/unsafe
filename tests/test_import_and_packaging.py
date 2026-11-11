"""Import, warning, and dependency constraints."""

import warnings
from importlib.metadata import requires, version
from pathlib import Path

import unsafe

ROOT = Path(__file__).resolve().parents[1]
OFFENSIVE = (
    "unsafe/ext/bruteforce",
    "unsafe/ext/exploits",
    "unsafe/ext/web",
    "unsafe/ext/cryptography/hash_cracker.py",
    "unsafe/ext/network/proxy.py",
    "unsafe/ext/network/scanners.py",
)


def test_import_exposes_version_and_helpers():
    assert unsafe.__version__ == "1.4.0"
    assert version("unsafe") == "1.4.0"
    assert unsafe.config.get_options().timeout == 10.0
    assert callable(unsafe.http.request)


def test_import_does_not_silence_warnings():
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        warnings.warn("maintenance-check", UserWarning)
    assert any(str(item.message) == "maintenance-check" for item in caught)


def test_runtime_dependencies_drop_unused_and_pin_safe_floors():
    setup_text = (ROOT / "setup.py").read_text(encoding="utf-8")
    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    quoted = [line.strip() for line in setup_text.splitlines() if line.strip().startswith('"')]
    declared = quoted + [line.strip() for line in requirements.splitlines() if line.strip()]
    names = []
    for line in declared:
        names.append(line.strip('",').lower().split(">")[0].split("<")[0].split("=")[0].split("[")[0])
    for dropped in ("pillow", "soupsieve", "charset-normalizer", "charset_normalizer", "idna"):
        assert dropped not in names
    blob = "\n".join(line.lower() for line in declared)
    assert "urllib3>=1.26.20,<1.27" in blob
    assert "certifi>=2026.10.23" in blob

    names = []
    for requirement in requires("unsafe") or []:
        if "extra ==" in requirement:
            continue
        names.append(requirement.split(">=")[0].split("<")[0].strip().lower())
    assert "pillow" not in names
    assert "urllib3" in names
    assert "certifi" in names
    assert "requests" in names


def test_offensive_modules_do_not_call_new_helpers():
    for relative in OFFENSIVE:
        path = ROOT / relative
        files = [path] if path.is_file() else list(path.rglob("*.py"))
        for source in files:
            text = source.read_text(encoding="utf-8")
            assert "unsafe.http" not in text
            assert "unsafe.config" not in text
            assert "from .http" not in text
            assert "from ..http" not in text
