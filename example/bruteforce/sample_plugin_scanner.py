from unsafe import bruteforce

plugins = bruteforce.plugin_scanner(
    domain="schechtl.de",
    timeout=5,
    worker=10
)

if plugins:
    print(plugins)