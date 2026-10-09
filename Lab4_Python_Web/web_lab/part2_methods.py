# Laborator: functii, metode si importuri pe web
# Student: Galusca Dumitru | SI-266
# Partea 2: exercitiile 9-20 (metode si atribute)

import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde


def main():
    """Executa cererile si exemplele din partea 2."""
    print("\nEX. 9 - Elementele raspunsului")
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    print("status_code:", response.status_code)  # atribut
    print("ok:", response.ok)                  # atribut
    print("url:", response.url)                # atribut
    print("encoding:", response.encoding)      # atribut

    print("\nEX. 10 - raise_for_status()")
    try:
        response.raise_for_status()  # metoda
        print("Pagina principala nu a produs eroare HTTP.")
    except requests.HTTPError as error:
        print("Pagina principala are o eroare HTTP:", error)
    time.sleep(1)
    missing_page = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    try:
        missing_page.raise_for_status()
        print("Pagina de test a returnat:", missing_page.status_code)
    except requests.HTTPError as error:
        print("Pagina lipseste sau serverul refuza accesul:", error)

    print("\nEX. 11 - Antete (items este metoda)")
    for name, value in response.headers.items():
        print(f"{name}: {value}")

    print("\nEX. 12 - headers.get()")
    print("Server:", response.headers.get("Server", "lipseste"))
    print("Content-Type:", response.headers.get("Content-Type", "lipseste"))
    print("content-type:", response.headers.get("content-type", "lipseste"))
    # Cheile antetelor HTTP din requests sunt insensibile la majuscule.

    print("\nEX. 13 - lower().count()")
    print("Aparitii ale 'cyber':", response.text.lower().count("cyber"))
    # lower() produce un sir nou pe care putem apela apoi metoda count().

    print("\nEX. 14 - find() si slicing")
    html = response.text
    html_lower = html.lower()
    start = html_lower.find("<title>")
    if start >= 0:
        start += len("<title>")
        end = html_lower.find("</title>", start)
        title = html[start:end].strip() if end >= 0 else "Titlu neinchis"
    else:
        title = "Titlu negasit"
    print("Titlu:", title)

    print("\nEX. 15 - splitlines()")
    lines = response.text.splitlines()
    print("Linii HTML:", len(lines))
    print("Lungimea liniei maxime:", len(max(lines, key=len)) if lines else 0)

    print("\nEX. 16 - startswith()")
    print("Conexiune securizata" if response.url.startswith("https://")
          else "Conexiune nesecurizata")

    print("\nEX. 17 - Istoric redirectionari HTTP")
    time.sleep(1)
    redirect_response = requests.get("http://cybercor.org", timeout=TIMEOUT)
    for item in redirect_response.history:
        print(item.status_code, item.url, "=>", item.headers.get("Location", "?"))
    print("URL final:", redirect_response.url)

    print("\nEX. 18 - HEAD versus GET")
    time.sleep(1)
    head_response = requests.head(BASE_URL, timeout=TIMEOUT)
    time.sleep(1)
    get_response = requests.get(BASE_URL, timeout=TIMEOUT)
    print("HEAD, bytes:", len(head_response.content))
    print("GET, bytes:", len(get_response.content))
    # HEAD returneaza antete, fara corp; GET returneaza si corpul paginii.

    print("\nEX. 19 - Cookie-uri")
    if get_response.cookies:
        for cookie in get_response.cookies:
            print(cookie.name, "secure:", cookie.secure)
    else:
        print("Niciun cookie setat")

    print("\nEX. 20 - Session si User-Agent personalizat (doar httpbin)")
    time.sleep(1)
    with requests.Session() as session:
        session.headers.update({"User-Agent": "WebLab-Galusca_Dumitru"})
        echoed = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
        echoed.raise_for_status()
        print("User-Agent primit de httpbin:", echoed.json().get("headers", {}).get("User-Agent"))
    # response.text este atribut (sir); response.json() este metoda care
    # transforma continutul JSON intr-un obiect Python.


if __name__ == "__main__":
    try:
        main()
    except (requests.RequestException, ValueError) as error:
        print("Eroare de retea sau raspuns JSON. Verificati accesul:", error)
        raise SystemExit(1)
