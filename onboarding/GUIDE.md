# Onboarding-Leitfaden – Devin Desktop für neue Entwicklerinnen und Entwickler

| Attribut | Wert |
|---|---|
| ID | `FW-OB-GUIDE` |
| Version | `0.1.0` |
| Status | `entwurf` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Zielgruppe | neue Entwicklerinnen und Entwickler im Projekt `<PROJECT_NAME>`; Begleitung durch Mentorin oder Mentor |
| Begleitdokumente | `QUICKSTART.md`, `MENTOR_CHECKLIST.md`, `exercises/`, `KNOWLEDGE_CHECK.md`, `COMPLETION_CRITERIA.md`, `REFERENCE.md`, `checklists/09-onboarding.md` |

## Lernziele

Nach dem Onboarding kannst du:

1. Aufgaben daraufhin beurteilen, ob und wie sie mit Devin bearbeitet werden dürfen (Delegationsverbote, Kontrollstufen, Betriebsmodi),
2. Kontext bewusst auswählen und einstufen (K0–K3) und K2-Inhalte korrekt bereinigen,
3. den Standardarbeitsablauf mit Skills anwenden (Analyse → Plan → kleine Änderung → Test → Review),
4. Devin-Ergebnisse belastbar prüfen (Fundstellen, Testaussagekraft, API-Existenz) und über den regulären Prozess einbringen,
5. Stopp-Situationen erkennen und richtig eskalieren.

Maßstab ist souveräne Nutzung: **Aufgaben angemessen abgrenzen, Kontext kontrolliert bereitstellen, Ergebnisse belastbar prüfen** – nicht, möglichst viele Aufgaben zu delegieren. Wer eine Woche lang nur M1-Analysen fährt und dabei das Projekt versteht, nutzt Devin besser als jemand, der am ersten Tag ungeprüfte Diffs produziert.

## Voraussetzungen

- Zugang zu `<REPOSITORY_NAME>` und Devin Desktop; Grundkenntnisse in `<TECH_STACK>` und Git.
- Datenschutz- und Vertraulichkeitsunterweisung der Organisation absolviert (`<TBD: Referenz>`).
- Benannte Mentorin oder benannter Mentor; Übungsrepository eingerichtet (`exercises/README.md`).
- Gelesen: `QUICKSTART.md`, `AGENTS.md`, Overlay Abschnitte 1–6 und 13–16.

## Programmüberblick

| Modul | Inhalt | Form | Nachweis (`checklists/09-onboarding.md`) |
|---|---|---|---|
| 1 | Möglichkeiten und Grenzen | Lektüre + Gespräch | Verbotsliste an Beispielen eingeordnet |
| 2 | Datenschutz und Kontextauswahl | Übung Ü5 | Einstufungsübung fehlerfrei |
| 3 | Sichere Arbeitsweise | Lektüre + 2 begleitete Preflights | Preflights dokumentiert |
| 4 | Repository- und Framework-Struktur | Rundgang | Struktur erklärt bekommen und wiedergegeben |
| 5 | Skills und effektives Prompting | Übungen Ü1–Ü2 | Skills ausgeführt, Fundstellen geprüft |
| 6 | Analyse bestehender Komponenten | Übung Ü2, FW-PR-012 | Erklärstrecke absolviert |
| 7 | Ungefährliche Übungsaufgabe | Übungen Ü3–Ü4 | Plan + Änderung + Tests + Bericht |
| 8 | Test und Review | Übung Ü4 + Selbstreview | CL-04/CL-05 angewendet |
| 9 | Typische Fehlanwendungen | Katalog unten + Ü6 | Negativübungen bestanden |
| 10 | Abschluss | `KNOWLEDGE_CHECK.md`, `COMPLETION_CRITERIA.md` | Freigabe dokumentiert |

Reihenfolge ist verbindlich bis Modul 3; danach dürfen Module nach Absprache verschränkt werden. Bis zur Freigabe gilt: Devin nur in Begleitung oder auf dem Übungsrepository.

## Modul 1 – Möglichkeiten und Grenzen

Lies `framework/core/00-principles.md` (P1–P10) und `framework/core/09-risk-model.md` (Kontrollstufen, R1–R13, V1–V12). Besprich mit deiner Mentorin oder deinem Mentor drei reale, bereinigte Beispiele aus dem Projektalltag: Welche wäre delegierbar, in welchem Modus, auf welcher Stufe, welche nicht und warum. Kernbotschaften: Devin ist ein Werkzeug mit Werkzeuggrenzen – es halluziniert plausibel (nicht existierende APIs, erfundene Begründungen), es kennt keine Projektabsichten und es trägt keine Verantwortung. Deine Prüfung ist der Qualitätsmechanismus, nicht sein Selbstvertrauen.

## Modul 2 – Datenschutz und Kontextauswahl

Lies `framework/core/02-privacy.md` und arbeite `decision-trees/01-context-allowed.md` durch. Übe mit Ü5: zehn synthetische Schnipsel (Ticket mit Namen, Logauszug mit Adresse, `.env`-Fragment, Architekturauszug, Convention-Dokument …) korrekt einstufen und die K2-Bereinigung durchführen. Merksatz: **Ohne Einstufung gilt K3.** Alles, was du Devin gibst, verlässt deinen Arbeitsplatz (Anbieterverarbeitung) – die Klassen entscheiden, was das darf.

## Modul 3 – Sichere Arbeitsweise

Lies `framework/core/05-working-model.md` (14 Schritte, M1–M5) und `.devin/README.md` (Permission-Modi, Sitzungsfreigaben). Führe zwei Preflights (`checklists/01-preflight.md`) unter Begleitung durch – einen für eine Analyse-, einen für eine Änderungsaufgabe. Verinnerliche die Sitzungsdisziplin: eine Aufgabe je Sitzung, Modus Normal, Freigaben höchstens sitzungsweise, Ergebnisbericht am Ende.

## Modul 4 – Repository- und Framework-Struktur

Rundgang mit der Mentorin oder dem Mentor durch: `AGENTS.md` (Hierarchie der Anweisungen), `.devin/` (Regeln, Skills, Berechtigungen, Hooks), `framework/` (Core, Packs), `project-overlay/` (die einzige projektspezifische Ebene), `checklists/`, `decision-trees/`, `prompts/`. Verstehe die Prioritätshierarchie (acht Ebenen, Verschärfungsprinzip) und warum ein Projektwechsel nur das Overlay tauscht.

## Modul 5 – Nutzung von Skills und effektives Prompting

Lies `framework/core/06-prompting-rules.md` und `prompts/README.md`. Führe auf dem Übungsrepository aus: `/fw-repo-analyze` (Ü1), `/fw-code-explain` auf zwei Ebenen (Überblick, Detail). Regeln, die du dabei einübst: Skills vor freien Prompts; Pflichtelemente jeder Anweisung (Ziel, Modus, Stufe, Scope, Kontext, Akzeptanzkriterien); Fundstellen-Stichprobe nach jeder Antwort; unzulässige Muster erkennen („mach einfach", „behebe alles", „mach die Tests grün").

## Modul 6 – Analyse bestehender Komponenten

Wende `fw-code-explain` und die Schulungsvorlage `prompts/12-developer-training.md` auf eine echte, von der Mentorin oder dem Mentor gewählte Komponente des Projekts an (nur lesend, K1). Ergebnis: Du kannst den Ablauf der Komponente mit Fundstellen erklären und hast eine Fragenliste für das Mentorengespräch – Historie und Absichten beantwortet das Team, nicht Devin.

## Modul 7 – Bearbeitung einer ungefährlichen Übungsaufgabe

Auf dem Übungsrepository, Stufe niedrig, kompletter Durchlauf: Preflight → `/fw-change-analyze` → `/fw-plan` (Ü3) → Planbestätigung durch Mentorin oder Mentor → `/fw-change-small` → `/fw-tests` (Ü4) → Ergebnisbericht → Selbstreview (CL-04) → Übungs-Merge-Request mit Nutzungsvermerk (`fw-mr-description`). Ziel ist der Prozess, nicht die Änderung: kleine Schritte, Berichte, Halte-Punkte.

## Modul 8 – Test und Review

Vertiefe `checklists/04-review-ai-code.md` und `05-testing.md` an deiner Übungsänderung: Prüfe RV2 (stimmen die Fundstellen?), RV4 (prüfen die Tests Verhalten?), RV5 (existieren alle verwendeten APIs?). Tausche anschließend mit einer anderen Person die Übungs-Diffs und reviewt gegenseitig – mit `fw-review-support` als Zulieferung, nicht als Ersatz.

## Modul 9 – Typische Fehlanwendungen

| Fehlanwendung | Warum sie passiert | Was stattdessen gilt |
|---|---|---|
| Ungeprüfte Übernahme („sieht gut aus") | Zeitdruck, plausible Ausgabe | Q3: nur übernehmen, was du erklären kannst; Fundstellen-Stichprobe |
| Ganze Tickets oder Logs einfügen | Bequemlichkeit | Bereinigen (CL-02); nur Titel, Beschreibung, Akzeptanzkriterien |
| „Mach die Tests grün" | Frust über rote Pipeline | M4-Regeln: Ursache verstehen; Tests nie anpassen lassen |
| Scope-Aufweichung („räum bei der Gelegenheit auf") | Effizienzillusion | Q1/P7: ein Ziel je Änderung; Aufräumen als eigene Aufgabe |
| Sitzungs-Marathon über mehrere Aufgaben | Kontext „ist ja schon da" | Least Context: neue Aufgabe, neue Sitzung |
| Bypass/Smart aktivieren | „geht schneller" | D-05: untersagt; Normal bestätigt in Sekunden |
| Devin als Entscheidungsinstanz („was sollen wir nehmen?") | Autoritätsillusion | V3: Optionen ja, Entscheidung Mensch |
| Vertrauen auf Devins Selbstauskunft („bist du sicher?") | Anthropomorphisierung | Belege verlangen (Tests, Fundstellen), nicht Beteuerungen |

Bearbeite abschließend Ü6 (Negativübungen: Injektionsköder, K3-Köder, Scope-Falle) – bestanden ist, wer die Fallen erkennt und korrekt reagiert.

## Abschlusscheck und Freigabe

1. Selbsttest `KNOWLEDGE_CHECK.md` (Selbstkontrolle, keine Personalbeurteilung).
2. Gemeinsamer Durchgang der Kriterien in `COMPLETION_CRITERIA.md`.
3. Mentorin oder Mentor dokumentiert die Freigabe zur selbstständigen Nutzung (`checklists/09-onboarding.md`). Ohne Freigabe weiterhin nur begleitetes Arbeiten.

## Nachschlagewerk

`REFERENCE.md` fasst das Tagesgeschäft auf einer Seite zusammen (Klassen, Stufen, Modi, Skills, Stopp-Regeln, Wege). Halte es beim Arbeiten geöffnet, bis du es nicht mehr brauchst.
