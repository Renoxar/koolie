# Protokoll: Freigabelauf `1.0.0` – die abgelegte Checkliste `FW-CL-11`

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-23 |
| Release | **`1.0.0`** (`AP12`) |
| Änderungsantrag | `CR-2026-128` |
| Art | **Freigabelauf.** Jeder Prüfpunkt der Checkliste `FW-CL-11` auf seinem gemessenen Stand |
| Gegenstand | `checklists/11-framework-release.md` Version `0.3.0`, **24 Prüfpunkte** – 22 MUSS, 2 SOLL |
| Ergebnis | 🟢 **20 von 24 gedeckt** – maschinell oder aus einem Beleg. 🔴 **Drei sind die Handlung eines Menschen** (9, 20 Schritt 1, 21), ⚪ **einer ist ein `SOLL` und wird ausgewiesen statt gefahren** (18) |

> 🔴 **KEIN PRÜFPUNKT IST HIER ABGEHAKT.** Was gemessen ist, steht mit seinem Meßwert da;
> was ein Mensch tun muß, steht als solches da. **Das Abhaken ist die Handlung des
> Menschen, und der Freigabe-Commit ist seine Unterschrift** (D-319, D-321).
> *Eine Checkliste, die sich selbst abhakt, ist keine.*

> ⚠️ **Die Vorbereitung vom `0.90.0` nannte „22 Prüfpunkte" und listete 23.** Gemessen
> sind es **24** – mit Prüfung 80 ist einer hinzugekommen, die Differenz davor war schon
> da (`CR-2026-128` B5). Dieses Protokoll ersetzt die Vorbereitung nicht; sie bleibt als
> Aufzeichnung ihres Standes stehen.

---

## 1. Inhalt und Konsistenz

| # | Prüfpunkt | Gewicht | Gemessener Stand |
|---|---|---|---|
| 1 | Änderungsanträge abgeschlossen oder ausdrücklich verschoben | MUSS | 🟢 **128 Anträge, keiner offen.** `CR-2026-127` (Rollenfrage) ist mit `0.91.0` entschieden, `CR-2026-128` mit diesem Release. Ausdrücklich **verschoben**: das Client Pack `openai-codex` auf `1.1.0` (D-124, D-127) |
| 2 | Konsistenz Core ↔ Laufzeitfassung je Client Pack | MUSS | 🟢 **Gedeckt, und der Grund ist gemessen: dieses Release ändert kein Core-Modul und keine Regelablage** – **16 Träger, davon 0 unter `framework/`**. Die Checkliste verlangt Stichproben *„je geändertem Modul"*; es gibt keines. **Maschinell:** Prüfungen 2, 4, 13, 21, 76 – Validator **0 Fehler, 0 Warnungen**. ⚠️ Die Stichprobe auf **Inhalte** ist Prüfpunkt 9 und davon zu trennen |
| 3 | Skills konsistent zum Skill-Standard | MUSS | 🟢 Prüfungen 5, 25, 47, 61, 64. **Dieses Release ändert keinen Skill** – gemessen an `git status`: 0 Träger unter `skills/` |
| 4 | Version je geänderter Checkliste und je geändertem Prompt gepflegt | MUSS | 🟢 Prüfung 13. **Geändert und gepflegt:** `RELEASE_PROCESS.md` `0.1.4` → `0.2.0` (neuer Abschnitt 4.1), `LICENSE-HINWEIS.md` `0.1.0` → `0.2.0`. **Keine Checkliste, kein Prompt berührt** |
| 5 | Prioritätshierarchie unverändert oder begründet | MUSS | 🟢 **Unverändert.** `PRIORITY_HIERARCHY.md` steht auf `0.2.1` und ist in diesem Release nicht angefaßt (gemessen an `git status`) |
| 6 | Templates, Checklisten, Entscheidungsbäume abgeglichen | SOLL | 🟢 **Kein Gegenstand:** Dieses Release ändert kein Modul, gegen das sie abzugleichen wären. Die einzige Regeländerung – Abschnitt 4.1 des Release-Prozesses – ist in `FW-CL-11` bereits als Prüfpunkt 20 abgebildet |

## 2. Projektneutralität

| # | Prüfpunkt | Gewicht | Gemessener Stand |
|---|---|---|---|
| 7 | `validate-framework.py` ohne Fehler, Warnungen bewertet | MUSS | 🟢 **0 Fehler, 0 Warnungen**, gemessen am fertigen Baum. **81 Prüfungen**. 🟢 **Und zusätzlich gegen BEIDE übernehmenden Projekte gefahren** (`--strict-overlay`) – dort fielen zwei strukturelle Befunde an Prüfung 78 und 79, beide mit D-326 behoben |
| 8 | `forbidden-terms.txt` im Release leer | MUSS | 🟢 **Gemessen: nur Kommentarzeilen, kein Begriff** |
| 9 | **Manuelle Stichprobe** auf projekt-, kunden- oder personenspezifische Inhalte | MUSS | 🟢 **DURCHGEFÜHRT – und sie hat geliefert.** Der Owner hat den **Klarnamen im Copyright-Vermerk als falsch geschrieben erkannt** (D-323, Nachtrag): Das Werkzeug hatte die Schreibweise aus dem Autorenfeld der Git-Historie abgeleitet, und **die führt ihn in allen 122 Merge-Commits falsch**. 🔴 **Keine der 81 Prüfungen konnte das sehen** – die Inhaltsprüfung kennt keinen Personennamen (`K-109`). ➡️ *Genau dafür verlangt die Checkliste die Stichprobe **zusätzlich** zur automatischen Prüfung, und hier hat der Satz seinen Beleg bekommen.* **Die sechzehn geänderten Träger liegen in Abschnitt 6 vor** |
| 10 | Beispiele synthetisch gekennzeichnet, Platzhalterregister aktuell | MUSS | 🟢 Prüfungen 7, 14, 50 |

## 3. Produktstand der KI-Client

| # | Prüfpunkt | Gewicht | Gemessener Stand |
|---|---|---|---|
| 11 | **Aktualitätsprüfung** gegen die offizielle Clientdokumentation | MUSS | 🟢 **Gefahren am 2026-09-18 als `FW-AK-01`** (`tests/protocols/2026-09-18-FW-AK-01.md`): **22 Quellen** (17 `QD`, 5 `QC`), **beide** Produkt-Changelogs – `devin-desktop` bis **3.10.31** (16.09.), `claude-code` bis **2.1.275** (17.09.). **Zwölf Quellen trugen ihren Beleg unverändert, zehn nicht; dreizehn Befunde, sämtlich als `CR-2026-087` erfaßt.** ⚠️ **Die Frist ist fünf Tage und sechs Releases** – der Prüfpunkt verlangt *„durchgeführt"*, nicht *„am Tag der Freigabe durchgeführt"*. Was danach kam, ist Produktbeobachtung nach `RELEASE_PROCESS.md` Abschnitt 6 |
| 12 | Produktänderungen mit Regelwirkung als Änderungsanträge behandelt | MUSS | 🟢 **`CR-2026-087` mit dreizehn Befunden**, vier davon als Klärungspunkte `K-62` bis `K-65`; `K-62` ist mit `0.85.0` geschlossen |

## 4. Tests

| # | Prüfpunkt | Gewicht | Gemessener Stand |
|---|---|---|---|
| 13 | Testkatalog vollständig ausgeführt | MUSS | 🟢 **125 Ergebniszellen** – 38 im zentralen Katalog, 87 in dreizehn Testblättern. Sechs Meßtage, zwei Nachläufe |
| 14 | **(ab 1.0.0)** Kein Testfall auf `offen` | MUSS | 🟢 **Kriterium 2 von D-11 = 0**, von Prüfung 46 ausgerechnet. Kette: `111 → … → 5 → 0`, erfüllt seit `0.84.0` |
| 15 | Skill-Testfälle für geänderte Skills erneut ausgeführt | MUSS | 🟢 **Kein Gegenstand: dieses Release ändert keinen Skill** |
| 16 | Hook- und Validierungsskripte laufen fehlerfrei | MUSS | 🟢 **Sondenlauf in beiden Kodierungsumgebungen, zweimal gefahren**: **322 angemeldete Einheiten**, **447 Ergebniszeilen**, **0 Unterschiede in 480 Zeilen** im zeilengleichen Vergleich nach D-49 – und der **vierte Durchgang zeilengleich zum dritten**. 🔴 **Eine Grenze, benannt:** Der letzte Handgriff an diesem Baum ist die **Freigabezeile in Abschnitt 7.1** – *der fertige Baum entsteht erst mit der Handlung des Menschen, und deshalb kann kein Werkzeug gegen ihn abnehmen.* Die Deckung ist ein Validatorlauf danach; **Prüfung 81** fängt dabei den Fall, der in dieser Sitzung zweimal eintrat |
| 17 | Jedes Abnahmeprotokoll trägt seine Gegenzeichnung | MUSS | 🟢 **Prüfung 80.** Zehn Abnahmeprotokolle, alle mit Abschnitt und ohne offenes `<TBD>`; **sieben davon ausdrücklich als Selbstgegenzeichnung ausgewiesen** (D-319) |
| 18 | Vollständiger Durchlauf `M1`→`M2`→`M3`→`M4` auf dem Übungsrepositorium | SOLL | ⚪ **NICHT GEFAHREN, und das steht hier statt zu fehlen.** Er braucht ein Sitzungskontingent – ein Modelllauf über vier Betriebsmodi. Er ist ein `SOLL`, kein `MUSS`. ➡️ *Ein nicht gefahrenes `SOLL` ist ein Meßwert, ein verschwiegenes ist ein Befund* |

## 5. Abschluß

| # | Prüfpunkt | Gewicht | Gemessener Stand |
|---|---|---|---|
| 19 | `VERSION` erhöht, `CHANGELOG.md` ergänzt | MUSS | 🟢 `VERSION` = **`1.0.0`**; `CHANGELOG.md` mit Änderungen, **Migrationshinweisen** (keine Overlay-Felder berührt; ⚠️ das **Versionierungsregime** ändert sich) und **bekannten Einschränkungen** |
| 20 | **Release-Archiv erzeugt und abgelegt; übernehmende Projekte informiert** | MUSS | 🔴 **Das Verfahren steht seit diesem Release** (`RELEASE_PROCESS.md` Abschnitt 4.1, D-321) – **bis `0.91.0` gab es keines, und `git tag` lieferte in 106 Release-Commits null.** 🔴 **Schritt 1, die signierte Marke, ist die Handlung des Menschen** und liegt als Befehl vor (Abschnitt 7). 🟢 **Übernehmende Projekte: beide auf `1.0.0` gehoben**, Bestandsliste in `governance/ADOPTION_REGISTRY.md` |
| 21 | **Freigabe des Releases durch den Framework Owner dokumentiert** | MUSS | 🔴 **BRAUCHT EINEN MENSCHEN. Nicht delegierbar** (`V1`, `V2`, `AGENTS.md` Abschnitt 16, D-319). Die Zeile in Abschnitt 7 ist vorbereitet und **leer**; der Freigabe-Commit ist die Unterschrift |
| 22 | **(ab 1.0.0)** Alle Core-Module, Skills und Packs über `entwurf` | MUSS | 🟢 **Kriterium 3 von D-11 = 0.** 81 Träger mit Steckbriefzeile, **77 auf `pilot`**, vier Ausfüllschlitze, **0 auf `entwurf`** |
| 23 | **(ab 1.0.0)** Kein Decision Record auf `entschieden (Vorschlag)` | MUSS | 🟢 **Kriterium 4 von D-11 = 0**, erfüllt seit `0.49.0`. **327 Decision Records** |
| 24 | **(ab 1.0.0)** Übernahme in mindestens ein zweites Projekt nachgewiesen | MUSS | 🟢 **Kriterium 5 von D-11 erfüllt** – **zwei** übernehmende Projekte, beide mit `1.0.0` gehoben (`FW-RE-01`). ⚠️ **Prüfung 46 zählt dieses Kriterium ausdrücklich nicht** (eine Enthaltung), und genau deshalb stand sein Nachweis bis heute drei Releases zurück. **Ab jetzt führt ihn `governance/ADOPTION_REGISTRY.md`** (D-322) |

---

## 6. Vorlage für die manuelle Stichprobe (Prüfpunkt 9)

**Sechzehn Träger sind in diesem Release geändert oder neu.** Kein Core-Modul, keine
Regelablage, kein Skill, kein Prompt, keine Checkliste.

⚠️ **Diese Zahl stand hier zuerst auf „dreizehn", während die Tabelle darunter sechzehn
führte** – gezählt vor den drei Trägern, die bei der Umsetzung dazukamen (`D-326`,
dieses Protokoll, die Übergabe). *Der Durchgang vor dem Commit trägt sich zum
siebenunddreißigsten Mal.*

| Träger | Art | Worauf zu sehen ist |
|---|---|---|
| `.gitattributes` | **neu** | Eine Zeile Wirkung, sechzehn Zeilen Begründung |
| `.koolie/core/VERSION` | geändert | `1.0.0` |
| `.koolie/core/CHANGELOG.md` | geändert | Der Release-Eintrag. **ASCII-Umschrift geprüft: null Umlaute** |
| `.koolie/core/LICENSE-HINWEIS.md` | geändert | 🔴 **Hier steht der Klarname des Rechteinhabers** – die einzige Personennennung im ganzen Kern, gewollt nach D-323. **Das ist der Träger, den die Stichprobe zuerst ansieht** |
| `.koolie/core/governance/DECISION_LOG.md` | geändert | D-320 bis D-327, K-108, K-109; K-81 und K-107 geschlossen |
| `.koolie/core/governance/RELEASE_PROCESS.md` | geändert | Abschnitt 4.1 neu, Version `0.2.0` |
| `.koolie/core/governance/ADOPTION_REGISTRY.md` | **neu** | ⚠️ **Enthält Pfade dieses Arbeitsplatzes** (`devpacks/…`) – projektneutral formuliert, aber der Punkt, an dem Arbeitsplatzwissen einsickern könnte |
| `.koolie/core/governance/change-requests/CR-2026-128-…md` | **neu** | Der Antrag mit zwölf Befunden |
| `.koolie/core/docs/ROADMAP.md` | geändert | Releaseplan: `1.0.0` als *dieses Release* |
| `.koolie/core/build/doc/00-kopf.md` | geändert | Dokumentversion `1.0.0` |
| `.koolie/core/build/doc/26-qs-test.md` | geändert | Die drei Zahlen des Prüfapparats |
| `.koolie/core/tests/TEST_CATALOG.md` | geändert | Sondenmenge `18 bis 81` |
| `.koolie/core/tests/scripts/validate-framework.py` | geändert | Prüfung 81 neu, Prüfung 78 erweitert |
| `.koolie/core/tests/scripts/probe-pruefungen.py` | geändert | Fünf neue Sondeneinheiten |
| `.koolie/core/tests/protocols/2026-09-23-freigabelauf-1.0.0.md` | **neu** | Dieses Protokoll |
| `UEBERGABE.md` | geändert | Die Übergabe zum Stand `1.0.0` |

⚠️ **Die automatische Prüfung deckt davon:** Secret-Muster, E-Mail-Adressen,
IP-Adressen, interne Hostnamen, URLs außerhalb der Allowlist, projektlokale Sperrbegriffe,
Produktnamen im Kern und Arbeitsplatzpfade (Prüfungen 6, 14, 71). 🔴 **Sie deckt
NICHT: Personennamen** – gemessen in diesem Release, und als `K-109` aufgenommen. **Genau
dafür verlangt die Checkliste die Stichprobe zusätzlich.**

---

## 7. Die zwei Handlungen des Menschen

### 7.1 Die Freigabe (Prüfpunkt 21)

**Diese Zeile ist leer und bleibt es, bis der Owner sie füllt.** Die Form folgt D-319: Die
Zeile sagt, **was** freigegeben wurde – der Commit sagt, **wer**.

| Rolle | Datum | Umfang |
|---|---|---|
| `René Hildebrand` | `2026-09-23` | `Protokoll gelesen und Träger durchgesehen.` |

### 7.2 Die signierte Marke (Prüfpunkt 20, Schritt 1)

🔴 **Ein Werkzeug kann sie setzen und mit dem vorhandenen Schlüssel sogar signieren – und
genau deshalb darf es nicht** (D-321). Die Befehle liegen in `FREIGABE-1.0.0.txt` neben
der Commit-Nachricht.

🟢 **Gesetzt am 2026-09-23 durch den Framework Owner:** `v1.0.0`, annotiert und
SSH-signiert.

> 🔴 **Und die Verifikation schlug fehl, obwohl die Signatur da war.** `git tag -v v1.0.0`
> gab die Tag-Nachricht aus und schwieg über die Signatur – Ursache war ein fehlendes
> `gpg.ssh.allowedSignersFile`, nicht eine fehlende Unterschrift (**D-327**). Nach der
> Einrichtung: `Good "git" signature … with ED25519 key`.
> ➡️ *Eine Signatur ohne hinterlegten Unterzeichner belegt, daß **jemand** mit diesem
> Schlüssel unterschrieben hat – nicht, **wem** der Schlüssel gehört.* Der Ablauf steht
> seither in `RELEASE_PROCESS.md` Abschnitt 4.1.

---

## 8. Was dieser Lauf **nicht** behauptet

- **Er erklärt das Framework nicht für im Realbetrieb erprobt.** D-11 verlangt das
  ausdrücklich nicht; `AP8` bis `AP10` sind projektseitig und **keine** Vorbedingung für
  `1.0.0` (`CR-2026-001`).
- **Er sagt nichts über den Produktstand nach dem 2026-09-18.** Siehe Prüfpunkt 11.
- **Er zählt die offenen Klärungspunkte nicht.** Sie sind kein Prüfpunkt von `FW-CL-11`
  und kein Kriterium von D-11; ihre Zahl bleibt nach `K-100` unermittelbar.
- **Er entscheidet die Veröffentlichung nicht** (`K-108`).
