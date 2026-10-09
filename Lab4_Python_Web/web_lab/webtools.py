# Laborator: functii, metode si importuri pe web
# Student: Galusca Dumitru | Grupa: SI-266
# Modul propriu pentru exercitiile 44-50.
from __future__ import annotations
# Regula: pe cybercor.org doar GET/HEAD, cu timeout si pauze intre cereri.

import hashlib
import json
import re
import socket
import ssl
import time
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10
DEFAULT_HEADERS = {"User-Agent": "WebLab-Galusca_Dumitru"}
SECURITY_HEADERS = (
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
)
ALLOWED_PATHS = ("/", "/robots.txt", "/sitemap.xml", "/this-page-does-not-exist")
_last_request = None


def check_target(url: str) -> None:
    """Valideaza ca URL-ul apartine site-ului permis de laborator."""
    if not isinstance(url, str):
        raise TypeError("URL-ul trebuie sa fie un sir de caractere")
    parsed = urlparse(url)
    if (parsed.scheme not in ("http", "https") or
            parsed.hostname != "cybercor.org" or
            parsed.port is not None or
            parsed.path not in ("",) + ALLOWED_PATHS or
            parsed.query or parsed.fragment or parsed.username or parsed.password):
        raise ValueError("Laboratorul permite doar paginile indicate de pe cybercor.org")


def _pause_between_requests() -> None:
    """Pastreaza cel putin o secunda intre cererile din acest proces."""
    global _last_request
    if _last_request is not None:
        time.sleep(1)  # pauza intre doua cereri consecutive
    _last_request = time.monotonic()


def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    """Returneaza raspunsul GET. Foloseste timeout si antetul laboratorului."""
    check_target(url)
    _pause_between_requests()
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)


def get_status(url: str) -> int:
    """Returneaza codul HTTP pentru URL-ul indicat."""
    return fetch(url).status_code


def get_title(html: str) -> str | None:
    """Extrage si returneaza titlul din HTML, fara a accesa reteaua."""
    normalized = html.lower()
    start_tag, end_tag = "<title>", "</title>"
    start = normalized.find(start_tag)
    if start < 0:
        return None
    start += len(start_tag)
    end = normalized.find(end_tag, start)
    return html[start:end].strip() if end >= 0 else None


def security_headers(url: str) -> dict[str, bool]:
    """Verifica prezenta a cinci antete de securitate HTTP."""
    response = fetch(url)
    return {header: header in response.headers for header in SECURITY_HEADERS}


def score_headers(results: dict[str, bool]) -> str:
    """Transforma rezultatele True/False in scor de tipul 3/5."""
    return f"{sum(results.values())}/{len(results)}"


def check_paths(base: str, paths: list[str]) -> dict[str, int | None]:
    """Obtine codurile HTTP pentru lista limitata de cai din laborator."""
    statuses = {}
    for path in paths:
        url = urljoin(base.rstrip("/") + "/", path.lstrip("/"))
        check_target(url)
        try:
            statuses[path] = get_status(url)
        except requests.RequestException as error:
            print(f"Cererea pentru {path} a esuat: {error}")
            statuses[path] = None
    return statuses


def fetch_robots(base: str) -> str | None:
    """Returneaza robots.txt sau None cand lipseste / este inaccesibil."""
    try:
        response = fetch(base.rstrip("/") + "/robots.txt")
        if response.status_code >= 400:
            return None
        return response.text
    except requests.RequestException:
        return None


def disallowed_paths(robots_text: str | None) -> list[str]:
    """Extrage caile mentionate in liniile Disallow din robots.txt."""
    if robots_text is None:
        return []
    paths = []
    for line in robots_text.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("disallow:"):
            path = stripped.split(":", 1)[1].split("#", 1)[0].strip()
            if path:
                paths.append(path)
    return paths


def response_times(*urls: str) -> dict[str, float]:
    """Masoara timpul total al cererilor, in secunde."""
    result = {}
    for url in urls:
        start = time.perf_counter()
        fetch(url)
        result[url] = round(time.perf_counter() - start, 3)
    return result


def log(message: str, **details: object) -> None:
    """Afiseaza un mesaj urmat de argumentele transmise cu nume."""
    parts = [message] + [f"{key}={value}" for key, value in details.items()]
    print(" | ".join(parts))


def extract_links(html: str) -> list[str]:
    """Returneaza legaturile href cu ghilimele duble, fara duplicate."""
    matches = re.findall(r'href="([^"]+)"', html)
    return list(dict.fromkeys(matches))


def split_links(links: list[str], domain: str) -> tuple[list[str], list[str]]:
    """Imparte legaturile HTTP(S) in interne si externe dupa domeniu."""
    internal, external = [], []
    for link in links:
        absolute = urljoin(BASE_URL + "/", link)
        parsed = urlparse(absolute)
        if parsed.scheme not in ("http", "https"):
            continue  # mailto:, javascript:, tel: nu reprezinta pagini web
        (internal if parsed.netloc.lower() == domain.lower() else external).append(absolute)
    return internal, external


def resolve(hostname: str) -> str:
    """Obtine adresa IPv4 a unui domeniu folosind DNS."""
    if hostname != "cybercor.org":
        raise ValueError("Se permite rezolvarea doar a domeniului laboratorului")
    return socket.gethostbyname(hostname)


def cert_days_left(hostname: str) -> int:
    """Returneaza zilele ramase pana la expirarea certificatului TLS."""
    if hostname != "cybercor.org":
        raise ValueError("Se verifica doar certificatul domeniului laboratorului")
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as raw_socket:
        with context.wrap_socket(raw_socket, server_hostname=hostname) as secure_socket:
            certificate = secure_socket.getpeercert()
    expires = datetime.fromtimestamp(
        ssl.cert_time_to_seconds(certificate["notAfter"]), tz=timezone.utc
    )
    return (expires - datetime.now(timezone.utc)).days


def page_fingerprint(url: str) -> str:
    """Calculeaza suma SHA-256 a continutului HTTP returnat."""
    return hashlib.sha256(fetch(url).content).hexdigest()


def redirect_chain(base: str) -> list[dict[str, object]]:
    """Intoarce redirectionarile observate de la varianta HTTP a site-ului."""
    url = "http://cybercor.org/"
    _pause_between_requests()
    response = requests.get(url, timeout=TIMEOUT, headers=DEFAULT_HEADERS)
    return [{"status": item.status_code, "url": item.url, "location": item.headers.get("Location")}
            for item in response.history]


def site_report(url: str) -> dict[str, object]:
    """Genereaza si salveaza in report.json raportul despre site-ul permis."""
    check_target(url)
    response = fetch(url)
    hostname = urlparse(url).hostname
    title = get_title(response.text)
    headers = security_headers(url)
    links = extract_links(response.text)
    internal, external = split_links(links, hostname)
    robots = disallowed_paths(fetch_robots(url))

    # La erorile de conexiune pastram None pentru valorile indisponibile.
    try:
        ip = resolve(hostname)
    except (OSError, ValueError) as error:
        print("Nu am putut obtine IP-ul:", error)
        ip = None
    try:
        days = cert_days_left(hostname)
    except (OSError, ssl.SSLError, KeyError, ValueError) as error:
        print("Nu am putut citi certificatul TLS:", error)
        days = None
    try:
        redirects = redirect_chain(url)
    except requests.RequestException as error:
        print("Nu am putut urmari redirectionarile:", error)
        redirects = []

    report = {
        "student": "Galusca Dumitru", "grupa": "SI-266",
        "checked_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "requested_url": url, "status_code": response.status_code,
        "final_url": response.url, "title": title, "ip_address": ip,
        "redirects_from_http": redirects,
        "security_headers": headers, "security_score": score_headers(headers),
        "certificate_days_left": days,
        "links_internal": len(internal), "links_external": len(external),
        "robots_disallowed_paths": robots,
    }
    print(f"\n=== Raport site: {url} ===")
    print("Cod de stare:", report["status_code"])
    print("URL final:", report["final_url"])
    print("Titlu:", title or "lipseste")
    print("Adresa IP:", ip if ip is not None else "indisponibila")
    print("Redirectionari:", redirects if redirects else "niciuna sau indisponibile")
    print("Scor securitate:", report["security_score"])
    print("Certificat:", days if days is not None else "indisponibil", "zile ramase" if days is not None else "")
    print("Legaturi:", len(internal), "interne,", len(external), "externe")
    print("Cai interzise:", ", ".join(robots) if robots else "niciuna identificata")
    with open("report.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)
    print("Salvat in report.json")
    return report


if __name__ == "__main__":
    # Ex. 46: autotestul se lanseaza DOAR prin `python webtools.py`.
    try:
        print("Autotest:", get_status(BASE_URL))
    except requests.RequestException as error:
        print("Autotest imposibil (reteaua nu a raspuns):", error)
        raise SystemExit(1)
