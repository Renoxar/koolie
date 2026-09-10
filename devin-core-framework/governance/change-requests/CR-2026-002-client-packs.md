# Änderungsantrag `CR-2026-002`

| Feld | Inhalt |
|---|---|
| Titel | Client Packs: Abbildungsschicht für KI-Clients mit Fähigkeitsmatrix |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | neu: `devin-core-framework/clients/`; geändert: `devin-core-framework/docs/PLACEHOLDER_REGISTRY.md`, `devin-core-framework/OWNERS.md`, `README.md`, `devin-core-framework/CHANGELOG.md` |
| Ebene laut Entscheidungsbaum 6 | Core (Struktur) |
| Art | neu |
| Dringlichkeit | regulär (Review-Zyklus) |

## 1. Anlass und Problem

Das Framework ist an einen einzigen KI-Client gebunden, obwohl seine Substanz clientneutral ist. D-02 trennt bereits die kanonische, werkzeugneutrale Langform in `devin-core-framework/framework/` von der Laufzeitform in der Projektwurzel – die Naht für eine Ablösung existiert also, ist aber nirgends benannt. `root-template/` ist faktisch der Adapter für einen Client, ohne als solcher deklariert zu sein.

Der schwerwiegendere Punkt betrifft nicht die Pfade, sondern die **Durchsetzungstiefe**. Zusagen wie „Secret-Dateien werden nicht gelesen" sind beim heutigen Client Verweigerungsregeln, die die Engine erzwingt. Bei einem Client ohne pfadbasierte Berechtigungen wäre dieselbe Zusage nur noch ein Satz im Kontext, dem ein Modell folgen kann oder auch nicht. Ohne eine Stelle, an der dieser Unterschied ausgewiesen wird, würde eine Portierung falsche Sicherheit erzeugen – und zwar im Datenschutz- und Sicherheitskern, also dort, wo der Schaden am größten ist.

Zeitlich ist der Eingriff jetzt am günstigsten: Die Strukturänderung ist ein Breaking Change und in einem 0.x-Stand nach Semantic Versioning kostenlos. Nach 1.0.0 kostet sie ein 2.0.0 samt Migrationspaket für jedes aufnehmende Projekt. Derzeit existiert genau ein aufnehmendes Repository (das Übungsrepository).

## 2. Vorgeschlagene Änderung

Einführung von **Client Packs** unter `devin-core-framework/clients/`:

1. `README.md` – Zweck, Abgrenzung, Regeln der Fähigkeitsmatrix, Erstellungsanleitung.
2. `_template/CLIENT_PACK.md` – Vorlage mit Pfadabbildung und einer Fähigkeitsmatrix aus 26 Zusagen in sieben Gruppen (R Regelladung, S Skills, B Berechtigungen, H Hooks, A Agentenprofile, M Modi, X externe Anbindung).
3. `devin-desktop/CLIENT_PACK.md` – der heutige Client als erstes Pack, ausgefüllt aus dem Ist-Zustand.

**Kern der Vorlage** ist die dreiwertige Einstufung je Zusage: `[TECHNISCH]` (Engine erzwingt), `[TEXTUELL]` (nur Anweisung), `[NICHT ABBILDBAR]` (kein Mechanismus). Sechs Zusagen sind als **Kernzusagen** markiert; sie entsprechen `_core_rules_integrity` in der Berechtigungsdatei. Weicht eine davon von `[TECHNISCH]` ab, ist sie einzeln zu begründen, im Overlay als Ausnahme zu führen und durch `<SECURITY_CONTACT>` freizugeben.

Neu registrierte Platzhalter: `<CLIENT_PACK_NAME>`, `<CLIENT_PACK_CODE>` sowie der clientneutrale Marker `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>`.

**Nicht Bestandteil dieses Antrags** (Folgearbeit für Release 0.5.0): Verschiebung von `root-template/` unter das jeweilige Pack, Schalter `--client` in `install.py`, Umbenennung der devin-spezifischen Verzeichnis- und Markernamen, ein zweites Client Pack.

## 3. Prüffragen (durch Owner auszufüllen)

- [x] Richtige Ebene nach Entscheidungsbaum 6? — Ja. Die Schicht ist Struktur des Kerns; sie enthält keine Projektwerte.
- [x] Verschärfungsprinzip eingehalten? — **Ja, und das ist hier die entscheidende Frage.** Ein Client Pack führt keine Verhaltensregel ein, lockert keine bestehende und steht in keiner Konfliktbeziehung zu Core, Overlay oder Packs. Die achtstufige Prioritätshierarchie (D-06) bleibt unberührt; ein Client Pack ist bewusst **keine** Regelebene, sondern eine Abbildungsschicht. Bei Widerspruch zur Langform gilt die Langform. Das ist in `clients/README.md` Abschnitt 2 normativ festgehalten.
- [x] Widerspruchsfreiheit geprüft? — Gelesen: `PRIORITY_HIERARCHY.md`, `09-risk-model.md` (V1–V12), `08-skill-conventions.md`, `role-packs/README.md`, `tech-packs/README.md`, `.devin/README.md`, `.devin/rules/README.md`, `.devin/config.json`. Die Delegationsverbote V1–V12 sind ausdrücklich von der Matrix ausgenommen: Sie sind organisatorischer Natur und bei jedem Client `[TEXTUELL]`.
- [x] Laufzeitfassungen betroffen? — Nein. `AGENTS.md`, `.devin/rules/*` und `.devin/config.json` bleiben unverändert; das Devin-Pack beschreibt sie nur.
- [x] Belegstatus korrekt? — Ja, und der Befund ist unbequem: 13 der 26 Zeilen des Devin-Packs tragen einen VERIFY-Marker, keine einzige Einstufung ist gegen eine Installation geprüft. Das Pack weist sich deshalb im Kopf ausdrücklich als **unbelegt** aus.
- [x] Test- und Validierungsbedarf? — `validate-framework.py` ohne Fehler und Warnungen. Ein Testfall für die Vollständigkeit einer Fähigkeitsmatrix (jede Zeile eingestuft, jede Kernabweichung begründet) ist als Folgearbeit vorzusehen.
- [x] Auswirkungen auf Overlays und laufende Onboardings? — Keine. Rein additive Änderung.
- [x] Dokumentation? — CHANGELOG, Platzhalterregister, OWNERS, Verzeichnisbaum in `README.md`.

## 4. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | angenommen |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Die Schicht macht eine bereits vorhandene Naht (D-02) explizit und ist rein additiv. Ihr eigentlicher Wert liegt in der Fähigkeitsmatrix: Sie zwingt jede Portierung dazu, offenzulegen, welche Zusage der Zielclient technisch erzwingt und welche nur noch Prosa ist. Ohne diesen Zwang wäre Clientneutralität ein Sicherheitsrisiko statt einer Verbesserung. Der Zeitpunkt ist der günstigste mögliche: ein 0.x-Stand mit einem einzigen aufnehmenden Repository. |
| Ziel-Release | 0.5.0 |
| Decision-Log-Eintrag | D-12 |

## 5. Umsetzung (nach Annahme)

- [x] `clients/README.md`, `_template/CLIENT_PACK.md`, `devin-desktop/CLIENT_PACK.md` angelegt
- [x] Platzhalter registriert; `OWNERS.md` und Verzeichnisbaum ergänzt
- [x] Validator ohne Fehler und Warnungen
- [x] CHANGELOG und Decision Log ergänzt
- [ ] Folgearbeit 0.5.0: `root-template/` je Pack, `install.py --client`, Umbenennung, zweites Client Pack
- [ ] Kommunikation an Projekte — entfällt (nur das Übungsrepository hat aufgenommen)
