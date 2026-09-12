# Änderungsantrag `CR-2026-044`

| Feld | Inhalt |
|---|---|
| Titel | Die Aktivierungsprüfung liest fest verdrahtete Pfade **eines** Clients – für das zweite Pack prüft sie nichts |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-12 |
| Betroffene Artefakte | `tests/scripts/validate-framework.py` (`check_strict_overlay`, Aufruf in `main`), `tests/scripts/probe-pruefungen.py` (neue Sonden), `tests/TEST_CATALOG.md` (`FW-RE-02`) |
| Ebene laut Entscheidungsbaum 6 | Kern – Prüfwerkzeug, clientneutral |
| Art | Befund **B02** des unabhängigen Reviews vom 2026-09-12, P1; **gegengeprüft und gemessen** |
| Dringlichkeit | **vor einem dritten Client Pack** – der Befund vervielfacht seinen Schaden mit jedem Pack |

## 1. Anlass und Problem

`check_strict_overlay(root)` prüft die Aktivierungsreife eines Projekts: Ist das Overlay aktiv,
stehen noch offene Werte in sicherheitsrelevanten Abschnitten, trägt die Berechtigungsdatei noch
Platzhalter. Die Funktion bekommt das erkannte Manifest **nicht übergeben** und liest stattdessen
zwei fest verdrahtete Pfade: `.devin/rules/20-project-overlay.md` und `.devin/config.json`.

**In einer `claude-code`-Installation gibt es beide nicht.** Die Funktion findet sie nicht,
überspringt sie stillschweigend – und meldet 0 zusätzliche Fehler. Die Erkennung des installierten
Packs existiert **in derselben Datei** seit der Umstellung auf mehrere Client Packs
(`detect_client`); sie wird hier nur nicht benutzt.

### Gemessen, nicht nur gelesen

Zwei frische Testinstallationen, je eine pro Pack, darin **derselbe** Defekt. Gemessen ist die
Änderung der Fehlerzahl, nicht ihr absoluter Wert – ein frisches Overlay trägt ohnehin offene
Werte. Der `devin-desktop`-Lauf ist die Positivkontrolle: Ohne ihn wäre nicht zu unterscheiden,
ob die Prüfung bei `claude-code` nichts sieht oder ob der Defekt keiner ist.

| Gesetzter Defekt | `claude-code` | `devin-desktop` |
|---|---|---|
| Overlay-Status auf `aktivierung-ausstehend` | **±0** | **−1 Fehler** |
| Platzhalter in der Berechtigungsdatei (nach Bereinigung gesetzt) | **±0** (7 → 7 → 7) | **+1 Fehler** (10 → 9 → 10) |

**Die Prüfung reagiert beim einen Pack und sieht das andere überhaupt nicht.**

### Zwei Befunde, die dabei herausfielen

Der `−1` in der ersten Zeile ist kein Messfehler. Er ist ein **eigener Befund**, und der
unangenehmere von beiden:

1. **Der Status wird als Präfix geprüft.** `wert.lower().startswith("aktiv")` – damit besteht
   `aktivierung-ausstehend` die Aktivierungsprüfung. Ein Status, der wörtlich sagt, dass die
   Aktivierung **aussteht**, bringt den Fehler zum Verschwinden, der vorher stand. Wer ihn
   einträgt, macht die Prüfung stiller, nicht lauter.

2. **Fehlende Pflichtabschnitte werden akzeptiert.** Die Prüfung sucht in den sicherheitsrelevanten
   Abschnitten nach offenen Werten; ist ein Abschnitt gar nicht da, findet sie nichts und meldet
   nichts. **Ein Overlay ohne Abschnitt 13 ist damit besser gestellt als eines mit einem offenen
   Wert darin.**

Beides ist derselbe Befundtyp wie der Rest dieses Projekts: eine Prüfung, die mehr verspricht, als
sie leistet.

## 2. Vorgeschlagene Änderung

1. **Das Manifest wird übergeben.** `check_strict_overlay(root, man)` leitet die Pfade aus dem
   Manifest ab – Laufzeitregel aus `pack_runtime_dir`, Berechtigungsdatei aus `permissions_file`.
   Kein Pfad eines Clients steht mehr im Kern.

2. **Der Status wird als Aufzählung geprüft**, nicht als Präfix: Aktiv ist genau `aktiv`. Jeder
   andere Wert – auch einer, der mit „aktiv" beginnt – ist nicht aktiv.

3. **Pflichtabschnitte werden auf Existenz geprüft**, nicht nur auf ihren Inhalt. Ein fehlender
   sicherheitsrelevanter Abschnitt ist ein Fehler, kein Freispruch.

4. **Wirkungsnachweis nach D-23 mit denselben Fixtures für beide Packs.** Das ist das
   Abnahmekriterium des Reviews: Dieselben positiven und negativen Aktivierungsfälle laufen für
   jedes Pack, und ein Defekt muss in **jeder** Installation gemeldet werden.

## 3. Was dieser Antrag nicht ändert

- **Die Prüfung bleibt optional.** Sie läuft nur mit `--strict-overlay`; daran ändert sich nichts.
- **Der Abgleich zwischen Quell-Overlay und Laufzeitfassung** – das Review schlägt ihn zusätzlich
  vor – ist hier **nicht** enthalten, siehe E4. Er ist ein eigener Gegenstand.
- **Die sicherheitsrelevanten Abschnitte selbst** werden nicht neu bestimmt; die Liste bleibt, wie
  sie ist.

## 4. Prüffragen

- [x] Richtige Ebene: Kern – der Validator ist clientneutral, und genau das ist er hier nicht.
- [x] Verschärfungsprinzip: Der Antrag verschärft dreifach; er lockert nichts.
- [x] Widerspruchsfreiheit: D-15, D-28 (Werkzeugneutralität des Kerns) gelesen; `detect_client`
      existiert bereits und wird genutzt statt nachgebaut.
- [x] Laufzeitfassungen: nicht betroffen.
- [x] Belegstatus: **gemessen** an zwei frischen Installationen mit Positivkontrolle.
- [ ] Test- und Validierungsbedarf: **neue Sonden nach D-23, je Pack.**
- [x] Overlays: Ein bestehendes Overlay, dessen Status nicht wörtlich `aktiv` lautet, fällt nach
      der Änderung durch – siehe E2.
- [ ] Dokumentation: CHANGELOG, `FW-RE-02` im Testkatalog.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Manifest übergeben oder die Pfade je Pack im Validator führen? | **Manifest übergeben.** Die Erkennung steht in derselben Datei; sie nicht zu benutzen war ein Versehen, keine Entscheidung | Die Funktion bekommt einen zweiten Parameter. Wer sie einzeln aufruft, muss das Manifest beschaffen |
| E2 | Status als Aufzählung – genau `aktiv`? | **Ja, genau `aktiv`.** Ein Präfixvergleich, den `aktivierung-ausstehend` besteht, ist keine Prüfung, sondern eine Einladung | **Eine Verschärfung, die bestehende Overlays brechen kann.** Ein Projekt, das `aktiv seit 2026-03` einträgt, fällt künftig durch. Das ist gewollt – aber es ist ein Migrationsfall und gehört in die Migrationshinweise |
| E3 | Pflichtabschnitte auf Existenz prüfen? | **Ja.** Ein Overlay ohne Abschnitt 13 ist sonst besser gestellt als eines mit einem offenen Wert darin – das ist die Prüfung auf den Kopf gestellt | Ein bestehendes Overlay, dem ein Abschnitt fehlt, fällt künftig durch. Auch das ist ein Migrationsfall |
| E4 | Auch Feldgleichheit zwischen Quell-Overlay und Laufzeitfassung prüfen? | **Nein, nicht in diesem Antrag.** Das Review schlägt es vor, und es ist richtig – aber es ist ein eigener Gegenstand mit eigener Unschärfe: Welche Felder gleich sein müssen, ist nirgends festgelegt. Ein Antrag, der drei Befunde behebt und einen vierten dazu erfindet, wird nicht fertig | Der Befund bleibt offen und braucht einen eigenen Antrag. Bis dahin kann die Laufzeitfassung von der Quelle abweichen, ohne dass es jemand merkt |
| E5 | Wie wird die Wirkung nachgewiesen? | **Dieselben Fixtures für beide Packs**, je Defekt eine Sonde in jeder Installation. Genau das ist das Abnahmekriterium des Reviews – und genau das hätte den Befund von Anfang an verhindert | Die Sonden werden teurer: Sie brauchen eine **Installation** je Pack, nicht nur eine Kopie des Repositoriums. Der Sondenlauf wird spürbar länger |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle fünf Fragen wie vorgelegt.** E1 das Manifest wird übergeben; E2 der Status gilt als aktiv nur bei genau `aktiv`; E3 sicherheitsrelevante Abschnitte werden auf Existenz geprüft; E4 die Feldgleichheit zwischen Quell-Overlay und Laufzeitfassung bleibt einem eigenen Antrag; E5 dieselben Fixtures laufen für beide Packs |
| Datum | 2026-09-12 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | **E2 und E3 sind Verschärfungen und gehören in die Migrationshinweise.** Ein Overlay, dessen Status nicht wörtlich `aktiv` lautet, und eines, dem ein sicherheitsrelevanter Abschnitt fehlt, fallen künftig durch. **Der Nachweis muss je Pack geführt werden** – das ist der Kern des Befunds und das Abnahmekriterium des Reviews. **Nachgewiesen:** sechs Sonden und vier Gegenproben, je Fall in jeder Installation; gegen 0.27.0 fallen **fünf von sechs** Sonden, und die eine, die besteht, ist genau der Fall, den die alte Fassung beim einen Pack traf. **Offen bleibt E4** – der Abgleich zwischen Quelle und Laufzeitfassung ist als eigener Gegenstand auszuweisen, nicht als erledigt |
| Umsetzung | umgesetzt mit `0.28.0` |
