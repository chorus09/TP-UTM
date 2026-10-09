# Laborator: functii, metode si importuri pe web
# Student: Galusca Dumitru | SI-266
# Partea 5: exercitiile 44-50. Rulare: python main.py https://cybercor.org
from __future__ import annotations

import argparse
import csv
from datetime import datetime

import requests
import webtools  # ex. 44: importam modulul creat de noi
from webtools import get_title, security_headers, DEFAULT_HEADERS  # ex. 45 si 47

# Daca am defini aici o functie get_title(), am suprascrie in acest fisier
# numele importat mai sus si am apela functia noastra locala, nu cea importata.
BASE_URL = "https://cybercor.org"


def save_csv(url: str) -> None:
    """Ex. 49: salveaza statusurile cailor in CSV cu data verificarii."""
    paths = ["/", "/robots.txt", "/sitemap.xml"]
    results = webtools.check_paths(url, paths)
    with open("report.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["path", "status", "checked_at"])
        writer.writeheader()
        for path, status in results.items():
            writer.writerow({
                "path": path,
                "status": status if status is not None else "indisponibil",
                "checked_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            })
    print("Salvat in report.csv")


def main() -> None:
    """Ex. 48 si 50: primeste URL, scrie CSV si genereaza raport JSON."""
    parser = argparse.ArgumentParser(description="Laborator 4: raport HTTP despre cybercor.org")
    parser.add_argument("url", nargs="?", default=BASE_URL, help="URL-ul site-ului laboratorului")
    arguments = parser.parse_args()
    webtools.check_target(arguments.url)

    print("EX. 44 - Modulul webtools")
    print("Titlu:", webtools.get_title(webtools.fetch(arguments.url).text))
    print("EX. 45 - Importarea numelor")
    print("get_title():", get_title("<title>Test de import</title>"))
    print("security_headers():", security_headers(arguments.url))
    print("EX. 46 - Blocul __main__ se executa doar daca webtools.py este rulat direct")
    print("EX. 47 - Constanta importata:", DEFAULT_HEADERS)
    print("EX. 48 - Argument CLI:", arguments.url)

    print("EX. 49 - Generarea CSV")
    save_csv(arguments.url)
    print("EX. 50 - Raportul JSON si afisarea datelor reale")
    webtools.site_report(arguments.url)


if __name__ == "__main__":
    try:
        main()
    except (requests.RequestException, ValueError, OSError) as error:
        print("Nu s-a putut completa raportul. Verificati URL-ul si reteaua:", error)
        raise SystemExit(1)
