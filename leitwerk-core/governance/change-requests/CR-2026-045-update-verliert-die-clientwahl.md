# Änderungsantrag `CR-2026-045`

| Feld | Inhalt |
|---|---|
| Titel | Der dokumentierte Aktualisierungsaufruf legt in einem fremden Projekt eine zweite Laufzeitschicht an |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-12 |
| Betroffene Artefakte | `install.py` (`--client`, `--update`, `--check`), `docs/ADOPTION_GUIDE.md` (Abschnitt 3), `tests/scripts/probe-pruefungen.py` (neue Sonde) |
| Ebene laut Entscheidungsbaum 6 | Kern – Installationswerkzeug |
| Art | Befund **B10** des unabhängigen Reviews vom 2026-09-12, P2; **gegengeprüft und gemessen** |
| Dringlichkeit | **vor einem dritten Client Pack**, und vor dem nächsten Release-Wechsel eines fremden Projekts |

## 1. Anlass und Problem

`install.py --client` trägt einen **Vorgabewert**: `devin-desktop`. `docs/ADOPTION_GUIDE.md`
Abschnitt 3 empfiehlt für den Release-Wechsel wörtlich:

```bash
python leitwerk-core/install.py --update
```

Ohne `--client`. In einem Projekt, das mit einem anderen Pack installiert wurde, greift damit die
Vorgabe – und `--update` aktualisiert nicht die vorhandene Installation, sondern **legt eine
zweite an**.

### Gemessen

Eine frische `claude-code`-Installation, danach der dokumentierte Aufruf:

```text
Aufruf: python leitwerk-core/install.py --update   (ohne --client)
  Client:  devin-desktop
  Zusammenfassung: 60 angelegt, 0 aktualisiert, 0 unveraendert, 18 Projektdateien behalten.

Laufzeitschichten vorher:  ['.claude']
Laufzeitschichten nachher: ['.claude', '.devin']
```

**Sechzig Dateien**, eine vollständige zweite Laufzeitschicht: Regelablage, Skill-Ablage,
Agentenprofile, eine zweite Berechtigungsdatei. Und – der eigentliche Schaden – **„0
aktualisiert"**: Die Installation, die aktualisiert werden sollte, ist nicht angefasst worden. Der
Aufruf tut nicht zu viel, er tut **das Falsche**.

### Warum das mehr ist als ein unglücklicher Vorgabewert

Ein Projekt, das so aktualisiert wird, hat anschließend zwei Regelsätze im Verzeichnis. Welcher
davon in der Sitzung landet, entscheidet der Client – und beide Packs führen Regeln, die einander
nicht kennen. Der Befund gehört damit zu derselben Familie wie `AP2-CC-01` und B02: **eine Stelle,
an der das Framework stillschweigend etwas anderes tut, als es sagt.**

Das Risiko wächst mit jedem Pack. Mit zwei Packs trifft es die Projekte des einen; mit drei die
Projekte von zweien.

## 2. Vorgeschlagene Änderung

1. **`install.py` erkennt das installierte Pack** – so, wie der Validator es seit der Umstellung
   auf mehrere Packs tut: Geprüft wird, welches `runtime_dir` aus den Manifesten im
   Zielverzeichnis tatsächlich liegt.

2. **`--update` und `--check` ohne `--client` verwenden das erkannte Pack.** Der Vorgabewert
   greift dort nicht mehr.

3. **Widerspricht ein ausdrückliches `--client` dem erkannten Pack, bricht der Lauf ab** – mit
   Nennung beider Packs und des Wegs, es doch zu tun. Eine zweite Laufzeitschicht entsteht dann
   nur, wenn jemand sie ausdrücklich will.

4. **Wird nichts erkannt**, bleibt es bei `--client` beziehungsweise dessen Vorgabe: Eine
   Erstinstallation hat nichts, was sie erkennen könnte.

5. **`ADOPTION_GUIDE.md` Abschnitt 3** nennt den Aufruf mit dem Hinweis, dass das Pack erkannt
   wird – und was zu tun ist, wenn die Erkennung fehlschlägt.

6. **Wirkungsnachweis nach D-23:** Eine Sonde aktualisiert eine `claude-code`-Installation ohne
   `--client` und prüft, dass **keine** zweite Laufzeitschicht entsteht. Gegenprobe: Dieselbe
   Aktualisierung auf einer `devin-desktop`-Installation läuft unverändert durch.

## 3. Was dieser Antrag nicht ändert

- **Der Vorgabewert bleibt** – für die Erstinstallation. Er ist dort sinnvoll und harmlos.
- **Bestehende Doppelinstallationen werden nicht aufgeräumt.** Wer zwei Laufzeitschichten im
  Verzeichnis hat, bekommt mit diesem Antrag keine Hilfe beim Entfernen; das wäre ein eigener
  Gegenstand mit Löschverhalten, und Löschen gehört nicht in ein Installationswerkzeug ohne
  ausdrückliche Entscheidung.
- **Die Erkennung selbst wird nicht neu erfunden.** Sie folgt derselben Regel wie im Validator.

## 4. Prüffragen

- [x] Richtige Ebene: Kern – `install.py` ist clientneutral und trifft hier eine Clientwahl.
- [x] Verschärfungsprinzip: Der Antrag verschärft – ein Lauf, der bisher stillschweigend
      durchlief, bricht künftig ab.
- [x] Widerspruchsfreiheit: `ADOPTION_GUIDE.md` Abschnitt 3, `detect_client` im Validator gelesen.
- [x] Laufzeitfassungen: nicht betroffen; es ändert sich, **welche** erzeugt wird.
- [x] Belegstatus: **gemessen** an einer frischen Installation, 60 Dateien.
- [ ] Test- und Validierungsbedarf: **neue Sonde nach D-23** samt Gegenprobe.
- [x] Overlays: nicht betroffen.
- [ ] Dokumentation: CHANGELOG, `ADOPTION_GUIDE.md`.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Erkennung statt Vorgabe bei `--update` und `--check`? | **Ja.** Eine Aktualisierung richtet sich an etwas Vorhandenes; was vorhanden ist, ist ablesbar. Ein Vorgabewert ist dort eine Vermutung, die niemand braucht | Die Erkennung kann fehlschlagen – etwa bei einer unvollständigen Installation. Dann braucht der Nutzer `--client`, und die Fehlermeldung muss das sagen |
| E2 | Was tun, wenn `--client` dem erkannten Pack widerspricht? | **Abbrechen und beide nennen.** Ein Wechsel des Packs ist eine Entscheidung, kein Nebenprodukt einer Aktualisierung | Ein Pack-Wechsel wird umständlicher. Wer ihn will, muss die alte Laufzeitschicht selbst entfernen – der Abbruchtext nennt den Weg |
| E3 | Den Vorgabewert für die Erstinstallation behalten? | **Ja.** Dort gibt es nichts zu erkennen, und ein Vorgabewert erspart dem Einstieg eine Entscheidung, die er noch nicht treffen kann | Der erste Aufruf installiert weiterhin ungefragt `devin-desktop`. Wer ein anderes Pack will und `--client` vergisst, merkt es erst hinterher – die Ausgabe nennt das Pack aber in der ersten Zeile |
| E4 | `ADOPTION_GUIDE.md` korrigieren oder den Aufruf um `--client` ergänzen? | **Korrigieren, ohne `--client` zu verlangen.** Ein Leitfaden, der bei jedem Aufruf einen Schalter mitschleppt, wird nicht befolgt; die Erkennung nimmt ihm die Pflicht ab | Der Leitfaden muss erklären, was passiert, wenn die Erkennung fehlschlägt – eine Zeile mehr an einer Stelle, die kurz sein sollte |
| E5 | Wie wird die Wirkung nachgewiesen? | **Zwei Läufe, beide nötig:** eine Sonde, die auf einer `claude-code`-Installation aktualisiert und belegt, dass keine zweite Schicht entsteht – und die Gegenprobe auf `devin-desktop`, die belegt, dass die Aktualisierung weiterhin tut, was sie soll | Die Sonde braucht zwei vollständige Installationen. Der Sondenlauf wird länger; zusammen mit `CR-2026-044` lohnt sich ein gemeinsamer Aufbau |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle fünf Fragen wie vorgelegt.** E1 `--update` und `--check` erkennen das installierte Pack; E2 ein widersprechendes `--client` bricht ab und nennt beide Packs; E3 der Vorgabewert bleibt für die Erstinstallation; E4 der Leitfaden wird korrigiert, ohne `--client` zu verlangen; E5 Sonde und Gegenprobe je Pack |
| Datum | 2026-09-12 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | **Der Abbruch muss den Weg nennen**, sonst ist er eine Sackgasse: Der Text sagt, welches Pack installiert ist, welches angefordert war, was ein Weiterlauf angerichtet hätte, und dass ein Packwechsel das Entfernen der vorhandenen Laufzeitschicht verlangt. **Nachgewiesen:** je Pack eine Sonde und eine Gegenprobe; gegen 0.27.0 fallen drei von vier, und die eine, die besteht, ist `devin-desktop` – also genau das Pack, das die alte Vorgabe zufällig traf. Der Abbruchpfad ist an seinem Exit-Code belegt, nicht nur an seinem Text |
| Umsetzung | umgesetzt mit `0.28.0` |
