# Änderungsantrag `CR-2026-011`

| Feld | Inhalt |
|---|---|
| Titel | Hauptdokument: reproduzierbarer Bau aus einer Referenzinstallation, Abbildungsschicht eingearbeitet |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | `build/assemble.py`; neu: `build/doc/07a-abbildungsschicht.md`; geändert: 20 Kapitelquellen, insbesondere `00`, `01`, `04`, `05`, `07`, `15`, `31`, `32` |
| Ebene laut Entscheidungsbaum 6 | Core (Dokumentation und Werkzeug) |
| Art | Änderung |
| Dringlichkeit | regulär (Review-Zyklus) |

## 1. Anlass und Problem

Das Hauptdokument stand auf Framework-Release 0.1.0 und beschrieb ein Framework für genau einen KI-Client. Eine Auszählung der Kapitelquellen ergab drei Befunde, von denen nur der zweite erwartet war.

**Der Bau war nicht reproduzierbar.** 28 der 91 Einbettungen zeigten nicht auf den Kern, sondern auf die **installierte Laufzeitschicht dieses Repositorys** – Pfade, die in der `.gitignore` stehen. Der Bau gelang nur, weil zufällig eine `devin-desktop`-Installation im Arbeitsverzeichnis lag; in einem frischen Auscheckstand brach `assemble.py` ab. Das Dokument zeigte damit die Darstellung *eines* Clients, ohne das zu sagen, und niemand außerhalb dieses Arbeitsplatzes konnte es erzeugen.

**Die Prosa war ungleich veraltet.** 25 von 33 Kapiteln nannten einen einzelnen Client, aber fünf Kapitel trugen 110 der 173 Fundstellen. Die übrigen zwanzig hatten ein bis drei – meist „Devin“ als Synonym für „der Assistent“.

**Zwei Kapitel waren durch Repository-Artefakte überholt.** Kapitel 15 führte von Hand eine Tabelle der Client-Mechanismen mit Belegstatus – genau das, was seit 0.5.0 Pfadabbildung und Fähigkeitsmatrix eines Client Packs leisten. Kapitel 31 pflegte ein Inventar auf dem Stand von 0.2.0, das beschrieb, was das Dateisystem ohnehin weiß.

Nur rund ein Zehntel des Dokuments ist handgeschriebene Prosa: 843 Zeilen erzeugen 8.573 Zeilen Ergebnis. Der Umbau war deshalb kleiner als „32 Kapitel“ – und an anderer Stelle unangenehmer.

## 2. Vorgeschlagene Änderung

**Eine Referenzinstallation als zweite Quelle.** `assemble.py` legt beim Bau eine frische Installation des gewählten Client Packs in einem temporären Verzeichnis an und liest die Laufzeitartefakte von dort. Ein Einbettungspfad mit **Laufzeit-Platzhalter** (`<RUNTIME_DIR>`, `<SKILLS_DIR>`, `<PERMISSIONS_FILE>`, …) meint die Laufzeitschicht; jeder andere Pfad meint das Repository. Die Regel ist am Pfad ablesbar und braucht keine zweite Angabe.

Die Alternative – die werkzeugneutralen Kernquellen einzubetten – wurde verworfen: Sie hätte gezeigt, was im Kern steht, nicht was ein Projekt vorfindet. Gerade bei der Berechtigungsdatei ist die gerenderte Form die Aussage.

**Herkunft an der Datei.** Jede aus der Installation gelesene Einbettung trägt die Angabe, aus welchem Client Pack sie stammt. Das gehört an die Datei und nicht in eine Fußnote, weil sie bei einem anderen Pack anders aussieht.

**`--client` als Schalter.** Das Dokument lässt sich für jedes Pack bauen. Zeigen zwei Platzhalter auf dieselbe Datei – bei einem Client ohne eigene Hook-Datei etwa `<HOOKS_FILE>` und `<PERMISSIONS_FILE>` –, bekommt die zweite Stelle einen Verweis statt eines zweiten Abdrucks.

**Ein neues Kapitel 7a „Client Packs: die Abbildungsschicht".** Der inhaltliche Kern der Releases 0.5.0 bis 0.8.0 kam im Dokument nicht vor. Das Kapitel bettet die Regeln der Schicht und die Fähigkeitsmatrix des zweiten Packs ein, statt sie abzuschreiben. Die Nummerierung bleibt stabil: `07a` sortiert zwischen `07` und `08`, kein bestehender Verweis bricht.

**Ein Pack als durchgehendes Beispiel.** `devin-desktop`, ausdrücklich als solches benannt. Beide Packs überall zu zeigen würde Umfang und Pflege verdoppeln; die Fähigkeitsmatrix beider steht im neuen Kapitel nebeneinander – das ist die Stelle, an der der Unterschied hingehört.

**Kapitel 15 und 31 verlieren ihre handgepflegten Tabellen** an die Artefakte, die dieselbe Aussage versioniert führen. Kapitel 31 gewinnt dafür das Laufzeitglossar als neuen Anhang 31.2.

## 3. Prüffragen (durch Owner auszufüllen)

- [x] Richtige Ebene nach Entscheidungsbaum 6? — Ja. Keine Regel ändert sich; betroffen sind Dokumentation und das Assemblierungswerkzeug.
- [x] Verschärfungsprinzip eingehalten? — Nicht berührt. Die eingebetteten Artefakte sind unverändert; sie kommen nur aus einer anderen, nachvollziehbaren Quelle.
- [x] Widerspruchsfreiheit geprüft? — Die Kapitel 4, 5, 7, 15 und 31 nannten Mechanismen, die seit 0.5.0 anders geregelt sind; genau diese Widersprüche werden hier aufgelöst. `FW-KO-04` und der Validator: 0 Fehler.
- [x] Laufzeitfassungen betroffen? — Nein. Installationsumfang unverändert: 80 / 79 Dateien.
- [x] Belegstatus korrekt? — Der Verifikationsbedarf verweist jetzt auf die Fähigkeitsmatrizen, die ihn versioniert führen, statt ihn im Anhang zu duplizieren. Belegstand unverändert: 13 von 26 Zeilen bei `devin-desktop`, 9 von 26 bei `claude-code` tragen einen VERIFY-Marker.
- [x] Test- und Validierungsbedarf? — Siehe Abschnitt 5.
- [x] Auswirkungen auf Overlays und laufende Onboardings? — Keine. Kein installiertes Artefakt ändert sich.
- [x] Dokumentation? — CHANGELOG, Decision Log, Roadmap.

## 4. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | angenommen |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Ein Dokument, das nur auf einem einzelnen Arbeitsplatz baut, ist kein Lieferbestandteil, sondern ein Zufall. Die Referenzinstallation macht den Bau reproduzierbar und zeigt zugleich die Fassung, die ein Projekt tatsächlich vorfindet – benannt nach dem Client Pack, aus dem sie stammt. |
| Ziel-Release | 0.9.0 |
| Decision-Log-Eintrag | D-21 |

## 5. Umsetzung (nach Annahme)

- [x] `assemble.py`: Referenzinstallation, Platzhalterauflösung über das Manifest, Herkunftsangabe je Einbettung, `--client`, Verweis statt Doppelabdruck bei gleichem Zielpfad
- [x] 23 Direktiven auf Laufzeit-Platzhalter umgestellt, 5 auf Kernquellen (Overlay-Saat und Regelvorlage liegen versioniert unter `templates/`)
- [x] **Bau aus einem frischen Auscheckstand ohne jede Installation: gelingt** – vorher Abbruch mit „eingebettete Datei fehlt“. Geprüft für beide Client Packs
- [x] Neues Kapitel 7a; Kapitel 15 und 31 auf Einbettungen umgestellt; Kapitel 00, 01, 04, 05, 07, 32 neu geschrieben
- [x] Begriffsablösung im Langlauf: 28 Ersetzungen in 19 Kapiteln
- [x] **Messung:** Einclient-Nennungen in der Prosa von 173 auf 50 gesunken, betroffene Kapitel von 25 auf 14. Die verbleibenden benennen einen realen Client, wo einer gemeint ist – Quellenliste der Produktdokumentation (19), clientspezifische Annahme A-05 und Herstellernennungen (7), Glossareinträge, die den Client *definieren* (6), sowie das durchgehende Beispiel
- [x] Validator und `install.py --check` gegen die Wurzelinstallation: 0 Fehler; Installationsumfang unverändert
- [ ] **Folgearbeit:** Die Word-Fassung (`build-docx.py`) ist nicht Teil dieser Änderung. Sie folgt dem Markdown, wurde aber seit dem Umbau nicht erzeugt – `pandoc` und `mmdc` sind hier nicht installiert
- [ ] **Beobachtung:** Kapitel 32 ist eine Selbstprüfung der Erstfassung. Sie ist fortgeschrieben, bleibt aber ihrer Anlage nach ein Rückblick auf 0.1.0. Ob sie als Abschlussteil erhalten bleibt oder in einen Release-Bericht überführt wird, ist eigene Arbeit
