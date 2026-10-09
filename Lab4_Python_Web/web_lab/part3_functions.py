# Laborator: functii, metode si importuri pe web
# Student: Galusca Dumitru | SI-266
# Partea 3: exercitiile 21-34 (functii cu docstring)
from __future__ import annotations

import time
from urllib.parse import urljoin

import requests
import webtools

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde


def fetch(url: str, timeout: int = 10) -> requests.Response:
    """Ex. 21 si 23: descarca URL-ul cu timeout implicit sau explicit."""
    return webtools.fetch(url, timeout=timeout)


def get_status(url: str) -> int:
    """Ex. 22 si 26: returneaza codul de stare HTTP."""
    return fetch(url).status_code


def get_title(html: str) -> str | None:
    """Ex. 24-25: returneaza titlul din text HTML fara cereri de retea."""
    normalized = html.lower()
    begin = normalized.find("<title>")
    if begin == -1:
        return None
    begin += len("<title>")
    finish = normalized.find("</title>", begin)
    return html[begin:finish].strip() if finish >= 0 else None


def page_exists(url: str) -> bool:
    """Ex. 27: verifica daca URL-ul raspunde fara eroare HTTP/retea."""
    try:
        # Exemplul .invalid apare explicit in cerintele exercitiului 27.
        if url.endswith(".invalid"):
            result = requests.get(url, timeout=TIMEOUT)
        else:
            result = fetch(url)
        result.raise_for_status()
        return True
    except requests.RequestException:
        return False


def check_paths(base: str, paths: list[str]) -> dict[str, int | None]:
    """Ex. 28: asociaza fiecare cale cu statusul ei HTTP."""
    results = {}
    for path in paths:
        url = urljoin(base.rstrip("/") + "/", path.lstrip("/"))
        results[path] = get_status(url)
    return results


def get_header(url: str, name: str, default: str = "lipseste") -> str:
    """Ex. 29: returneaza antetul indicat sau valoarea implicita."""
    return fetch(url).headers.get(name, default)


def security_headers(url: str) -> dict[str, bool]:
    """Ex. 30: indica prezenta celor cinci antete de securitate."""
    response = fetch(url)
    names = (
        "Strict-Transport-Security", "Content-Security-Policy",
        "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy",
    )
    return {name: name in response.headers for name in names}


def score_headers(results: dict[str, bool]) -> str:
    """Ex. 31: transforma indicii de securitate intr-un scor x/5."""
    return f"{sum(results.values())}/{len(results)}"


def fetch_robots(base: str) -> str | None:
    """Ex. 32: citeste robots.txt sau returneaza None daca lipseste."""
    try:
        response = fetch(base.rstrip("/") + "/robots.txt")
        return response.text if response.status_code < 400 else None
    except requests.RequestException:
        return None


def disallowed_paths(robots_text: str | None) -> list[str]:
    """Ex. 32: extrage din robots.txt directivele Disallow."""
    if robots_text is None:
        return []
    paths = []
    for line in robots_text.splitlines():
        if line.strip().lower().startswith("disallow:"):
            path = line.split(":", 1)[1].split("#", 1)[0].strip()
            if path:
                paths.append(path)
    return paths


def response_times(*urls: str) -> dict[str, float]:
    """Ex. 33: cronometreaza cate o cerere pentru fiecare URL."""
    results = {}
    for url in urls:
        start = time.perf_counter()
        fetch(url)
        results[url] = round(time.perf_counter() - start, 3)
    return results


def log(message: str, **details: object) -> None:
    """Ex. 34: afiseaza detaliile suplimentare primite cu nume."""
    parts = [message]
    for key, value in details.items():
        parts.append(f"{key}={value}")
    print(" | ".join(parts))


def main() -> None:
    """Apeleaza cel putin o data toate functiile exercitiilor 21-34."""
    print("\nEX. 21 - fetch(url)")
    response = fetch(BASE_URL)
    print("Cod HTTP:", response.status_code)

    print("\nEX. 22 - get_status(url) si pauze")
    for path in ("/", "/robots.txt", "/sitemap.xml"):
        print(path, get_status(BASE_URL + path))
        # Pauza dintre cereri este aplicata si de webtools.fetch().

    print("\nEX. 23 - Parametru timeout implicit si explicit")
    print("Implicit:", fetch(BASE_URL).status_code)
    print("Explicit (3 secunde):", fetch(BASE_URL, timeout=3).status_code)

    print("\nEX. 24 - Titlul fara cerere suplimentara")
    print("Titlu:", get_title(response.text))

    print("\nEX. 25 - Documentatia functiei")
    help(get_title)

    print("\nEX. 26 - Type hints nu verifica tipurile automat")
    try:
        print("get_status(123):", get_status(123))
    except (requests.RequestException, ValueError, TypeError) as error:
        print("Argument invalid (adnotarile nu l-au blocat automat):", type(error).__name__)

    print("\nEX. 27 - Tratarea erorilor")
    print("Site valid:", page_exists(BASE_URL))
    print("Domeniu .invalid:", page_exists("https://this-domain-does-not-exist.invalid"))

    print("\nEX. 28 - Dictionar cu statusuri")
    paths = ["/", "/robots.txt", "/sitemap.xml"]
    print(check_paths(BASE_URL, paths))

    print("\nEX. 29 - Argumente cu nume")
    print("Server:", get_header(BASE_URL, name="Server"))

    print("\nEX. 30 - Cinci antete de securitate")
    headers = security_headers(BASE_URL)
    print(headers)

    print("\nEX. 31 - Functii apelate impreuna")
    print("Scor:", score_headers(security_headers(BASE_URL)))

    print("\nEX. 32 - Doua functii pentru robots.txt")
    print(disallowed_paths(fetch_robots(BASE_URL)))
    print("Verificare None:", disallowed_paths(None))

    print("\nEX. 33 - *args")
    print(response_times(BASE_URL + "/", BASE_URL + "/robots.txt"))

    print("\nEX. 34 - **kwargs")
    log("verificat", url=BASE_URL, status=response.status_code)
    # print() afiseaza si nu livreaza rezultatul apelantului; return da o
    # valoare care poate fi pastrata, testata sau reutilizata in alta functie.


if __name__ == "__main__":
    try:
        main()
    except requests.RequestException as error:
        print("Eroare de retea la exercitiile 21-34:", error)
        raise SystemExit(1)
