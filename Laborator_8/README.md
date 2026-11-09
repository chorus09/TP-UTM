# Laboratorul 8 — Funcții și excepții

**Student:** Galușca Dumitru

**Grupa:** SI-266

Cele 8 sarcini analizează un jurnal `auth.log` de laborator: extrag autentificările eșuate, le numără pe adrese IP și identifică adresele care depășesc un prag configurabil.

## Fișiere

- `L8_TP_Galusca_Dumitru_SI-266.py` — lucrarea completată și verificatorul interactiv.
- `arsenal/aparare/parse_auth.py` — extragerea și numărarea autentificărilor eșuate.
- `arsenal/aparare/detector.py` — detectorul și raportul JSON.
- `arsenal/aparare/start/auth.log` — jurnalul inclus în laborator.
- `arsenal/aparare/test_detector.py` — verificări cu biblioteca standard Python.

## Rulare

Din acest folder:

```powershell
python -m arsenal.aparare.parse_auth arsenal/aparare/start/auth.log
python -m arsenal.aparare.detector arsenal/aparare/start/auth.log
python -m arsenal.aparare.detector arsenal/aparare/start/auth.log --prag 2 --json
python -m unittest arsenal.aparare.test_detector -v
```

Verificatorul interactiv pornește cu `python L8_TP_Galusca_Dumitru_SI-266.py`. Toate cele 8 sarcini trec. Jurnalul conține date de exercițiu, nu provine dintr-un sistem local.
