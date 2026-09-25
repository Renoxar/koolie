# Role Pack Requirements Engineering

| Attribut | Wert |
|---|---|
| Modul-ID | RP-RE |
| Ebene | 6 – Role Pack |
| Version | 0.1.4 |
| Status | pilot |
| Owner | `<FRAMEWORK_OWNER>` (bis zur Benennung eines Modul-Owners) |
| Zielrolle | Requirements Engineering, Product Owner, fachlich zuarbeitende Entwicklung |
| Laufzeitfassung | `30-role-requirements-engineering.md` in der Regelablage |
| Skills | `role-re-ticket` (`RP-RE-SK-001`) |

## 1. Zweck und Abgrenzung

Dieses Pack konkretisiert das Arbeitsmodell für die **Formulierung von Anforderungen**: aus einer Absicht, einem Gesprächsergebnis oder einer Fehlermeldung eine prüfbare, umsetzungsreife Aufgabenbeschreibung machen — mit Anforderungen in EARS-Syntax, abgeleiteten Arbeitspaketen, überprüfbaren Abnahmekriterien und einer verständlichen Änderungsmitteilung.

Der Unterschied zu einer reinen Textarbeit ist der **Einbezug der Codebasis**: Bevor eine Anforderung formuliert wird, wird geprüft, was es schon gibt, welche Begriffe der Code verwendet und welche Randbedingungen sich aus Datenmodell und Schnittstellenvertrag ergeben. Eine Anforderung, die eine bereits vorhandene Funktion beschreibt oder gegen ein Schema arbeitet, kostet im Verlauf mehr als die Recherche vorher.

**Nicht Gegenstand dieses Packs:**

| Nicht enthalten | Zuständig |
|---|---|
| Entscheidung, **ob** und **wann** etwas gebaut wird | `<PRODUCT_OWNER_ROLE>` |
| Priorisierung, Aufwandsschätzung, Terminzusagen | `<PRODUCT_OWNER_ROLE>`, Projektleitung |
| Architektur- und Technologieentscheidungen | `<ARCHITECT_ROLE>`, V3 der Delegationsverbotsliste |
| Risikobewertung und Kontrollstufenvorschlag einer Änderung | `fw-change-analyze` |
| Änderungsplan für die Umsetzung | `fw-plan` |
| Eintragen oder Ändern von Vorgängen im Ticketsystem | Mensch (V11: keine Außenkommunikation im Namen des Projekts) |

## 2. Der zentrale Grundsatz dieses Packs

> **Der Ist-Zustand ist keine Anforderung.**

Wer Code liest, während er Anforderungen formuliert, gerät in eine Falle: Aus „der Code antwortet mit 409" wird schnell „das System soll mit 409 antworten". Das ist keine Anforderung, sondern eine Beschreibung — und ob 409 fachlich richtig ist, hat niemand entschieden. Sobald so etwas als Anforderung in ein Ticket gerät, ist die Implementierung ihre eigene Spezifikation geworden und jede Prüfung zirkulär.

Dieses Pack trennt deshalb verbindlich drei Kategorien:

| Kategorie | Herkunft | Kennzeichnung | Formulierung |
|---|---|---|---|
| **Anforderung** | ausschließlich vom Menschen | EARS-Liste | `shall` |
| **Befund** | aus dem Code, mit Fundstelle | „Ist-Zustand: …" | Indikativ, nie `shall` |
| **Randbedingung** | aus Schema, Vertrag, Migration, durch Tests zugesichertem Verhalten, mit Fundstelle | „Randbedingung (belegt): …" | Indikativ, nie `shall` |

Ein Befund kann eine Anforderung **auslösen** — aber erst, nachdem ein Mensch entschieden hat, dass das Verhalten so bleiben oder sich ändern soll. Der Skill legt diese Entscheidung offen, statt sie stillschweigend zu treffen.

## 3. Typische Aufgaben mit Betriebsmodus und Kontrollstufe

| Aufgabe | Modus | Typische Kontrollstufe | Skill |
|---|---|---|---|
| Neue Anforderung aus einer Absicht formulieren | M1 | niedrig | `role-re-ticket` |
| Bestehende Aufgabenbeschreibung überarbeiten | M1 | niedrig | `role-re-ticket` |
| Fehlermeldung in eine Aufgabenbeschreibung überführen | M1 | niedrig–mittel | `role-re-ticket`, davor `fw-error-analyze` |
| Prüfen, was eine Anforderung technisch berührt | M1 | niedrig–mittel | `fw-change-analyze` |
| Codebasis für die Recherche kennenlernen | M1 | niedrig | `fw-repo-analyze` |
| Umsetzung planen | M2 | mittel | `fw-plan` |

Alle Aufgaben dieses Packs sind **M1 Read-only Analysis**: Der Skill liest und gibt Text aus. Er schreibt keine Datei und trägt nichts in ein Ticketsystem ein. Soll der Entwurf im Repository abgelegt werden, ist das ein eigener Schritt in M5 durch den Menschen.

## 4. Zusammenspiel mit den Framework-Skills

```text
Absicht, Gespräch, Fehlermeldung
        │
        ▼
  role-re-ticket ──── enge Recherche: Gibt es das schon? Welche Begriffe
        │             nutzt der Code? Welche Randbedingungen gelten?
        │             Ergebnis: Aufgabenbeschreibung mit EARS-Anforderungen
        ▼
  fw-change-analyze ── Vollanalyse: betroffene Komponenten, Verwender,
        │             Testlücken, Risiken R1–R13, Kontrollstufenvorschlag
        ▼
  fw-plan ─────────── Änderungsplan (M2)
        ▼
  fw-change-small / fw-tests / fw-refactor (M3/M4)
```

**Bewusste Aufgabenteilung:** `role-re-ticket` bewertet **kein** Risiko und schlägt **keine** Kontrollstufe vor. Das leistet `fw-change-analyze` mit ausgearbeiteter Faktorenliste. Zwei Skills, die dieselbe Codeanalyse mit unterschiedlicher Tiefe machen, liefern über die Zeit widersprüchliche Ergebnisse — deshalb recherchiert `role-re-ticket` nur so weit, wie es zum Formulieren nötig ist, und empfiehlt den Folge-Skill.

## 5. Werkzeug- und Sprachneutralität

Das Pack verdrahtet kein Ticketsystem und keine Sprache. Beides kommt aus dem Overlay:

| Wert | Quelle im Overlay | Wirkung |
|---|---|---|
| `<ISSUE_TRACKER>` | Abschnitt 13 | bestimmt die Auszeichnungssyntax der Ausgabe |
| Sprache von Bezeichnern, Kommentaren, Prosa | Abschnitt 9 | bestimmt, was in welcher Sprache formuliert wird |
| `<PROJECT_RULES_PATH>` | Abschnitt 9 | Fachbegriffe und Namenskonventionen |
| Glossar (Manifest-Typ `glossary`) | Abschnitt 19 | verbindliche Fachbegriffe |

Unterstützte Auszeichnungsformen: **JIRA-Wiki** (`h2.`, `||…||`, `#`-Listen), **Markdown** (`##`, Pipe-Tabellen) und **neutral** (Klartext mit Überschriftenzeilen). Ist `<ISSUE_TRACKER>` im Overlay nicht gesetzt oder unbekannt, fragt der Skill nach, statt eine Syntax zu unterstellen.

## 6. Anforderungssyntax: EARS

Funktionale Anforderungen werden nach **EARS** (Easy Approach to Requirements Syntax) formuliert. Die Muster:

| Muster | Form | Anwendung |
|---|---|---|
| Ubiquitär | `Das <System> shall <Verhalten>.` | dauerhaft geltendes Verhalten |
| Ereignisgetrieben | `When <Auslöser>, das <System> shall <Verhalten>.` | Reaktion auf ein Ereignis |
| Zustandsgetrieben | `While <Zustand>, das <System> shall <Verhalten>.` | Verhalten in einem Zustand |
| Unerwünschtes Verhalten | `If <Bedingung>, then das <System> shall <Verhalten>.` | Fehler- und Ausnahmefälle |
| Optionales Merkmal | `Where <Merkmal zutrifft>, das <System> shall <Verhalten>.` | konfigurierbare Funktionen |

**Regeln:**

1. Ein Hauptverhalten je Anforderung. Unabhängig prüfbare Verhalten werden getrennt.
2. Keine unbestimmten Wörter: *angemessen*, *geeignet*, *schnell*, *benutzerfreundlich*, *bei Bedarf*, *möglichst*, *gegebenenfalls* — es sei denn, das Overlay oder das Glossar definiert sie messbar.
3. EARS wird nicht auf rein technische Arbeitspakete gezwungen. Ein Arbeitspaket ist keine Anforderung.
4. Erfordert die EARS-Form eine Annahme, die die Anforderung inhaltlich verändert (ein erfundener Auslöser, ein erfundener Fehlerfall), wird **nachgefragt** statt formuliert.

## 7. Nachvollziehbarkeit

```text
Anforderung (was das System soll)
      │
      ▼
Arbeitspaket (was zu tun ist)
      │
      ▼
Abnahmekriterium (woran Fertigstellung erkennbar ist)
```

Jede Anforderung hat mindestens ein Arbeitspaket und mindestens ein Abnahmekriterium. Ein Abnahmekriterium ist keine wörtliche Kopie der Anforderung, sondern deren Umformulierung als **beobachtbares, abgeschlossenes Ergebnis**. Drei unterschiedlich formulierte Fassungen desselben Satzes sind ein Mangel, keine Nachvollziehbarkeit.

## 8. Umgang mit Kontext und Datenschutz

Aufgabenbeschreibungen und Ticketinhalte sind in der Regel **K2** (`.koolie/core/framework/core/02-privacy.md`): Sie werden je Aufgabe freigegeben und bereinigt übergeben. Für dieses Pack gilt zusätzlich:

1. In den Entwurf gelangen **keine** Personennamen, Kundennamen, Behördennamen, Kennungen, Adressen oder Zugangsdaten — auch nicht, wenn sie in der Eingabe stehen. Rollen statt Personen.
2. Beispieldaten im Entwurf sind synthetisch und als solche gekennzeichnet.
3. Findet der Skill in der Eingabe oder im Code K3-Inhalte, gibt er sie nicht wieder, nennt die Fundstelle und hält an.
4. Die projektlokale Sperrbegriffsliste (`.koolie/project-overlay/forbidden-terms.txt`) gilt auch für Entwürfe.

## 9. Aktivierung im Projekt

1. Rolle im Overlay Abschnitt 1 („Rollen im Team") aufführen.
2. Laufzeitfassung kopieren:
   `.koolie/core/framework/role-packs/requirements-engineering/runtime/30-role-requirements-engineering.md`
   → `30-role-requirements-engineering.md` in der Regelablage
3. Skill kopieren:
   `.koolie/core/framework/role-packs/requirements-engineering/skills/role-re-ticket/`
   → `role-re-ticket/` in der Skill-Ablage
3a. `python .koolie/core/install.py --update` ausführen – er bringt die kopierte Laufzeitfassung in die Form des installierten Client Packs. 🔴 **Ohne diesen Schritt steht dort die Quellform**, und ein Client mit eigener Bedingungssprache wertet Felder aus, die er für Regeldateien nicht kennt (`K-18`, gemessen 2026-09-21: zwei Validatorfehler).
3b. Den Skill in die **Berechtigungsdatei** eintragen – `<Werkzeug>(role-re-ticket)` nach `permission_tools.skill` des Client Packs. 🔴 **Ohne den Eintrag fällt der Aufruf in den Rückfragekorb und im rückfragefreien Betrieb in die Abweisung**; die Sitzung liest die `SKILL.md` dann ersatzweise als Datei, ohne die Werkzeugbeschränkung des Skills (D-81, D-238). **Prüfung 72** setzt es in beide Richtungen durch.
4. `<ISSUE_TRACKER>` im Overlay Abschnitt 13 setzen und die Sprachregeln in Abschnitt 9 prüfen.
5. Ein Glossar als Manifest-Typ `glossary` registrieren, falls vorhanden — der Skill nutzt es für verbindliche Fachbegriffe.
6. Validieren: `python .koolie/core/tests/scripts/validate-framework.py --strict-overlay`

Nicht aktivierte Packs liegen nur im Verzeichnis und werden vom KI-Client nicht als Regel geladen.

## 10. Änderungsverlauf

| Version | Datum | Änderung | Autor (Rolle) |
|---|---|---|---|
| 0.1.0 | 2026-09-09 | angelegt: Pack, Skill `role-re-ticket`, Laufzeitfassung | `<FRAMEWORK_OWNER>` |
| 0.1.2 | 2026-09-21 | Abschnitt 9: Die Aktivierung hat vier Schritte statt zwei – die kopierte Laufzeitfassung wird über `install.py --update` in die Form des Client Packs gebracht (3a), und der Skill gehört in die Berechtigungsdatei (3b). Beides gemessen am Messbaum von Bündel 5 (`CR-2026-115`, D-244; D-238) | `<FRAMEWORK_OWNER>` |
| 0.1.4 | 2026-09-25 | Abschnitt 2: Als Herkunft einer Randbedingung gilt auch durch Tests zugesichertes Verhalten, wie in `role-re-ticket` und der Laufzeitfassung (`CR-2026-147`, D-402, K-149) | `<FRAMEWORK_OWNER>` |
