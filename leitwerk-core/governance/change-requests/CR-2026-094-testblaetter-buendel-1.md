# Änderungsantrag `CR-2026-094`

| Feld | Inhalt |
|---|---|
| Titel | Testblätter, Bündel 1 – elf Ergebniszellen, und vier Befunde, die größer sind als das Bündel |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-19 |
| Betroffene Artefakte | drei `TESTS.md` (elf Ergebniszellen, eine Erwartungszelle), `tests/scripts/validate-output.py` (Manifestauflösung), `tests/scripts/validate-framework.py` (**Prüfung 62**, Register, Nachweisspanne), `tests/scripts/probe-pruefungen.py` (Sonden 62a/62b, Gegenproben 62a/62b, Spanne), **dreizehn** `SKILL.md` und ihre `CHANGELOG.md` (Ausgabevorlage, Versionsanhebung), `clients/claude-code/CLIENT_PACK.md` (S2, S3, Version), `tests/TEST_CATALOG.md` (Spanne), `governance/DECISION_LOG.md` (D-185 bis D-190, `K-73` neu), `docs/ROADMAP.md` (Standzeile, Posten 0.68.0 und 0.69.0), `tests/protocols/2026-09-19-testblaetter-buendel-1.md` (neu), `CHANGELOG.md`, `VERSION` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind Testblätter, Prüfapparat, Skills und ein Client Pack |
| Art | Messung, Befund, neue Prüfung |
| Dringlichkeit | **Regulär.** Der Meßtag war geplant (D-180); die vier Befunde sind bei seiner Durchführung angefallen |

## 1. Anlass

Der Releaseplan nennt als Posten **Bündel 1 der dreizehn Testblätter**: elf offene
Ergebniszellen an den drei Skills, die **keinen** Befehlsschlitz ausführen. `K-72` war die
Bedingung dafür und ist mit 0.67.1 entschieden.

## 2. Das Ergebnis in einer Zeile

🟢 **Alle elf Zellen bestanden. Kriterium 2: 85 → 74.** 26 Läufe, rund 23 USD.

Der Weg dahin und jeder Beleg stehen im Protokoll
(`tests/protocols/2026-09-19-testblaetter-buendel-1.md`). Dieser Antrag legt vor, was zu
entscheiden war.

## 3. Der erste Befund: das Prüfmittel selbst war clientgebunden (D-186)

`validate-output.py` ist das **zweite Prüfmittel** von drei `P01`-Zellen und löste den
Skillpfad fest verdrahtet als `.devin/skills/<name>/SKILL.md` auf. In einem
`claude-code`-Meßbaum meldet es *„Skill nicht gefunden"* und endet wie ein Befund.

🔴 **Der Lauf vom 2026-09-17 hat nur deshalb bestanden, weil das Auswerteskript mit
`--root` auf das Framework-Repositorium zeigte** – dort liegt eine
`devin-desktop`-Testinstallation. Ein richtiger Schluß aus einem falschen Beleg.

**Prüfung 48 sieht es nicht:** Sie nimmt **Werkzeuge** ausdrücklich aus ihrem Gegenstand –
und diese Ausnahme ist für Texte *über* Werkzeuge gedacht, nicht für eine Clientbindung,
die **wirkt**.

## 4. Der zweite Befund: der Aufruf mit Schrägstrich ist kein Werkzeugaufruf (D-187)

Zwölf von zwölf Mitschriften führen `<command-name>` samt Argumenten und die ganze
`SKILL.md` als Nutzernachricht – **keinen** `Skill`-Werkzeugaufruf. Die Zeile `S2` der
Fähigkeitsmatrix beschreibt beides als einen Weg; gemessen wurde 2026-09-14 der
**modellseitige** Aufruf, benannt ist in der ersten Spalte der **Schrägstrich**.

➡️ **Der Testkatalog verlangt seit D-146 genau den Weg, über den die Zeile nichts
Gemessenes sagte.**

## 5. Der dritte Befund: das Frontmatter erscheint als `command_permissions` (D-188)

Jede Mitschrift trägt `{"type": "command_permissions", "allowedTools": ["Read","Grep","Glob"]}`
– genau die Werkzeuge aus `allowed-tools`. Der Trennbaum `kplanw` (Frontmatter entfernt)
führt dort eine **leere** Liste; die Ableitung ist damit belegt.

🔴 **Der Schreibkorb, den der Aufbau eigens geöffnet hatte, war für die Dauer des Befehls
wirkungslos.** Sechs Zellen prüfen ein Unterlassen von Schreibhandlungen – ihre Zurechnung
gehört je Schicht ausgewiesen (D-122), und der Zuschnitt ohne Frontmatter ist genau dafür
gefahren worden.

🔴 **Offen bleibt `K-73`:** Zwei Läufe haben `Bash` **aufgerufen**, obwohl der Skill es in
`disallowed-tools` führt; beide Aufrufe wurden abgewiesen. `S3` sagt, die Sperre entferne
das Werkzeug aus dem Vorrat.

## 6. Der vierte Befund: zehn von dreizehn Skills trugen eine fremde Version (D-185)

**Gefunden haben es zwei gemessene Läufe**, unaufgefordert, in Nebenbemerkungen ihrer
Ergebnisberichte. Nachgezählt: 13 Träger, 15 Fundstellen, **10 abweichend** – und die drei
übereinstimmenden sind die drei, deren Version seit der Erstfassung nicht gestiegen ist.

## 7. Zwei Befunde an den Zellen selbst

**`SK-002-N03` verlangte ein Anhalten, dessen Auslöser nicht herstellbar ist** (D-189):
Der Skill knüpft es an personenbezogene **Echtdaten**, und Regel 5 des
Präparationsregisters verbietet reale Inhalte im Übungsrepositorium.

**`SK-001-N03` hängt an der Form der Eingabe** (D-190): `validierung` wird als
Fragestellung gelesen, `validierung.ts` trifft die Vorbedingung. Dieselbe Zelle, dieselbe
Präparation, zwei Ergebnisse.

## 8. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Welche der elf Zellen werden abgenommen?** | **Alle elf.** Jede Zelle nennt ihren Beleg, das gemessene Client Pack (D-117) und die Zurechenbarkeit (D-175) | **Vier Zellen sind nicht zurechenbar, zwei nur zur Hälfte** – und das steht jetzt in der Zelle. D-115 bleibt: Zurechenbarkeit ist nicht der Ergebnisstatus. Der Gegenpreis der Alternative wäre ein Katalog, der nur zurechenbares Verhalten abnimmt – nach dieser Reihe hätte er **sieben statt elf** |
| **E2** | **Versionsvorlage: Zahlen nachziehen oder ableiten?** | **Ableiten** (D-185), **Prüfung 62** setzt es durch | Dreizehn Skills angehoben, dreizehn Changelogzeilen, zwei Sonden und zwei Gegenproben. **Der Gegenpreis ist gemessen:** Die Zahlen sind über zehn Releases gedriftet, ohne daß eine Prüfung sie ansah |
| **E3** | **`validate-output.py`: Aufrufstelle anpassen oder Werkzeug umbauen?** | **Werkzeug umbauen** (D-186): Ablage aus dem Manifest, Rückfall auf die Quelle, Abbruch bei zwei Packs | Ein Kernwerkzeug geändert, vier Zuschnitte gemessen. **Die Alternative pflegt eine Angabe an der Aufrufstelle, und niemand zählt sie nach** |
| **E4** | **Zeile `S2`: stehen lassen und vermerken, oder berichtigen?** | **Berichtigen** (D-187): zwei Wege, getrennt benannt, die drei Grenzen dem modellseitigen zugeordnet | Die Zeile wird länger, und das Client Pack steigt auf 0.23.0. **Eine Fähigkeitsmatrix ist eine Zusage, kein Protokoll** |
| **E5** | **Zeile `S3`: was wird eingetragen, was bleibt offen?** | **Eingetragen wird das Gemessene** (`command_permissions`, leere Liste ohne Frontmatter); **offen bleibt `K-73`** | Ein offener Punkt mehr, und er ist sicherheitsnah. **Zwei Beobachtungen ohne Trennlauf tragen keine Umstufung** – dieselbe Zurückhaltung wie bei `K-70` |
| **E6** | **`SK-002-N03`: Zelle, Präparation oder Skill?** | **Die Erwartungszelle** (D-189) | Eine berichtigte Zelle im selben Release, in dem sie gemessen wird. **Die Berichtigung nimmt eine Forderung weg, deren Auslöser die Präparation nicht herstellen darf** – sie fügt keine hinzu, und der gemessene Lauf erfüllt die berichtigte Fassung wörtlich |
| **E7** | **`SK-001-N03`: welcher Lauf zählt?** | **Der zweite** (`validierung.ts`), und die Zelle nennt beide Formen (D-190) | Ein zusätzliches Laufpaar, rund 1,7 USD. **Der erste Lauf ist kein Fehlschlag** – er hat den Skill korrekt angewandt und eine andere Frage beantwortet als die Zelle stellt. Der Gegenpreis des Verschweigens wäre eine Zelle, die beim nächsten Durchgang wieder kippt |
| **E8** | **Wird der Prüfapparat in diesem Release beschleunigt?** | **Nein, eigener Posten `0.69.0`** | Ein Einschub mehr vor Bündel 2. **Der Grund ist der Meßtag selbst:** Der Sondenlauf kostet zweimal 233 Einheiten je Release und bremst jede Zwischenprüfung – aber ein Umbau des Prüfapparats **im selben Release wie eine Messung** vermischt zwei Gegenstände |

## 9. Entscheidung

**E1 bis E8 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-19). Decision
Records **D-185** bis **D-190**; Klärungspunkt **`K-73`** neu.

## 10. Abnahme

- `validate-framework.py`: **0 Fehler, 0 Warnungen** gegen den fertigen Baum, **Kriterium 2
  ausgerechnet: 74**.
- `probe-pruefungen.py` in **beiden** Kodierungsumgebungen (D-49).
- **Der Wirkungsnachweis für Prüfung 62 ist ein Paar aus zwei Sonden und zwei
  Gegenproben:** die Kopfzeile der Ausgabevorlage und die Zeile `Erstellt mit` – **die
  zweite Gestalt hätte ein Zuschnitt auf die Überschrift verfehlt**, und genau sie trugen
  zwei Skills doppelt. Die Gegenproben belegen, daß der unveränderte Baum durchläuft und
  daß der Schlitz mehrfach stehen darf.
- **Der Wirkungsnachweis für `validate-output.py` sind vier Zuschnitte**, je ein Lauf:
  Pack `claude-code`, Pack `devin-desktop`, kein Pack, zwei Packs.
- **Die Messung selbst ist durch Kontrollläufe belegt**, je Zelle einer, dazu ein
  zusätzlicher Trennlauf ohne Frontmatter und ein Trennlauf zu `K-73`.
