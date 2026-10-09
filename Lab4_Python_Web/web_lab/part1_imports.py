# Laborator: functii, metode si importuri pe web
# Student: Galusca Dumitru | SI-266
# Partea 1: exercitiile 1-8 (importuri)

import time
import urllib.request
import urllib.error
import requests
from requests import get
import requests as rq

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde


def main():
    """Parcurge in ordine toate demonstratiile din partea 1."""
    print("\nEX. 1 - Primul import")
    print("requests:", requests.__version__)
    print("urllib.request:", urllib.request.__name__)
    # requests este extern, deci se instaleaza cu pip; urllib vine cu Python.

    print("\nEX. 2 - Doua stiluri de import")
    # 'import requests' arata explicit modulul; 'from ... import get' este mai scurt,
    # dar poate crea confuzii daca avem mai multe functii numite get.
    time.sleep(1)
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    print("requests.get:", response.status_code)
    time.sleep(1)
    response = get(BASE_URL, timeout=TIMEOUT)
    print("from requests import get:", response.status_code)

    print("\nEX. 3 - Alias-uri")
    # Aliasul rq scurteaza codul repetitiv; un alias necunoscut scade lizibilitatea.
    time.sleep(1)
    response = rq.get(BASE_URL, timeout=TIMEOUT)
    print("rq.get:", response.status_code)

    print("\nEX. 4 - Doar biblioteca standard")
    time.sleep(1)
    # Serverul poate raspunde diferit la cererile urllib si requests.
    # Daca apare un HTTPError, afisam codul si continutul raspunsului.
    try:
        with urllib.request.urlopen(BASE_URL, timeout=TIMEOUT) as response:
            print("status:", response.status)
            html = response.read().decode("utf-8", errors="replace")
            print("Primele 200 de caractere:", html[:200])
    except urllib.error.HTTPError as error:
        print("status:", error.code)
        print("Raspunsul HTTP a fost refuzat de server pentru urllib:", error.reason)
        print("Primele 200 de caractere din raspunsul de eroare:",
              error.read(200).decode("utf-8", errors="replace"))
        print("Trecem la exercitiul urmator.")
    except urllib.error.URLError as error:
        print("Nu am primit raspuns la cererea urllib:", error.reason)
        print("Trecem la exercitiul urmator.")

    print("\nEX. 5 - Inspectarea unui modul")
    print("dir(requests):", dir(requests))
    # requests.get = functie; requests.Session = clasa;
    # requests.adapters = modul.

    print("\nEX. 6 - Documentatia functiei get")
    help(requests.get)
    # Parametrul pentru limita asteptarii este timeout.
    time.sleep(1)
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    print("Status cu timeout:", response.status_code)

    print("\nEX. 7 - Cronometrarea cererii")
    time.sleep(1)
    start = time.perf_counter()
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    duration = time.perf_counter() - start
    print("time.perf_counter:", round(duration, 3), "s")
    print("response.elapsed:", response.elapsed.total_seconds(), "s")

    print("\nEX. 8 - ImportError")
    try:
        import bs4
        print("bs4 exista. Versiune:", bs4.__version__)
    except ImportError:
        print("Instalati modulul cu: pip install beautifulsoup4")
    # Modul = fisier Python; pachet = colectie de module; biblioteca =
    # colectie de functionalitati si pachete disponibile programatorului.


if __name__ == "__main__":
    try:
        main()
    except (requests.RequestException, OSError) as error:
        print("Eroare de retea. Reincercati dupa ce verificati conexiunea:", error)
        raise SystemExit(1)
