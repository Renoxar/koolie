# Protokoll: Öffentliche Verständlichkeit und Auffindbarkeit – der Einstieg, und der Spiegel, der schon veröffentlicht hatte

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-26 |
| Release | `1.15.0` |
| Änderungsantrag | `CR-2026-154` |
| Art | Dokumentationsrelease mit einer Erweiterung des Validators – **keine Sitzung mit einem Client, kein Kontingent**; die Kaltleser-Probe lief mit vier kurzen Modellläufen |
| Gegenstand | `README.md`, `README.en.md`, `QUICKSTART.md`, `QUICKSTART.en.md`; `dokumentklasse()` und Prüfung 94 des Validators; der öffentliche Spiegel |
| Ergebnis | 🟢 **Entschieden, `D-437` bis `D-439`.** `K-108` und `K-166` fortgeschrieben. Die Kaltleser-Probe beantwortet alle 32 Fragen richtig; der Quickstart ist wörtlich nachgefahren; die Sonden `D437` fallen gegen den Vorstand |

---

## 1. Was gefragt war

Der Posten `1.15.0` (D-422): die README für interessierte Entwickler, technische Verantwortliche und
Entwicklungsteams, eine englische Fassung von README und Quickstart und belegbare Erklärungen, soweit die README
sie braucht. Die Entscheidungsfragen E1 bis E9 sind vorgelegt und ohne Änderung angenommen worden (*„Go 4 it“*).

## 2. Der Vorbedingungsdurchgang

| Messung | Ergebnis | Folge |
|---|---|---|
| Push-Spiegel des Gitea-Repositoriums (API) | aktiv seit 2026-09-26, Abgleich bei jedem Push, letzter beim Push von `v1.14.2`, ohne Fehler | D-439 |
| Öffentliches GitHub-Repositorium (API ohne Anmeldung) | öffentlich seit 2026-09-24; `main` und alle Marken, keine Releases; Beschreibung gesetzt, 20 Topics, darunter `cursor` | D-439, Korrektur durch den Owner |
| Historie | 323 Commits; 153 mit Klarnamen als Autor, alle mit privater Adresse, 41 mit der damals versionierten Übergabe | `K-108` fortgeschrieben |
| README | 0 anklickbare Links; 3 von 4 Packs genannt; Namensmetapher als zweiter Abschnitt | D-438 |
| Einstieg zum Ausprobieren | keiner – der Onboarding-Quickstart setzt eine Installation und eine Mentorin voraus | D-437 |
| `dokumentklasse()` | außerhalb des Kerns nur `README.md` | `DOK_WURZEL` (D-437) |

## 3. Der Quickstart, wörtlich nachgefahren

In einem Klon des Arbeitsstands unter einem kurzen Pfad, mit synthetischem Autor:

| Schritt | Ergebnis |
|---|---|
| 1 Übungs-Repository anlegen | Commit `Start` |
| 2 `install.py --target ../koolie-uebung --client claude-code` | installiert; die Zusammenfassung nennt die nächsten Schritte |
| 4 `grep -n "git push"` in `.claude/settings.json` | zwei Treffer: `permissions.deny` und `_core_rules_integrity.deny_must_contain` |
| 5 `.gitignore`, Commit, Validator | `Ergebnis: 0 Fehler, 0 Warnungen` |
| 6 `--check-overlay-ready` | 8 Fehler zu offenen `<TBD>`-Werten, wie beschrieben |

🔴 **Ein erster Lauf im Ablagebereich der Sitzung hielt an:** Der Installer meldete einen Pfad von 260 Zeichen und
kopierte nichts (D-368). Der Quickstart nennt den Fall seither in Schritt 2. Das Verhalten des Clients (Schritt 7)
ist nicht erneut gemessen; es stammt aus `2026-09-17-sitzungstest-schranken.md`, Abschnitte 3, 5 und 6.

## 4. Die Kaltleser-Probe (D-379)

Je Dokument eine frische Sitzung, die **nur** das eine Dokument lesen durfte und feste Fragen beantwortete – neun
zur README, sieben zum Quickstart, je Sprache. Das Soll ist vor den Läufen aus den Dokumenten geschrieben worden.

| Dokument | richtig | teilweise | falsch | Stolperstellen → Abhilfe |
|---|---|---|---|---|
| `README.md` | 9 | 0 | 0 | „drei der sechs Kernzusagen – Lese- und Schreibschutz“ ergab keine drei → die Datei-Sperren einzeln benannt; `[NICHT ABBILDBAR]` passte nicht zu den drei Arten von Regeln → Satz ergänzt; **„`seed_paths` in allen drei Manifesten“ war veraltet** (vier Packs) → berichtigt; zwei Quickstarts ohne Unterscheidung → Rollentabelle ergänzt; Kürzel K0–K3, M1–M5 und Ebenen erst im hinteren Teil erklärt → belassen, sie stehen in der Leitidee und im Aufbau |
| `README.en.md` | 9 | 0 | 0 | dieselbe Zählung der Kernzusagen; *delegation bans* unerklärt → erklärt; drei unidiomatische Wendungen → umformuliert |
| `QUICKSTART.md` | 7 | 0 | 0 | kürzerer Ort ohne Anleitung zum Ersetzen des Pfads → ergänzt; `python3` → Hinweis; Starter nur im Archiv und nur für Schritt 2 → gesagt; erwartete Fehlerzeilen nicht gezeigt → gezeigt; andere Packs ohne Dateinamen → Verweis auf das Laufzeitglossar |
| `QUICKSTART.en.md` | 7 | 0 | 0 | dieselben; dazu der Verzeichniswechsel in Schritt 5 und die deutschen Meldungen der Werkzeuge → beides gesagt |

**Kein *„falsch“*, kein *„teilweise“*.** Die Stolperstellen sind am Text behoben; die Probe ist danach nicht
wiederholt worden, weil keine Antwort vom Soll abwich.

## 5. Die Einstiegsdokumente im Validator (D-437)

| Probe | Ergebnis |
|---|---|
| Gegenbeweis gegen den Vorstand: Validator von `v1.14.2`, offener Codeblock in `QUICKSTART.en.md` | `0 Fehler, 0 Warnungen` – der Fehler wäre unbemerkt geblieben |
| Sonde `D437b`: derselbe Fall mit dem neuen Validator | gemeldet (Prüfung 93) |
| Sonde `D437c`: alte Schreibung in `QUICKSTART.md` | gemeldet (Prüfung 92) |
| Sonde `D437d`: zweite Hauptüberschrift in `README.en.md` | gemeldet (Prüfung 93) |
| Gegenprobe `D437a`: der ausgelieferte Stand ohne Steckbrief | läuft durch (Prüfung 94 nimmt aus) |
| Gegenprobe `D437e`: ohne Kennzeichen des Quellrepositoriums | ungeprüft – die Wurzel gehört dem Projekt (D-299) |

## 6. Abnahme

| Lauf | Ergebnis |
|---|---|
| Validator | 0 Fehler, 0 Warnungen, beide Kodierungsumgebungen |
| Sondenlauf | **356 Einheiten**, Exit 0, beide Umgebungen zeilengleich; neu: Sonden `D437b` bis `D437d`, Gegenproben `D437a` und `D437e`. Der erste Durchgang fiel in beiden Umgebungen an Gegenprobe `78a` – Kapitel 26 zählte die beiden neuen Kernträger noch nicht, nachgezogen auf 586 und 527 – und in der UTF-8-Umgebung einmal an Sonde `96d` (`kiro`), die im cp1252-Durchgang, einzeln und im Abnahmelauf bestand: ein Ausreißer der nebenläufigen Bahnen, in keinem Träger dieses Releases begründet |
| Pilot / Übungsrepo | beide gehoben und dort committet; an der Laufzeitschicht ändert sich nichts |

## 7. Was offen bleibt

`K-108` (Entscheidung des Owners über die öffentliche Historie); `K-166` (Website, Fachartikel, Sichtbarkeit,
Messplan); zwei Korrekturen der GitHub-Metadaten durch den Owner (D-439). Ohne Ziel-Release weiter: `K-165`,
`K-169`, `K-170`, `K-172`, `K-173`. Eingeplant: `1.16.0` Cursor, `1.17.0` Paketquellen, `1.18.0` (`K-174`).
