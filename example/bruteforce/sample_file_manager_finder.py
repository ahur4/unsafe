from unsafe import bruteforce

file_managers_url = bruteforce.file_manager_finder(
    domain="lacasadepinturas.com",
    timeout=10,
    random_agent=True,
    worker=10
)

if file_managers_url:
    print(file_managers_url)