# Gegenprüfung zu B08 und B11: die Aktivierung, die sich selbst voraussetzt, und die Ausnahme ohne Mechanismus

| Feld | Wert |
|---|---|
| Gegenstand | **B08** – die Aktivierungsprüfung und der Status-Hook. **B11** – das generelle Netzverbot und die zugesagten Ausnahmen je Domain |
| Anlass | Die Befunde **B08** und **B11** des unabhängigen Reviews vom 2026-09-12, beide P2 und beide ungeprüft. Nach D-23 und dem Arbeitsplan gehört jeder Befund vor der Umsetzung gegengeprüft |
| Datum | 2026-09-13 |
| Framework-Version | 0.32.0 (Auscheckstand `a950c35`, Arbeitsbaum sauber) |
| Prüfmethode | **Code- und Dokumentenprüfung, dazu zwei erzeugte Installationen.** Jede Fundstelle nachgelesen; `check_strict_overlay` und `hook-overlay-status.py` Zeile für Zeile; die Namensliste des Validators durchgerechnet; die erzeugte Berechtigungsdatei beider Packs an frischen Installationen nachgesehen; die Fachmatrizen ausgezählt |
| Umgebung | Windows 11, Python 3.14.4 |
| Ergebnis | **Beide Befunde bestätigen sich vollständig.** Dazu **fünf eigene Feststellungen**, von denen zwei den Zuschnitt der Umsetzung verändert haben, und ein Nebenbefund, der beim Einfügen einer Matrixzeile auffiel |

## 1. B08 – die Aktivierung verlangt, was sie herstellen soll

### 1.1 Die Zirkularität ist dreifach verankert

| Stelle | Aussage | Ergebnis |
|---|---|---|
| `docs/ADOPTION_GUIDE.md` Schritt 7 | fährt `validate-framework.py --strict-overlay` | **bestätigt** |
| `docs/ADOPTION_GUIDE.md` Schritt 9 | setzt den Status **danach** auf `aktiv` | **bestätigt** |
| `checklists/10-project-adoption.md`, Kopfzeile „Wann“ | „bei Übernahme …, **vor dem Setzen des Overlay-Status auf `aktiv`**“ | **bestätigt** |
| ebenda, MUSS-Punkt | „`validate-framework.py --strict-overlay` läuft ohne Fehler“ | **bestätigt** |
| `templates/project-overlay/OVERLAY.md` Abschnitt 21 | Status wird `aktiv`, **wenn** Checkliste **und** Lauf durch sind | **bestätigt** |
| `check_strict_overlay` | vergleicht **exakt** auf `aktiv`, in beiden Trägern | **bestätigt** |

Der Vergleich ist seit 0.28.0 eine Aufzählung statt eines Präfixvergleichs, weil
`aktivierung-ausstehend` vorher bestand (D-44). Damit ist die Lage eindeutig: **Wer den
dokumentierten Ablauf befolgt, setzt `aktiv`, bevor die Übernahmecheckliste fertig ist** – und ein
Agent arbeitet dann regelkonform in M3 auf einem unfertigen Overlay. Das Review nennt es „zirkulär,
solange keine Prüfung eines Aktivierungskandidaten vorgesehen ist“; das trifft.

### 1.2 Eigene Feststellung 1: Der Name der fehlenden Prüfung steht längst da

| Stelle | Wortlaut |
|---|---|
| `docs/ADOPTION_GUIDE.md:145` | „Der erste Lauf prüft Struktur, Inhalte und **Aktivierungsreife** des Overlays.“ |
| `validate-framework.py`, Docstring von `check_strict_overlay` | „**Aktivierungsreife** des Projekts (--strict-overlay) – clientneutral.“ |

**Beide beschreiben eine Kandidatenprüfung. Die Umsetzung verlangt den fertigen Zustand.** Es fehlt
kein Begriff, es fehlt die Prüfung dazu.

Das hat den Zuschnitt der Umsetzung verschoben: Nicht ein neues Konzept wird eingeführt, sondern
eine Prüfung gebaut, die zwei Dokumente seit je beschreiben. Und es entschied die Frage, **welcher**
Schalter der neue sein soll: Der Name „Aktivierungsreife“ passt auf den Kandidaten, aber
`--strict-overlay` hat mit dem Aktualisierungsablauf (`ADOPTION_GUIDE.md` Abschnitt 3, Schritt 4)
einen **zweiten, funktionierenden Aufrufer**, der ein bereits aktives Overlay prüft. Ihn umzudeuten
hätte jeder bestehenden Projekt-CI stillschweigend eine andere Prüfung gegeben.

### 1.3 Eigene Feststellung 2: Der Status-Hook trägt drei Defekte, nicht zwei

Das Review nennt zwei. Am Skript (Stand 0.32.0) nachgelesen sind es drei:

| Nr. | Zeile | Code | Folge |
|---|---|---|---|
| 1 | `:54` | `if value.startswith("aktiv"):` | **Präfixvergleich.** `aktivierung-ausstehend` wird als `aktiv` gemeldet – der Wert, der wörtlich sagt, dass die Aktivierung aussteht. **Das Review nennt diesen Defekt nicht** |
| 2 | `:51` | `re.search(r"Overlay-Status:\s*…")` | Verlangt einen Doppelpunkt. Die Steckbriefzeile `\| Overlay-Status \| … \|` trägt keinen – sie wird **nie** getroffen |
| 3 | `:60` | `break` | Die erste Datei mit Treffer entscheidet; eine aktive Laufzeitregel gewinnt gegen ein inaktives Quell-Overlay |

**Defekt 1 ist wörtlich derselbe, den D-44 im Validator behoben hat.** Die gemeinsame Auswertung
`_overlay_status_angaben` liegt seit 0.28.0 im Validator; der Hook benutzt sie nicht. Das ist das
Muster von D-49: Die Lehre war gezogen, aber nur in der Nachbarfunktion.

Die Reproduktion des Reviews bestätigt sich aus den Defekten 2 und 3: Tabellenstatus `inaktiv` ohne
lesbare Laufzeitregel → `unbekannt` (Defekt 2); aktive Laufzeitregel plus inaktiver Quellstatus →
`aktiv` (Defekt 3).

## 2. B11 – die Ausnahme ohne Mechanismus

### 2.1 Eigene Feststellung 3: Die Widerlegung steht fünf Zeilen unter der Zusage

`framework/core/03-security.md`, Abschnitt 4:

| Zeile | Text |
|---|---|
| 54 | „`Fetch(*)` \| deny; **Ausnahmen je Domain im Overlay**“ |
| 57 | „Regeln aus höheren Ebenen haben Vorrang, **`deny` gewinnt immer** `[DOK]`.“ |
| 59 | „Der Grund ist mechanisch: In der Berechtigungsdatei gewinnt `deny` immer, und **keine der abgebildeten Clientformen kennt ein Ausnahmemuster innerhalb eines deny**.“ |

**Zeile 59 buchstabiert das Argument aus, das Zeile 54 widerlegt** – geschrieben für das
Kernverzeichnis, zu einem anderen Zweck. Der Befund war im eigenen Dokument vorweggenommen.

### 2.2 Eigene Feststellung 4: Fünf Träger, keine Matrixzeile

Ausgezählt über das Repositorium – fünf Stellen versprechen die Freigabe je Domain:
`framework/core/03-security.md:54`, `framework/core/02-privacy.md` Regel 3.7 (dort mit `[DOK]`),
`framework/runtime/rules/10-privacy-security.md:31`, `checklists/02-privacy-context.md:39`,
`templates/project-overlay/OVERLAY.md` Abschnitt 11.

Eine sechste Stelle nennt einen **anderen** Mechanismus: `framework/core/02-privacy.md` Abschnitt 6
führt „Sandbox-Modus mit Domain-Allowlist“ – unter Windows laut Dokumentation nicht verfügbar. Das
ist keine Berechtigungsregel und löst die Zusage nicht ein.

**Keine Fähigkeitsmatrix führt eine Zeile zur zugesagten Ausnahme.** B8 deckt das *Verbot* ab und
steht bei beiden Packs für die Abrufwerkzeuge auf `[TECHNISCH]`. Dieselbe Bauform wie der Suchkanal
aus 0.30.0: **eine Zusage, die keine Schicht kennt.**

### 2.3 Eigene Feststellung 5: Bei einem Pack ist sie nicht ausdrückbar

`clients/claude-code/manifest.json` führt `WebFetch` und `WebSearch` in `permission_tools_bare`.
An einer frischen Installation nachgesehen:

```
$ python leitwerk-core/install.py --client claude-code --root <leer>
$ python -c "…" .claude/settings.json
deny:  ['WebFetch', 'WebSearch']
ask:   ['mcp__*']
allow: []
```

**Das ganze Werkzeug, ohne Argument.** Eine Domain-Angabe ist nicht ausdrückbar. Zum Vergleich
`devin-desktop`: `permission_tools_bare` enthält nur `mcp__*`, die erzeugte Datei trägt
`deny: ['Fetch(*)']` – dort **überlebt** ein Muster das Rendern; ob der Client eine Domain-Angabe
auswertet, ist unbelegt.

Dazu: `permission_tools.fetch` führt bei `claude-code` beide Werkzeuge zusammen. **Für eine
Websuche gibt es überhaupt kein Domain-Ziel** – auch ein künftiger Mechanismus könnte sie nicht
abdecken.

Das Verwerfen ist im Manifest deklariert und für sich richtig. Unbenannt blieb die **Folge** –
wörtlich dasselbe Muster wie B01 bei `permissions` in `drop_fields` (D-50), über einen anderen
Mechanismus.

### 2.4 Der Validator entschied dieselbe Absicht je Pack verschieden

`check_config` führte die Liste `("Exec(git push", …, "Fetch(*", …, "WebFetch", "WebSearch")` und
prüfte mit `rule.startswith(verboten)`. Durchgerechnet:

| Regel in `allow` | Ergebnis bis 0.32.0 |
|---|---|
| `Fetch(*)` | abgelehnt |
| `Fetch(domain:docs.example.invalid)` | **zulässig** |
| `WebFetch(domain:docs.example.invalid)` | abgelehnt |
| `WebSearch` | abgelehnt |

**Dieselbe Absicht, zwei Packs, zwei Entscheidungen.** Niemand hat das entschieden; es ist eine
Nebenwirkung fest verdrahteter Namen – derselbe Fehlertyp wie B02 und B10.

## 3. Nebenbefund beim Einfügen der Matrixzeile: Die Summen überzeichnen

Die neue Zeile **B10** musste in die Fachmatrix und damit in die Summen von Abschnitt 3. Dabei
zeigte sich:

| Angabe bis 0.32.0 (`claude-code`) | Ausgezählt |
|---|---|
| `[TECHNISCH]` 25 von 29 | **20** von 30 |
| `[TEXTUELL]` 3 von 29 (R5, R6, B9) | **7** von 30 (dazu B3, B4, B5, B8) |
| `[NICHT ABBILDBAR]` 1 von 29 (S5) | **3** von 30 (S3, S5, B10) |

Zwei Ursachen: **S3 steht seit 0.31.0 auf `[NICHT ABBILDBAR]`** (`CR-2026-050`), ohne dass die
Summen nachgezogen wurden. Und die vier Zeilen mit einer Kanalgrenze – B3, B4, B5, B8 – zählten als
`[TECHNISCH]`, obwohl D-47 sie je Kanal ausweist und ihr Shell-Teil nur als Anweisung trägt.

**Die Überschrift desselben Abschnitts sagte „Alle sechs Kernzusagen sind technisch abgebildet“** –
seit 0.30.0 zu weit gefasst: B3, B4 und B5 gelten nur für den direkten Zugriff.

**Es ist der dritte Drift dieser Summen.** Das Pack `devin-desktop` dokumentiert einen früheren
selbst: „Die Zeilenzahl ist mit 0.26.0 nachgezählt worden – sie stimmte vorher nicht.“ Eine Zahl,
die dreimal von Hand stimmen musste, gehört ausgerechnet (**Prüfung 31**, D-60).

## 4. Was diese Gegenprüfung nicht belegt

- **Sie belegt nicht, dass ein Client eine Domain-Angabe auswertet oder nicht.** Für
  `devin-desktop` ist die Form ausdrückbar und ihre Wirkung **unerhoben**; die Matrixzeile B10
  trägt deshalb `[TEXTUELL]` mit VERIFY-Marker. Widerlegt ist nur, dass sie **gegen ein bestehendes
  `deny`** wirken könnte – das ist Mechanik, nicht Messung.
- **Sie belegt keine Sitzung.** Ob ein KI-Client den Status-Hinweis des Hooks befolgt und
  tatsächlich in M1 bleibt, ist nicht gemessen. Der Hook informiert; er blockiert nie.
- **Sie belegt die Zirkularität nicht durch einen vollständigen Übernahmelauf.** Belegt ist, dass
  `check_strict_overlay` exakt `aktiv` verlangt und dass fünf Textstellen die Reihenfolge
  andersherum vorschreiben. Ein realer Übernahmelauf in ein fremdes Projekt ist **nicht** gefahren.
- **Die Auszählung der Matrix hängt an einer Zählregel**, und die ist eine Entscheidung, nicht ein
  Messwert. Sie steht seit 0.33.0 in beiden Packs und in Prüfung 31 an derselben Stelle: eine Zeile
  zählt bei ihrer schwächsten Einstufung.

## 5. Gegenzeichnung

| Rolle | Name/Kennung | Datum | Ergebnis bestätigt |
|---|---|---|---|
| `<FRAMEWORK_OWNER>` | `<TBD>` | `<TBD>` | `<TBD>` |
