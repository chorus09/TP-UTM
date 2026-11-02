# Laboratorul 7 — Colecții

**Student:** Galușca Dumitru

**Grupa:** SI-266

Cele 11 sarcini folosesc liste, tupluri, mulțimi și dicționare pentru a analiza capturi SUID, `sudo -l` și crontab. Se identifică fișierele SUID noi față de o instalare de referință și cele cu risc mare.

## Fișiere

- `L7_TP_Galusca_Dumitru_SI-266.py` — fișierul de laborator completat și verificatorul său interactiv.
- `arsenal/privesc/enum.py` — enumerarea constatărilor, în format de pachet Python.
- `arsenal/privesc/diferenta.py` — comparația SUID cu sistemul de referință.
- `arsenal/privesc/start/` — capturile folosite la analiză.
- `arsenal/privesc/enum.json` — raportul generat.
- `arsenal/privesc/test_diferenta.py` — verificarea diferenței pe capturile incluse.

## Rulare

Din acest folder:

```powershell
python -m arsenal.privesc.enum arsenal/privesc/start
python -m arsenal.privesc.diferenta
python -m unittest arsenal.privesc.test_diferenta -v
```

Verificatorul interactiv se pornește cu `python L7_TP_Galusca_Dumitru_SI-266.py`; toate cele 11 sarcini trec. Datele sunt capturi de laborator, nu rezultatul unei scanări pe sistemul local.
