from unsafe import bruteforce

admin_urls = bruteforce.admin_finder(
    domain="portal.saorg.ir",
    timeout=10,
    extension=bruteforce.Extensions.PHP,
    proxies=[
        "http://127.0.0.1:3128",
        "http://127.0.0.2:3128",
        "http://127.0.0.3:3128",
        "http://127.0.0.4:3128",
    ],
    random_agent=True,
    worker=10
)


if admin_urls:
    print("I Found some urls related to admin panel.")
    print(admin_urls)