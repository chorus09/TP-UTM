# Laborator: functii, metode si importuri pe web
# Student: Galusca Dumitru | SI-266
# Partea 4: exercitiile 35-43 (biblioteca standard)
from __future__ import annotations

import hashlib
import json
import re
import socket
import ssl
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import requests
import webtools

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde


def parse_url(url: str) -> dict[str, str]:
    """Ex. 35: separa schema, domeniul, calea, query si fragmentul."""
    parts = urlparse(url)
    return {key: getattr(parts, key) for key in
            ("scheme", "netloc", "path", "query", "fragment")}


def absolute_links(base: str, links: list[str]) -> list[str]:
    """Ex. 36: transforma caile relative in URL-uri absolute."""
    return [urljoin(base.rstrip("/") + "/", link) for link in links]


def extract_links(html: str) -> list[str]:
    """Ex. 37: extrage legaturile href dintre ghilimele, fara duplicate."""
    return list(dict.fromkeys(re.findall(r'href="([^"]+)"', html)))


def split_links(links: list[str], domain: str) -> tuple[list[str], list[str]]:
    """Ex. 38: desparte URL-urile pe acelasi domeniu de cele externe."""
    return webtools.split_links(links, domain)


class ImageFinder(HTMLParser):
    """Ex. 39: colecteaza valorile atributelor src ale tag-urilor img."""

    def __init__(self) -> None:
        """Porneste parserul si creeaza lista de imagini."""
        super().__init__()
        self.images = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Este apelata automat de parser pentru fiecare tag de inceput."""
        if tag.lower() == "img":
            source = dict(attrs).get("src")
            if source is not None:
                self.images.append(source)


def page_fingerprint(url: str) -> str:
    """Ex. 40: returneaza SHA-256 pentru corpul paginii."""
    response = webtools.fetch(url)
    return hashlib.sha256(response.content).hexdigest()


def save_headers_json(url: str, filename: str = "headers.json") -> dict[str, str]:
    """Ex. 41: salveaza antetele intr-un JSON si le incarca inapoi."""
    response = webtools.fetch(url)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(dict(response.headers), file, indent=2, ensure_ascii=False)
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def resolve(hostname: str) -> str:
    """Ex. 42: returneaza adresa IPv4 asociata domeniului."""
    if hostname != "cybercor.org":
        raise ValueError("Se verifica numai domeniul indicat in laborator")
    return socket.gethostbyname(hostname)


def cert_days_left(hostname: str) -> int:
    """Ex. 43: calculeaza zilele ramase pentru certificatul TLS."""
    if hostname != "cybercor.org":
        raise ValueError("Se verifica numai certificatul indicat in laborator")
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as connection:
        with context.wrap_socket(connection, server_hostname=hostname) as secured:
            certificate = secured.getpeercert()
    expiry = datetime.fromtimestamp(
        ssl.cert_time_to_seconds(certificate["notAfter"]), tz=timezone.utc
    )
    return (expiry - datetime.now(timezone.utc)).days


def main() -> None:
    """Executa exemplele din partea 4 si autotestul parserului."""
    print("\nEX. 35 - urlparse")
    print(parse_url("https://cybercor.org/path?x=1#top"))

    print("\nEX. 36 - urljoin")
    print(absolute_links(BASE_URL, ["/about", "contact.html", "../index.html"]))

    print("\nEX. 37 - re.findall pentru href")
    response = webtools.fetch(BASE_URL)
    links = extract_links(response.text)
    print("Legaturi fara duplicate:", links)

    print("\nEX. 38 - Legaturi interne si externe")
    internal, external = split_links(links, urlparse(BASE_URL).netloc)
    print("Interne:", len(internal), "Externe:", len(external))
    # Nu accesam prin retea niciunul dintre linkurile extrase.

    print("\nEX. 39 - HTMLParser si handle_starttag")
    test_html = """
    <html><body>
      <img src="/logo.png" alt="Logo">
      <IMG SRC="poza.jpg">
      <img alt="imagine fara src">
      <img src="https://cdn.example.com/banner.webp" />
      <a href="/despre">Aceasta nu este o imagine</a>
    </body></html>
    """
    finder = ImageFinder()
    finder.feed(test_html)
    print("Test:", finder.images)
    assert finder.images == [
        "/logo.png", "poza.jpg", "https://cdn.example.com/banner.webp"
    ], "Parserul nu a gasit exact imaginile asteptate"
    print("Testul a trecut!")
    finder = ImageFinder()
    finder.feed(response.text)
    print(len(finder.images), "imagini gasite in pagina reala")
    for source in finder.images:
        print(source)
    print("Numar aparitii text '<img':", response.text.lower().count("<img"))
    # Verificare manuala suplimentara: in browser Ctrl+U pentru sursa HTML.
    # handle_starttag() este apelata intern de HTMLParser.feed(), nu direct.

    print("\nEX. 40 - SHA-256")
    first = page_fingerprint(BASE_URL)
    second = page_fingerprint(BASE_URL)
    print("Amprenta 1:", first, "\nAmprenta 2:", second)
    print("Identice:", first == second)
    # Daca serverul schimba chiar si un singur octet HTML, hash-ul poate diferi.

    print("\nEX. 41 - JSON pentru antete")
    headers = save_headers_json(BASE_URL)
    print("Content-Type citit din headers.json:", headers.get("Content-Type", "lipseste"))

    print("\nEX. 42 - Rezolvare DNS")
    try:
        print("IPv4:", resolve("cybercor.org"))
    except (socket.gaierror, OSError) as error:
        print("DNS indisponibil:", error)

    print("\nEX. 43 - Expirarea certificatului TLS")
    try:
        print("Zile ramase:", cert_days_left("cybercor.org"))
    except (ssl.SSLError, OSError, KeyError, ValueError) as error:
        print("Certificat indisponibil:", error)


if __name__ == "__main__":
    try:
        main()
    except requests.RequestException as error:
        print("Eroare de retea la exercitiile 35-43:", error)
        raise SystemExit(1)
