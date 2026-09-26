# Änderungsantrag `CR-2026-153`

| Feld | Inhalt |
|---|---|
| Titel | Die Attributionszeile im Commit-Vorschlag – und die Kurzform, die die ganze Einstellungsdatei verwirft |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-26 |
| Betroffene Artefakte | `.koolie/core/clients/claude-code/manifest.json` (`settings_extra`), `.koolie/core/clients/claude-code/CLIENT_PACK.md` (Abschnitt 8b, `0.24.5`); `.koolie/core/install.py`; `.koolie/core/tests/scripts/validate-output.py`, `probe-pruefungen.py`; `.koolie/core/framework/skills/fw-change-small/TESTS.md` (Zelle); `.koolie/core/build/doc/31-anhaenge.md` (`QC-7`); Register, Roadmap, Hauptdokument, CHANGELOG, `VERSION`, Bestandsliste |
| Ebene laut Entscheidungsbaum 6 | Client Pack (Einstellung), Installer und Prüfmittel |
| Art | **Änderung.** PATCH-Release nach D-431 – keine Anweisung eines Skills berührt, **ohne Overlay-Bruch** |
| Dringlichkeit | regulär – eingeplant mit D-431 |
| Status | 🟢 **entschieden am 2026-09-26** (E1 bis E9) |

---

## 1. Anlass

D-431 und `K-171`: Im Nachlauf von `1.14.1` trug `SK-005-P01` in Format und Verhalten, aber der Commit-Vorschlag
führte eine Zeile `Co-Authored-By` mit einer Adresse des Herstellers – nicht in jedem Lauf. Q5 verlangt eine
Nachricht, die das Warum beschreibt; der Vermerk der KI-Nutzung gehört in den Merge Request. Kriterium 2 von D-11
stand auf 1.

## 2. Die Vorprüfung

Ohne Kontingent:

1. **Die Herstellerreferenz** (`code.claude.com/docs/en/settings-reference.md`, Abschnitt „Git and attribution“,
   im Wortlaut gelesen, `QC-7`): Der Schlüssel heißt `attribution` – ein Objekt mit `commit` und `pr`
   (Zeichenketten, leer blendet aus) und `sessionUrl` (Boolean). `includeCoAuthoredBy` ist veraltet seit 2.0.62.
   🔴 **Die Kurzform `attribution: false` gibt es erst ab 2.1.281; ältere Stände verwerfen die ganze Datei, die
   sie enthält.** Die Zielspanne des Packs ist `2.1.x` – mit der Kurzform verlöre eine ältere Installation ihre
   Berechtigungen und Hooks.
2. **Der Wirkweg:** eine Anweisung des Clients an das Modell, keine Nachbearbeitung von `git commit`. Die Referenz
   gibt eigenen Anweisungen zur Attribution Vorrang (außer in verwalteten Einstellungen) – Q5 im Skill hat die
   Zeile trotzdem nicht verhindert.
3. **Ein Beobachtungspunkt ohne Modellurteil:** Jedes Sitzungstranskript trägt eine Anlage `remote_session_change`
   mit dem Feld `commit` – der vorgegebene Text. In allen 51 Transkripten von `1.14.1` steht dort der Trailer.
4. **Der Weg im Pack:** `settings_extra` im Manifest, wie `autoMemoryEnabled` (D-154); Prüfung 54 hält die Ebene.
   Die Messbäume entstehen aus einer frischen Installation und tragen den Schlüssel damit von selbst.
5. **Die Reichweite:** `install.py --update` fasst die Berechtigungsdatei nie an – ein neuer Schlüssel erreicht kein
   bestehendes Projekt, zum zweiten Mal nach D-154.
6. **Das Prüfmittel** fand den Trailer nur über die Adresse (`validate-output.py` Punkt 3).
7. **Die Fähigkeitsmatrix:** Ihre Zeilen stammen aus der Vorlage und gelten für alle vier Packs; das Vorbild für
   eine abgeschaltete Voreinstellung ist Abschnitt 8a des Packs.
8. **Das Framework-Repositorium selbst** trägt die Zeile in 169 von 321 Commits.

## 3. Die Messung

Fünf Sitzungsläufe mit dem Client Pack `claude-code` 2.1.283 (Opus 5.5), **3,28 USD** (vorgelegt: ~3,50 USD, hart 8
Läufe und 8 USD): zwei unabhängige Ketten von `SK-005-P01` zu je zwei Turns und ein Kontrolllauf ohne Skill, im
frischen Messbaum aus dem Messstand des Übungsrepositoriums. **In allen fünf Transkripten ist die Vorgabe leer;
beide Ketten tragen.** Einzelheiten im Protokoll (`tests/protocols/2026-09-26-attributionszeile.md`).

## 4. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | Was wird gesetzt? | 🟢 **`attribution` in Objektform**, `commit` leer, `sessionUrl` aus, `pr` unberührt (D-433) | Umständlicher als `false` – mit Absicht |
| **E2** | Schranke oder Standard? | 🟢 **Standard**, wie D-154 (D-433) | Ein Projekt kann die Zeile zurückholen |
| **E3** | Wo wird es belegt? | 🟢 **Abschnitt 8b des Packs**, Quelle `QC-7`, keine Matrixzeile (D-433) | Weicht vom Wortlaut von `K-171` ab |
| **E4** | Bestehende Projekte | 🟢 **Hand-Nachtrag und Migrationshinweis; `install.py --update` meldet fehlende Zusatzschlüssel**, Sonden `D434`/`D434a` (D-434) | Der Mensch trägt weiter nach |
| **E5** | Das Prüfmittel | 🟢 **Q5-Prüfung im Commit-Abschnitt**, Selbstproben Q1 bis Q5 (D-435) | – |
| **E6** | Q5 im Regeltext schärfen? | 🟢 **Nein**; die übrigen Packs als `K-173` | Ohne Einstellung trägt dort nur die Regel |
| **E7** | Kosten und Wartbarkeit des Messapparats (Frage des Owners bei der Vorlage) | 🟢 **`1.18.0` nach `1.17.0`** (`K-174`, D-436); zwei kostenlose Hebel sofort | Ein Release mehr im Plan |
| **E8** | Der Nachlauf | 🟢 **Zwei Ketten `SK-005-P01` und eine Kontrolle**, Nachweis an der Vorgabe im Transkript, Abbruch statt Rückfall bei fehlendem Prompt | 5 Läufe, ~3,50 USD |
| **E9** | Die eigenen Commits des Framework-Repositoriums | 🟢 **Ab `1.14.2` ohne Trailer**; die Historie bleibt | – |

## 5. Umsetzung

1. Manifest `settings_extra.attribution` mit Begründung; Client Pack Abschnitt 8b und Änderungsverlauf (`0.24.5`); Quelle `QC-7` im Anhang.
2. `install.py`: `fehlende_zusatzschluessel()` und der Hinweis nach `--update`; Sonden `D433`, `D434`, Gegenprobe `D434a`.
3. `validate-output.py` Punkt 5: `ki_vermerke_im_commit()`; Selbstproben Q1 bis Q5. Alle Sonden fallen gegen `v1.14.1`.
4. Nachlauf `SK-005-P01`; Zelle eingetragen.
5. Register, Roadmap (`1.18.0`), Hauptdokument, CHANGELOG, `VERSION`, Bestandsliste; Hebung beider Projekte (im Pilot die Einstellung von Hand nachgetragen) und Bau der Erzeugnisse.

## 6. Entscheidung

🟢 **Angenommen am 2026-09-26.** Der Owner hatte vorab festgelegt, dass seinen Empfehlungen gefolgt wird (*„Gehe davon
aus, dass ich deinen Empfehlungen folge“*); bei der Vorlage fragte er nach Kosten und Wartbarkeit der Testläufe und
gab den Auftrag, das nach den geplanten Releases einzuplanen – daraus E7.

| # | Entscheidung | Decision Record |
|---|---|---|
| E1, E2, E3, E6, E8 | Die Attributionsvorgabe abgeschaltet und gemessen | D-433 |
| E4 | Die Meldung fehlender Zusatzschlüssel | D-434 |
| E5 | Q5 im Prüfmittel | D-435 |
| E7 | `1.18.0` | D-436 |
| E9 | Arbeitsweise, kein Regelinhalt | – |
