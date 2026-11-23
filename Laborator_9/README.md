# Laboratorul 9 — Obiecte și clase

**Student:** Galușca Dumitru

**Grupa:** SI-266

Cele 8 sarcini modelează procesele și evenimentele Windows ca obiecte Python. Clasele `Proces`, `Eveniment` și `Inventar` permit identificarea constatărilor suspecte și construirea unui raport JSON.

## Fișiere

- `L9_TP_Galusca_Dumitru_SI-266.py` — lucrarea completată și verificatorul interactiv.
- `arsenal/windows/inventar.py` — clasele, funcțiile de încărcare și raportul.
- `arsenal/windows/start/` — capturile JSON folosite la analiză.
- `arsenal/windows/test_inventar.py` — verificarea raportului pe capturile incluse.

## Rulare

Din acest folder:

```powershell
python -m arsenal.windows.inventar arsenal/windows/start
python -m arsenal.windows.inventar arsenal/windows/start --json
python -m unittest arsenal.windows.test_inventar -v
```

Verificatorul interactiv pornește cu `python L9_TP_Galusca_Dumitru_SI-266.py`. Toate cele 8 sarcini trec. Capturile sunt date de exercițiu.
