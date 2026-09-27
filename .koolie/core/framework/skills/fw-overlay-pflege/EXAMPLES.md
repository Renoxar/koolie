# fw-overlay-pflege – Beispiele (erläuternd, nicht normativ)

Alle Beispiele sind **synthetisch**. Pfade, Rollen und Entscheidungen sind erfunden und bezeichnen kein reales Projekt.

## Positivbeispiel (synthetisch): eine Architekturentscheidung eintragen

**Vorher, im eigenen Terminal der Person:** `python .koolie/core/mandat.py erteilen --rolle Architekt --umfang dokumente --minuten 30 --anlass "ADR Bestellservice"`

**Aufruf:** `/fw-overlay-pflege eintrag "Als Architekt entscheide ich: Bestellungen ändert nur der Service; Alternativen waren direkter Repository-Zugriff und ein Ereignisbus."`

**Erwartetes Verhalten (Auszug, nach der Bestätigung im Folgeturn):**

```markdown
## Overlay-Pflege – fw-overlay-pflege v<Version aus dem Steckbrief>

### Anlass und Mandat
- Anlass: eintrag · Rolle: Architekt · Mandat: aktiv, Umfang dokumente, noch 24 Minuten

### Eingetragene Änderungen
| Datei | Abschnitt | Vorher → nachher | Quelle | berechtigungswirksam |
| documents/architecture/decisions/ADR-2026-09-27-bestellservice.md | neu | – → Kontext, Entscheidung, Alternativen (2), Folgen | Entscheidung Architekt, Sitzung | nein |
| overlay-manifest.yaml | documents | – → DOC-004 (architecture, K1, aktuell) | wie oben | nein |

### Offen gelassen
- Folgen für die Migration bestehender Direktzugriffe – `<TBD: Umstellungsplan>` – nicht besprochen

### Prüfung
- Validator --strict-overlay: 0 Fehler, 0 Warnungen

### Nächster Schritt für den Menschen
- `python .koolie/core/mandat.py beenden`
- Diff im Merge Request prüfen
```

## Negativbeispiel (synthetisch): ohne Mandat

**Aufruf:** `/fw-overlay-pflege eintrag "Trag die Testpfade test/** ein."`

**Erwartetes Verhalten:**

```text
Gesperrt: Schreiben in .koolie/project-overlay/ (kein Mandat).
Warum:    Overlay-Änderungen entscheidet der Mensch; eingetragen wird nur mit Mandat (M6).
Lösung:   Im eigenen Terminal: python .koolie/core/mandat.py erteilen --rolle <Rolle> --umfang overlay --minuten 60
Folge:    Danach trage ich `<TEST_PATHS>`: `test/**` in Abschnitt 4 ein; der Diff wird im Merge Request geprüft.
```

**Unzulässig wäre:** den Wert über die Shell schreiben, `mandat.py erteilen` selbst aufrufen oder eine Vorlage zum Abschreiben liefern, ohne den Weg zum Mandat zu nennen.
