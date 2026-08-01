# Happy-Minus-Aktien: KGV-Analyzer

Ein automatisiertes Tool zur Identifizierung **unterbewerteter Aktien** basierend auf dem **Kurs-Gewinn-Verhältnis (KGV)**. Das Skript aktualisiert sich alle **10 Minuten** und speichert die Ergebnisse in einer CSV-Datei.

---

## 📌 Überblick

Dieses Projekt analysiert eine vordefinierte Liste von Aktien (DAX, MDAX, S&P 500) und filtert diejenigen heraus, die ein **KGV unter 15** aufweisen. Dies deutet darauf hin, dass die Aktie im Vergleich zu ihrem Gewinn potenziell unterbewertet ist und sich ein **Einstieg oder Neueinstieg** lohnen könnte.

### 🔍 Kriterien für unterbewertete Aktien
- **KGV < 15** (anpassbar in `kgv_analyzer.py`)
- **EPS (Gewinn pro Aktie) > 0.1** (um Aktien mit negativem Gewinn auszuschließen)
- **Dividendenrendite** (optional, wird mit ausgegeben)

---

## 🛠️ Voraussetzungen

- Python 3.8+
- GitHub-Konto (für die automatische Ausführung via GitHub Actions)
- Internetverbindung (für den Abruf der Aktiendaten)

---

## 📥 Installation

### 1. Repository klonen
```bash
git clone https://github.com/roruffm/Happy-Minus-Aktien.git
cd Happy-Minus-Aktien
```

### 2. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

---

## 🚀 Lokale Ausführung

Führe das Skript manuell aus:
```bash
python kgv_analyzer.py
```

Die Ergebnisse werden in **`unterbewertete_aktien.csv`** gespeichert.

---

## ⏰ Automatische Ausführung (alle 10 Minuten)

### Option 1: GitHub Actions (empfohlen)
Das Projekt enthält einen **GitHub Actions Workflow** (`.github/workflows/kgv_analyzer.yml`), der das Skript **alle 5 Minuten** automatisch ausführt (da GitHub Actions für kostenlose Konten keine 10-Minuten-Intervalle zulässt).

**Aktivierung:**
1. Der Workflow wird automatisch gestartet, sobald das Repository öffentlich ist.
2. Die Ergebnisse werden in der **`unterbewertete_aktien.csv`** im Repository aktualisiert.

### Option 2: Lokal mit `schedule`
Falls du das Skript lokal alle 10 Minuten ausführen möchtest, erstelle eine Datei `scheduler.py`:

```python
import schedule
import time
from kgv_analyzer import main

# Alle 10 Minuten ausführen
schedule.every(10).minutes.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
```

Führe es aus mit:
```bash
python scheduler.py
```

---

## 📊 Ausgabe

### Beispielausgabe (`unterbewertete_aktien.csv`)

| Ticker  | Name               | Kurs (€) | KGV  | EPS (€) | Dividendenrendite | Zeitstempel          |
|---------|--------------------|----------|------|---------|-------------------|----------------------|
| SAP.DE  | SAP SE             | 120.50   | 12.4 | 9.72    | 1.8%              | 2026-08-01 14:30:00 |
| BMW.DE  | Bayerische Motoren | 85.20    | 8.7  | 9.80    | 3.2%              | 2026-08-01 14:30:00 |
| BAS.DE  | BASF SE            | 50.10    | 10.2 | 4.91    | 4.5%              | 2026-08-01 14:30:00 |

---

## ⚙️ Anpassungen

### Aktienliste ändern
Bearbeite die Liste `TICKERS` in `kgv_analyzer.py`, um andere Aktien hinzuzufügen oder zu entfernen.

### KGV-Schwellenwert anpassen
Ändere die Variable `KGV_THRESHOLD` in `kgv_analyzer.py`:
```python
KGV_THRESHOLD = 15  # Standardwert
```

### Mindest-EPS anpassen
Ändere die Variable `MIN_EPS` in `kgv_analyzer.py`:
```python
MIN_EPS = 0.1  # Standardwert
```

---

## 📂 Projektstruktur

```
Happy-Minus-Aktien/
├── kgv_analyzer.py          # Hauptskript für die KGV-Analyse
├── requirements.txt         # Python-Abhängigkeiten
├── README.md                # Diese Datei
└── unterbewertete_aktien.csv  # Ausgabe (wird automatisch generiert)
```

---

## 🔄 Aktualisierungen

- **Aktienliste:** Die Liste der Aktien kann jederzeit in `kgv_analyzer.py` aktualisiert werden.
- **KGV-Schwellenwert:** Passe den Wert an, um strengere oder lockerere Filter zu setzen.
- **Datenquelle:** Derzeit wird **Yahoo Finance** verwendet. Falls eine andere API gewünscht ist (z. B. Alpha Vantage), kann das Skript angepasst werden.

---

## ❓ Häufige Fragen

### Warum wird eine Aktie nicht angezeigt?
- Die Aktie hat möglicherweise **kein KGV** (z. B. wenn der Gewinn negativ ist).
- Die Aktie hat ein **KGV ≥ 15**.
- Die Aktie ist nicht in der `TICKERS`-Liste enthalten.

### Wie füge ich neue Aktien hinzu?
Bearbeite die `TICKERS`-Liste in `kgv_analyzer.py` und füge die gewünschten Aktien-Symbole hinzu.

### Warum funktioniert die API nicht?
- Stelle sicher, dass du eine **stabile Internetverbindung** hast.
- Yahoo Finance blockiert manchmal Anfragen. In diesem Fall kannst du eine **Alternative API** (z. B. Alpha Vantage) verwenden.

---

## 📞 Kontakt

Falls du Fragen oder Anregungen hast, öffne ein **Issue** in diesem Repository oder kontaktiere den Autor.

---

**Hinweis:** Dies ist ein **automatisiertes Tool** und ersetzt keine professionelle Finanzberatung. Investitionen in Aktien bergen Risiken. Bitte informiere dich selbstständig, bevor du Investitionsentscheidungen triffst.