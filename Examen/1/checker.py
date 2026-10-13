import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    return "https://" + host + "/" + path.lstrip("/")


def is_https(url):
    return url.startswith("https://")


def show_response(url):
    try:
        response = requests.get(url, timeout=5)
        print("Status:", response.status_code)
        print("Content-Type:", response.headers.get("Content-Type", "unknown"))
    except requests.RequestException as error:
        print("Error:", str(error))


def check_site(url):
    try:
        response = requests.get(url, timeout=5)
        return {
            "status": response.status_code,
            "content_type": response.headers.get("Content-Type", "unknown"),
            "length": len(response.content),
            "server": response.headers.get("Server", "unknown"),
        }
    except requests.RequestException as error:
        return {"status": None, "error": str(error)}


def scan_sites():
    results = []

    for url in SITES:
        results.append((url, check_site(url)))

    working = [
        (url, result)
        for url, result in results
        if result.get("status") == 200
    ]

    working.sort(
        key=lambda item: item[1]["length"],
        reverse=True
    )

    for url, result in working:
        print(f"{url} > 200, {result['length']}")

    print(f"Done: {len(working)} | Erorrs: {len(results) - len(working)}")


def check_headers(url):
    try:
        response = requests.get(url, timeout=5)

        received = {
            header.lower()
            for header in response.headers
        }

        present = [
            header for header in SECURITY_HEADERS
            if header.lower() in received
        ]

        missing = [
            header for header in SECURITY_HEADERS
            if header.lower() not in received
        ]

        score = int(
            100 * len(present) / len(SECURITY_HEADERS)
        )

        return {
            "present": present,
            "missing": missing,
            "score": score
        }

    except requests.RequestException as error:
        return {"status": None, "error": str(error)}


def retry_check(url, attempts=3):
    last_status = None
    last_error = None
    count = 0

    for _ in range(max(0, attempts)):
        count += 1

        try:
            response = requests.get(url, timeout=5)
            last_status = response.status_code
            last_error = None

            if last_status < 500:
                break

        except requests.RequestException as error:
            last_error = str(error)

    result = {
        "status": last_status,
        "attempts": count
    }

    if last_status is None and last_error is not None:
        result["error"] = last_error

    return result
