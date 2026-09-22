# Änderungsantrag `CR-2026-112`

| Feld | Inhalt |
|---|---|
| Titel | Der Arbeitsplatz im Kern – neun Werkzeuge trugen den Kontonamen einer Person, und ein Werkzeug wartete auf ein Datum |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-21 |
| Betroffene Artefakte | `tests/erhebungen/` (`ablage.py`, `baeume-b4.py`, `baeume_loeschen.py`, `cc-overlay-fuellen.py`, `dossier-b4.py`, `historie-bauen-b4.py`, `node-waechter.py`, `umgebungen-bauen-b4.py`, `zaehlen46.py`, `auswerten-b4.py`), `tests/scripts/validate-framework.py` (**Prüfung 71**), `tests/scripts/probe-pruefungen.py` (sechs Einheiten), `tests/TEST_CATALOG.md`, `tests/erhebungen/README.md`, `governance/DECISION_LOG.md` (**D-231**, **D-232** neu, **`K-85`** neu), `tests/protocols/2026-09-21-arbeitsplatz-im-kern.md` (neu), `docs/ROADMAP.md`, `CHANGELOG.md`, `VERSION`, `UEBERGABE.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind der Meßapparat und der Prüfapparat |
| Art | Befunde beim Bau der Dossiers des Nachlaufs – **kein Kontingent, kein Lauf am Client** |
| Dringlichkeit | **Regulär**, unmittelbar vor der Auswertung des Nachlaufs |

## 1. Anlass

Die Auswertung des Nachlaufs ist gefahren, und der nächste Befehl baut die Dossiers.
Er brach ab — und beim Blick auf die Abbruchstelle fiel der zweite, schwerere Befund
mit auf. **Beide kosteten nichts.**

### 🔴 Befund 1: Neun Werkzeuge des Kerns nennen einen Arbeitsplatz

`dossier-b4.py` führte in Zeile 33:

```python
KERN = os.path.join(r"C:\Users\<konto>\Documents\devpacks\leitwerk", "leitwerk-core")
```

Und es war nicht allein:

| Werkzeug | Wert |
|---|---|
| `baeume-b4.py`, `historie-bauen-b4.py`, `umgebungen-bauen-b4.py` | `UEB = …\devpacks\test-devin-framework` |
| `cc-overlay-fuellen.py` | `DD = …\devpacks\test-devin-framework` |
| `baeume_loeschen.py`, `node-waechter.py` | `QUELLE = …\devpacks\test-devin-framework\frontend\node_modules` |
| `zaehlen46.py` | `ROOT = …\devpacks\leitwerk` |
| `dossier-b4.py` | `KERN = …\devpacks\leitwerk\leitwerk-core` |
| `auswerten-b4.py` | derselbe Pfad im Kommentar |

**Der Pfad enthält den Kontonamen einer natürlichen Person.** Solange der Apparat
**neben** dem Repositorium lag, stand das in einer unversionierten Ablage. **Mit D-222
ist er hineingewandert und hat die Pfade mitgebracht** – in dasselbe Repositorium, für
das `0.78.1` eigens `UEBERGABE.local.md` eingeführt hat, weil eine Übergabe mit
Servername und Konto den Validator mit **drei Fehlern und drei Warnungen** beantwortet.

> *Wer einen Apparat umzieht, zieht seine Arbeitsplatzpfade mit um – und veröffentlicht
> sie, ohne es zu entscheiden.*

🔴 **Keine der siebzig Prüfungen sah es.** Prüfung 6 kennt Secret-Muster,
E-Mail-Adressen, IP-Adressen, interne Hostnamen und URLs außerhalb der Allowlist. **Ein
Pfad in ein Benutzerprofil ist nichts davon – und er trägt trotzdem den Namen eines
Menschen.**

### 🔴 Befund 2: Ein Werkzeug wartete auf ein Datum

```
ABBRUCH: …\belege\auswertung-2026-09-20.log fehlt - erst auswerten-b4.py
```

**Die Auswertung war gefahren** – nur eben am 21. Der Dateiname stand als Zeichenkette
im Quelltext von `dossier-b4.py`. Das ist die Bauform von **D-225** (drei
`--erwarte`-Sollwerte, keiner stimmte) und **D-153** (*eine Zahl, die gepflegt werden
muß, wird nicht gepflegt*), diesmal als **Datum**.

> *Ein Werkzeug, das die Ausgabe eines anderen beim Namen nennt, wartet auf den Tag, an
> dem jemand diesen Namen anders wählt.*

## 2. Was gemessen wurde, bevor entschieden wurde

- **Der Bestand vor dem Eingriff, über den ganzen Kern:** **18 Träger** nennen ein
  Benutzerprofil mit einem Kontonamen – **acht Werkzeuge** (dazu ein Kommentar) und
  **zehn Aufzeichnungen** (acht Protokolle, zwei Änderungsanträge).
- **Der Bestand danach:** **null Werkzeuge**, zehn Aufzeichnungen. Die Aufzeichnungen
  bleiben unangetastet und sind als **`K-85`** geführt.
- 🟢 **Prüfung 70 hat ihren ersten echten Fang gemacht – am Eingriff dieses Antrags
  selbst.** Die Umstellung ließ in drei Werkzeugen (`zaehlen46.py`,
  `baeume_loeschen.py`, `cc-overlay-fuellen.py`) den Aufruf `ablage.…` stehen, **ohne
  den Import**. Der Validator meldete drei `NameError`, **bevor ein Lauf sie fand** –
  genau der Fall, für den sie einen Tag zuvor entstanden ist.
- **Die drei Sonden und die drei Gegenproben zu Prüfung 71** laufen (`71a` bis `71c`).
  Gegenprobe `71c` belegt die angesagte Grenze: Eine Aufzeichnung bleibt unbeanstandet.
- **Die berichtigten Werkzeuge sind gefahren:** `zaehlen46.py` (Summe 32, unverändert),
  `node-waechter.py zaehlen` (9797 Dateien), `dossier-b4.py` (**19 Dossiers, jede Zelle
  mit Blattzeile und Auswertungsblock**).

## 3. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Wie kommt ein Werkzeug des Kerns an einen Pfad außerhalb des Kerns?** | **Gesagt oder abgeleitet, nie im Quelltext.** Das Übungsrepositorium wird **gesagt** (`LW_UEBUNG`, `ablage.uebungsrepositorium()`) – dieselbe Form wie `LW_ERHEBUNG` (D-224). Das Repositorium selbst wird **abgeleitet** (`ablage.WURZEL`). **Prüfung 71** meldet jeden absoluten Pfad in ein Benutzerprofil, dessen Kontosegment kein Platzhalter ist und dessen Zeile keine Begründung trägt | **Verworfen: ein Standardwert im Quelltext** – das wäre wieder ein Arbeitsplatz, nur ein anderer. **Verworfen: den Pfad abzuleiten** (etwa als Geschwister des Repositoriums) – das Übungsrepositorium muß nicht daneben liegen, und eine Ableitung, die meistens stimmt, ist schlechter als eine Angabe, die immer stimmt. **Verworfen: die Prüfung auf `.py` zu beschränken** – ein Arbeitsplatzpfad in einer Checkliste wäre derselbe Befund; Sonde `71b` fährt genau das. **Preis, benannt:** Fünf Werkzeuge brauchen ab sofort `LW_UEBUNG`; wer sie vergißt, bekommt einen Abbruch statt eines Laufs |
| **E2** | **Was wird aus den zehn Aufzeichnungen, die den Kontonamen weiter tragen?** | **Nichts – hier.** Prüfung 71 nimmt `tests/protocols/` und `governance/change-requests/` aus und **sagt es**; die Frage ist als **`K-85`** geführt | **Verworfen: sie mitzuberichtigen** – sie halten fest, **wo** gemessen wurde (*„außerhalb von `C:\Users\…`"*), und ein Protokoll, das man umschreibt, ist keines mehr (D-141). **Verworfen: sie stillschweigend auszunehmen** – dann entschiede der Zuschnitt einer Prüfung eine Datenschutzfrage, ohne daß jemand sie gestellt hätte. **Preis, benannt:** Der Kontoname steht weiter zehnmal im Quellrepositorium. `install.py` schreibt weder Protokolle noch Änderungsanträge in ein Projekt – die Reichweite endet an diesem Repositorium |
| **E3** | **Woher bekommt ein Werkzeug die Ausgabe eines anderen?** | **Es fährt sie selbst.** `dossier-b4.py` ruft `auswerten-b4.py` auf und legt dessen Protokoll mit dem Datum **dieses** Laufes neben die Belege | **Verworfen: die jüngste `auswertung-*.log` zu nehmen** – dann baut das Dossier stillschweigend aus einem alten Protokoll, wenn die Auswertung diesmal nicht lief; genau das sollte der Abbruch verhindern. **Verworfen: den Namen als Argument zu verlangen** – dann trägt ihn der Aufrufende, und die Wiederaufnahme hätte einen fünften Befehl. 🟢 **Nebenwirkung, gewollt:** Ein Dossier kann nicht mehr aus einer veralteten Auswertung entstehen. **Preis, benannt:** Jeder Dossierlauf fährt die Auswertung mit – kein Kontingent, wenige Sekunden |

## 4. Entscheidung

**E1 bis E3 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-21). Decision
Records **D-231** und **D-232**, **`K-85` neu**. **Kriterium 2 unverändert bei 32.**

## 5. Abnahme

- `validate-framework.py --root .`: **0 Fehler, 0 Warnungen**.
- `probe-pruefungen.py`: **voller Lauf in beiden Kodierungsumgebungen, 289 Einheiten, 416 Meldezeilen, keine ohne `OK`** – oberhalb der Trennlinie **zeilengleich** (345,0 s und 337,2 s), darunter die sechs neuen Einheiten zu Prüfung 71.
- `zaehlen46.py`: **Katalog 4 | Testblätter 28 | Summe 32** – unverändert.
- Protokoll: `leitwerk-core/tests/protocols/2026-09-21-arbeitsplatz-im-kern.md`.
- **Kein Lauf am Client, kein Kontingent verbraucht.**
