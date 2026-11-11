import re
from pathlib import Path

from setuptools import find_packages, setup

ROOT = Path(__file__).resolve().parent
long_description = (ROOT / "README.md").read_text(encoding="utf-8")
version_match = re.search(
    r'^__version__ = ["\']([^"\']+)["\']',
    (ROOT / "unsafe" / "__version__.py").read_text(encoding="utf-8"),
    re.MULTILINE,
)
if version_match is None:
    raise RuntimeError("unsafe/__version__.py is missing __version__")

# Direct dependencies only. certifi and urllib3 are pinned to a safe floor
# (urllib3 stays on the 1.26 line). Transitive packages such as charset-normalizer,
# idna, and soupsieve are left for those libraries to select.
requirements = [
    "beautifulsoup4>=4.12.3",
    "certifi>=2026.10.23",
    "mutagen>=1.47.0",
    "plum-py>=0.8.7",
    "PyPDF2>=3.0.1",
    "PySocks>=1.7.1",
    "requests>=2.32.3,<3",
    "urllib3>=1.26.20,<1.27",
]

setup(
    name="unsafe",
    version=version_match.group(1),
    author="Ahura Rahmani",
    author_email="ahur4.rahmani@gmail.com",
    license="MIT",
    url="https://github.com/ahur4/unsafe",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4,<8.4",
            "ruff>=0.6",
        ],
    },
    keywords=[
        "hack", "hack-module", "pentest", "unsafe", "osint",
        "osint-python", "hacking-python", "cryptography", "vulnerability-scanner", "vulnerability", "security",
        "hacker", "admin-finder", "wordpress-scanner", "instagram-osint", "cve", "proxy-wrapper", "proxy-checker",
        "ssh-connect", "hydra", "cracker", "sqlmap", "ahur4", "mesutfd", "web", "acunetix",
    ],
    description="A practical and optimal library for those interested in Pentest, cryptography,Vulnerability Scanner and ..",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=["unsafe", "unsafe.*"]),
    python_requires=">=3.8",
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
