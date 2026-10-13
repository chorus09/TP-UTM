from checker import (
    SITES,
    build_url,
    is_https,
    show_response,
    check_site,
    scan_sites,
    check_headers,
    retry_check
)

print("\nPART-1")
print(build_url("example.com", "login"))
print(build_url("example.com", "/login"))
print(is_https(SITES[0]))
print(is_https(SITES[9]))

print("\nPART-2")
show_response(SITES[0])
show_response(SITES[6])

print("\nPART-3")
for url in SITES:
    print(url, "->", check_site(url))

print("\nPART-4")
scan_sites()

print("\nPART-5")
for url in (SITES[10], SITES[11], SITES[9]):
    print(url, "->", check_headers(url))

print("\nPART-6=")
for url in (SITES[3], SITES[6], SITES[7], SITES[9]):
    print(url, "->", retry_check(url))
print("\n----------------------")
print("2 attempts for (retry_check)", retry_check(SITES[7], attempts=2))