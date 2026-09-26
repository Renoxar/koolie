# Änderungsantrag `CR-2026-154`

| Feld | Inhalt |
|---|---|
| Titel | Öffentliche Verständlichkeit und Auffindbarkeit – der Einstieg, und der Spiegel, der schon veröffentlicht hatte |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-26 |
| Betroffene Artefakte | `README.md` (neu gegliedert), `README.en.md`, `QUICKSTART.md`, `QUICKSTART.en.md` (neu, Wurzel des Framework-Repositoriums); `.koolie/core/docs/DOCUMENTATION_STANDARD.md` (Abschnitt 5, `0.2.0`); `.koolie/core/tests/scripts/validate-framework.py` (`DOK_WURZEL`), `probe-pruefungen.py` (Sonden `D437`); `.koolie/core/build/doc/29-grenzen.md`; Register, Roadmap, Hauptdokument, CHANGELOG, `VERSION`, Bestandsliste |
| Ebene laut Entscheidungsbaum 6 | Dokumentation des Framework-Repositoriums und Prüfmittel; keine Regel, kein Client Pack, keine Laufzeitschicht |
| Art | **Änderung.** MINOR-Release ohne Kontingent – neue Dokumente, **ohne Overlay-Bruch**, das Verhalten des Frameworks bleibt unverändert |
| Dringlichkeit | regulär – eingeplant mit D-422 |
| Status | 🟢 **entschieden am 2026-09-26** (E1 bis E9) |

---

## 1. Anlass

Auftrag des Owners vom 2026-09-26 (D-422, `K-166`): Koolie soll für interessierte Entwickler, technische
Verantwortliche und Entwicklungsteams leichter auffindbar und verständlich werden. Eingegrenzt bei der Annahme
von `1.14.0` auf die Dokumentation im Repositorium, besonders die README, und eine englische Fassung von README
und Quickstart – die Punkte 1, 2 und, soweit die README sie braucht, 4 des Auftrags. Website, Fachartikel,
GitHub-Metadaten, Sichtbarkeit und Messplan bleiben ohne Ziel-Release (`K-166`). Der vollständige Auftragstext
liegt beim Owner, außerhalb des Repositoriums.

## 2. Die Vorprüfung

Ohne Kontingent, vor der Vorlage:

1. 🔴 **Der öffentliche GitHub-Spiegel besteht.** Das führende Gitea-Repositorium spiegelt bei jedem Push in ein öffentliches
   GitHub-Repositorium (Push-Spiegel seit 2026-09-26, Repositorium öffentlich seit 2026-09-24, letzter Abgleich
   beim Push von `v1.14.2`, ohne Fehler). GitHub trägt `main` und alle Marken, keine Releases. Beschreibung und
   20 Topics sind gesetzt – darunter `cursor`, für das es kein Pack gibt; die Beschreibung schreibt „ai client
   packs“. Der Plan für `1.17.0` sah vor, die Historie **vor** dem Spiegeln durchzusehen.
2. 🔴 **Die öffentliche Historie trägt Personenbezug:** 153 von 323 Commits nennen den Klarnamen als Autor, in
   zwei Schreibweisen; alle tragen die private Adresse; 41 die damals versionierte Übergabe. `K-108` fragte
   ausdrücklich **vor** dem ersten Publizieren.
3. **Die README:** kein anklickbarer Link, nur drei der vier Packs genannt (`kiro` fehlte seit `1.13.0`), die
   Namensmetapher als zweiter Abschnitt, Verzeichnistabelle und Wartungsdetails vor dem Nutzen.
4. **Einen Einstieg zum Ausprobieren gab es nicht.** `onboarding/QUICKSTART.md` ist für den ersten Arbeitstag
   in einem Projekt geschrieben, das Koolie schon nutzt – mit Platzhaltern und Mentorin.
5. **Der Reifegrad:** alle vier Packs stehen auf `pilot`; `openai-codex` mit zwei nicht abbildbaren Kernzusagen
   und Inbetriebnahme nur mit Freigabe. Ein Vokabular „verfügbar / experimentell“ kennt das Framework nicht.
6. **Die Prüfungen:** Prüfung 12 prüft Markdown-Links in jedem `.md` – ein Linkprüfer ist vorhanden.
   `dokumentklasse()` kannte außerhalb des Kerns nur `README.md`; ein `README.en.md` wäre für 92 und 93
   unsichtbar. Prüfung 92 ist eine deutsche Stammliste und für englischen Text wirkungslos. Die README speist
   das Hauptdokument nicht.

## 3. Befunde neben dem Auftrag

Der Auftrag verlangt, funktionale Fehler und widersprüchliche Zusagen getrennt festzuhalten, statt sie durch
Verhaltensänderungen zu lösen:

| # | Befund | Behandlung |
|---|---|---|
| B1 | Die README nannte drei Client Packs; `kiro` fehlte seit `1.13.0` | im Text berichtigt (D-438) |
| B2 | Die README sagte, `seed_paths` sei „in allen drei Manifesten“ leer – es sind vier, alle leer (Kaltleser-Probe) | im Text berichtigt |
| B3 | Die Veröffentlichung ist geschehen, bevor `K-108` beantwortet war | `K-108` fortgeschrieben, Entscheidung beim Owner (E7) |
| B4 | Das Topic `cursor` verspricht eine Integration ohne Pack | Korrektur durch den Owner (E6, D-439) |

Keine Aussage der Fähigkeitsmatrizen hat sich beim Schreiben als widersprüchlich erwiesen.

## 4. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | Sprache und Ort der Einstiegsdokumente | 🟢 **Deutsch maßgeblich**; `README.en.md` und `QUICKSTART.en.md`, wechselseitig verlinkt; ein **neuer** Quickstart zum Ausprobieren (`QUICKSTART.md`), alle in der Wurzel (D-437) | Die Wurzel trägt zwei Dokumente mehr |
| **E2** | Prüfungen für die neuen Dokumente | 🟢 **Klasse A** (`DOK_WURZEL`): 92 und 93 im Quellrepositorium, 94 ausgenommen wie die README, im Projekt ungeprüft; kein englischer Rechtschreibprüfer; Übersetzungsbedarf als Verfahrensschritt im Dokumentationsstandard (D-437) | Die Deckung der Fassungen prüft keine Maschine |
| **E3** | Der Aufbau der README | 🟢 **Sieben Fragen zuerst**, dann Name, Übernahme, Aufbau, Wartung; echte Links; kein Warnhinweis entfällt (D-438) | Die README wird länger |
| **E4** | Die Bezeichnung des Reifegrads | 🟢 **Der Status des Packs** (`pilot`) mit der wichtigsten Grenze; `openai-codex` mit Auflage, Cursor geplant; kein neues Vokabular (D-438) | Keine Abstufung unter den Pilot-Packs |
| **E5** | Das Beispiel | 🟢 **Die gemessene Push-Sperre von `claude-code`**, Verhalten aus dem Protokoll vom 2026-09-17, als beobachtet gekennzeichnet; die Einrichtung nachgefahren; keine neuen Läufe (D-438) | Der Beleg ist neun Tage und einige Clientstände alt |
| **E6** | Der GitHub-Spiegel und seine Metadaten | 🟢 **Bestand festhalten**, Gitea führend, Releases weiter mit `1.17.0`; `cursor` und die Schreibweise korrigiert der Owner von Hand (D-439) | Jeder Push ist sofort öffentlich |
| **E7** | Die öffentliche Historie | 🟢 **Nicht in diesem Release**; `K-108` fortgeschrieben, Empfehlung: nicht umschreiben (D-324) | Klarname und Adresse bleiben öffentlich |
| **E8** | Der Umfang | 🟢 **Punkte 1, 2 und 4**, soweit die README sie braucht; der Rest bei `K-166` | Website und Artikel warten |
| **E9** | Version und Befunde | 🟢 **MINOR `1.15.0`**; Befunde als Text berichtigt oder als Klärungspunkt, keine Verhaltensänderung | – |

## 5. Umsetzung

1. README neu gegliedert; `README.en.md`, `QUICKSTART.md`, `QUICKSTART.en.md` neu. Der Quickstart ist in einem
   Klon unter einem kurzen Pfad wörtlich nachgefahren: Installation, `.gitignore`, Commit, Validator 0/0,
   `--check-overlay-ready` mit den erwarteten offenen Werten. Ein Lauf unter einem langen Pfad hielt am
   Pfadwächter (D-368) an – daraus der Hinweis in Schritt 2.
2. `validate-framework.py`: `DOK_WURZEL`, Prüfung 94 nimmt die Einstiegsdokumente aus. Sonden `D437b` bis
   `D437d`, Gegenproben `D437a` und `D437e`. **Gegen den Vorstand:** Der Validator von `v1.14.2` meldet einen
   offenen Codeblock in `QUICKSTART.en.md` nicht (0 Fehler).
3. Dokumentationsstandard Abschnitt 5 (`0.2.0`); Kapitel 29 um die Grenze der Sprachfassungen ergänzt.
4. Kaltleser-Probe (D-379) an allen vier Einstiegsdokumenten – Fragen, Soll und Ergebnis im Protokoll
   `tests/protocols/2026-09-26-auffindbarkeit.md`.
5. Register, Roadmap (`0.4.8`), Hauptdokument, CHANGELOG, `VERSION`, Bestandsliste; Hebung beider Projekte und
   Bau der Erzeugnisse.

## 6. Entscheidung

🟢 **Angenommen am 2026-09-26.** Die Fragen wurden mit Empfehlung und Schätzung vorgelegt (ohne Kontingent, eine
Sitzung); der Owner hat sie ohne Änderung angenommen (*„Go 4 it“*).

| # | Entscheidung | Decision Record |
|---|---|---|
| E1, E2 | Sprachstrategie und Einstiegsdokumente der Wurzel | D-437 |
| E3, E4, E5 | Der Aufbau der README, der Reifegrad, das Beispiel | D-438 |
| E6, E7 | Der öffentliche Spiegel; die Historie als offene Frage | D-439, `K-108` |
| E8 | Umfang, der Rest bleibt vorgemerkt | `K-166` |
| E9 | Arbeitsweise, kein Regelinhalt | – |
