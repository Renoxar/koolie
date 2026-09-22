# Änderungsantrag `CR-2026-007`

| Feld | Inhalt |
|---|---|
| Titel | Geteilte Kernbestandteile: Overlay-Vorlage, Regelvorlagen, Wurzel-Anweisung, Core-Regeltexte, Agentenprofil |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | neu: `leitwerk-core/framework/runtime/`, `leitwerk-core/templates/project-overlay/`, `leitwerk-core/templates/rules/`; geändert: `install.py`, `tests/scripts/validate-framework.py`, `clients/*/manifest.json`, `docs/PLACEHOLDER_REGISTRY.md` |
| Ebene laut Entscheidungsbaum 6 | Core (Struktur) |
| Art | Änderung |
| Dringlichkeit | regulär (Review-Zyklus) |

## 1. Anlass und Problem

`CR-2026-006` hat die Skills auf eine gemeinsame Quelle gebracht und dabei gemessen, was sonst noch doppelt lag: **18 der 32 Dateien** eines Client Packs waren byteweise identisch mit ihrer Entsprechung im anderen Pack. Weitere sieben unterschieden sich nur in der Form, nicht im Inhalt.

Zwei Klassen waren betroffen:

**Clientneutral, nur historisch im Pack.** `project-overlay/` ist **Ebene 4 – Projekt** und hat mit dem Client nichts zu tun; die beiden Regelvorlagen sind Framework-Gut. Sie lagen nur deshalb im Pack, weil `root-template/` ursprünglich alles enthielt.

**Inhalt Framework, Form Client.** Wurzel-Anweisung, die drei Core-Regeltexte und das Agentenprofil – derselbe Fall wie bei den Skills.

## 2. Vorgeschlagene Änderung

**Ein generischer Mechanismus für geteilte Bestandteile.** Das Manifest führt sie unter `shared_core` (wird bei `--update` überschrieben) und `shared_seed` (nur bei der Erstinstallation angelegt); ein Eintrag ist `{"src": …, "dst": …}`, der Zielpfad darf Laufzeit-Platzhalter enthalten, und ein Verzeichnis wird rekursiv abgebildet. Der Mechanismus trägt jede weitere Datei, die aus dem Kern installiert werden soll.

**Neue Ablagen:**

| Ablage | Inhalt |
|---|---|
| `templates/project-overlay/` | Saat für Ebene 4, 18 Dateien |
| `templates/rules/` | die beiden Regelvorlagen |
| `framework/runtime/` | Wurzel-Anweisung, Core-Regeltexte `00-`, `10-`, `15-`, Agentenprofil |

`framework/runtime/` ist die werkzeugneutrale Laufzeitfassung – genau das, was D-02 seit jeher meint, aber bisher nirgends lag.

**Drei neue Formtransformationen**, alle aus dem Manifest gesteuert:

| Transformation | Steuerung | Wirkung |
|---|---|---|
| Regeltext | `rule_frontmatter`: `yaml` oder `comment` | Ein Client ohne Ladetrigger bekommt statt des YAML-Frontmatters einen Kommentar, der Zweck und Ladeverhalten festhält |
| Wurzel-Anweisung | `root_instruction_imports` | An der Marke `<!-- RUNTIME_IMPORTS -->` werden die Einbindungen dieses Clients eingesetzt; ohne Einträge verschwindet die Marke rückstandsfrei |
| Agentenprofil | `agent_frontmatter` | Feldname und Werkzeugformat (`allowed-tools` als Liste gegenüber `tools` kommagetrennt) |

**Ein neuer Laufzeit-Platzhalter `<CLIENT_NAME>`.** Die Wurzel-Anweisung trug im Titel den Produktnamen – in einer Installation des anderen Packs schlicht falsch. Er wird jetzt aus dem Manifest gesetzt.

## 3. Prüffragen (durch Owner auszufüllen)

- [x] Richtige Ebene nach Entscheidungsbaum 6? — Ja, und die Änderung korrigiert zwei Fehlzuordnungen: Das Project Overlay ist Ebene 4 und gehörte nie in ein Client Pack; die Core-Regeltexte sind Ebene 3.
- [x] Verschärfungsprinzip eingehalten? — Ja. **Nachgewiesen, nicht behauptet:** Alle fünf verschobenen Laufzeitartefakte sind nach dem Rendern byteweise identisch mit dem Stand 0.4.0 (Vergleich gegen `git HEAD`). Einzige gewollte Abweichung ist der Titel der Wurzel-Anweisung, der jetzt den Namen des tatsächlich verwendeten Clients trägt.
- [x] Widerspruchsfreiheit geprüft? — `framework/runtime/` ergänzt `framework/core/` (Langform) um die Kurzfassung; das Verhältnis beider ist in D-02 geregelt und unverändert.
- [x] Laufzeitfassungen betroffen? — Nur ihr Ursprung. Installationsumfang unverändert: 80 / 79 Dateien.
- [x] Belegstatus korrekt? — Unverändert.
- [x] Test- und Validierungsbedarf? — Siehe Abschnitt 5.
- [x] Auswirkungen auf Overlays und laufende Onboardings? — Für ein bestehendes Projekt keine: Das Overlay ist Saat und wird nie überschrieben. Beim Release-Wechsel meldet `--check` die Core-Dateien als abweichend, sofern das Projekt noch den 0.4.0-Stand trägt; `--update` stellt her.
- [x] Dokumentation? — Platzhalterregister (`<CLIENT_NAME>`), CHANGELOG, Decision Log.

## 4. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | angenommen |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Ein Client Pack enthält jetzt nur noch, was tatsächlich clientspezifisch ist – sieben beziehungsweise sechs Dateien statt achtzig. Jede Doppelpflege ist beseitigt, ohne dass ein Inhalt sich ändert. |
| Ziel-Release | 0.5.0 |
| Decision-Log-Eintrag | D-17 |

## 5. Umsetzung (nach Annahme)

- [x] `shared_core` / `shared_seed` in `install.py`; Verzeichnisse werden rekursiv abgebildet
- [x] `project-overlay/` und die beiden Regelvorlagen nach `templates/` verschoben, mit Laufzeit-Platzhaltern versehen
- [x] Wurzel-Anweisung, Core-Regeltexte und Agentenprofil nach `framework/runtime/` verschoben und neutralisiert
- [x] Renderer `render_rule`, `render_root_instruction`, `render_agent`; Auswahl anhand des Quellpfads
- [x] `<CLIENT_NAME>` als Laufzeit-Platzhalter registriert und in die Validatorprüfung aufgenommen
- [x] **Byteweiser Vergleich gegen 0.4.0**: alle fünf Laufzeitartefakte identisch
- [x] Erstinstallation unverändert: 80 / 79 Dateien; `--check` gegen beide fehlerfrei
- [x] Drift an einer gerenderten Regel: Exit 1 mit Nennung der gemeinsamen Quelle; `--update` stellt her
- [x] Validator gegen beide Installationen und das Übungsrepository: je 0 Fehler
- [x] Zwischenbefund behoben: Beim Entfernen der Import-Marke blieb eine Leerzeile stehen; sie hätte in jedem bestehenden Projekt eine Scheindrift ausgelöst
- [ ] Folgearbeit: Berechtigungsdatei und Hook-Konfiguration. Beide sind mehr als eine Formfrage – sie erfordern eine Semantikabbildung der Regeln (Werkzeugnamen, Präfixmuster, getrennte Werkzeuge für Ändern und Anlegen) und gehören in einen eigenen Änderungsantrag.
