# Client Pack `<CLIENT_PACK_NAME>` – Vorlage

<!-- AUSFÜLLHINWEIS: Kopiere dieses Verzeichnis nach ../<client-name>/, ersetze alle Platzhalter
     und lege ../<client-name>/root-template/ mit den Wurzelartefakten dieses Clients an.
     Trage das Pack in ../README.md Abschnitt 6 und in leitwerk-core/OWNERS.md ein.
     Ein Client Pack führt keine Verhaltensregeln ein (../README.md Abschnitt 2). -->

| Attribut | Wert |
|---|---|
| Modul-ID | `CP-<CLIENT_PACK_CODE>` |
| Ebene | keine – Abbildungsschicht |
| Version | 0.2.0 |
| Status | entwurf |
| Owner (Rolle) | `<TBD: Rolle>` |
| Client | `<TBD: Produktname>` |
| Geprüfte Clientversion | `<TBD: Version; ohne diese Angabe ist keine Einstufung [TECHNISCH] zulässig>` |
| Datum der Prüfung | `<TBD: JJJJ-MM-TT>` |

## 1. Pfadabbildung

Wohin dieser Client die Laufzeitartefakte erwartet. Die linke Spalte ist die framework-interne Rolle des Artefakts und bleibt über alle Client Packs gleich.

| Rolle des Artefakts | Pfad bei diesem Client | Belegstatus |
|---|---|---|
| Wurzel-Anweisungsdatei | `<TBD>` | `<TBD>` |
| Regeldateien (Core-Kurzfassungen, Overlay, Packs) | `<TBD: Pfad oder „kein Äquivalent">` | `<TBD>` |
| Skills | `<TBD>` | `<TBD>` |
| Subagentenprofile | `<TBD: Pfad oder „kein Äquivalent">` | `<TBD>` |
| Berechtigungskonfiguration | `<TBD>` (erzeugt aus `framework/runtime/permissions.json`) | `<TBD>` |
| Hook-Konfiguration | `<TBD: eigene Datei, derselbe Pfad wie die Berechtigungsdatei, oder „kein Äquivalent">` | `<TBD>` |
| MCP-Konfiguration | `<TBD>` | `<TBD>` |
| Projektverzeichnis-Variable in Hooks | `<TBD: z. B. Name der Umgebungsvariable>` | `<TBD>` |
| Nutzerlokale Überschreibung | `<TBD>` | `<TBD>` |

## 1a. Semantikabbildung der Berechtigungen und Hooks

Die Regelmenge liegt werkzeugneutral im Kern (`leitwerk-core/framework/runtime/permissions.json`, `hooks.json`) und wird bei der Installation übersetzt (D-18). Diese Tabelle ist die menschenlesbare Fassung der Abbildungsfelder im `manifest.json`.

| Neutrales Werkzeugverb | Werkzeug bei diesem Client | Anmerkung |
|---|---|---|
| `read` | `<TBD>` | |
| `search` | `<TBD: Werkzeug oder „kein Äquivalent">` | ohne Äquivalent entfällt nur die `allow`-Regel |
| `write` | `<TBD: ein Werkzeug oder getrennte für Ändern und Anlegen>` | |
| `exec` | `<TBD>` | wörtlich oder präfixbasiert? |
| `fetch` | `<TBD>` | |
| `mcp` | `<TBD>` | |

| Weitere Eigenschaft | Wert |
|---|---|
| Name ohne Verzeichnisanteil | `<TBD: mit oder ohne Wurzelangabe>` |
| Zusätzliche Schlüssel | `<TBD: z. B. ein Standardmodus>` |
| Hook-Werkzeugnamen | `<TBD>` |
| Projektverzeichnis im Hook-Befehl | `<TBD: Name der Umgebungsvariable>` |

Drei Zusicherungen werden erzwungen und sind nicht verhandelbar: Eine `deny`- oder `ask`-Regel ohne Zielwerkzeug lässt die Installation scheitern (Weglassen wäre eine Lockerung); die Präfixform eines Befehlsverbots muss ein Präfix seiner wörtlichen Form sein; bei `allow` müssen beide Formen übereinstimmen. Lässt sich eine Kernzusage danach nicht abbilden, gehört sie in Abschnitt 4 und nicht in eine Ausnahme im Code.

## 2. Fähigkeitsmatrix

Einstufung je Zusage: `[TECHNISCH]` erzwungen · `[TEXTUELL]` nur Anweisung · `[NICHT ABBILDBAR]` kein Mechanismus. Regeln in `../README.md` Abschnitt 4.

### R – Regelladung

| ID | Zusage des Frameworks | Quelle | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|---|
| R1 | Die Wurzel-Anweisungsdatei wird zu Beginn jeder Sitzung ungefragt geladen | `AGENTS.md` | `<TBD>` | `<TBD>` | `<TBD>` |
| R2 | Weitere Regeldateien lassen sich mit Ladebedingungen versehen (immer, bei Relevanz, manuell) | Laufzeit-README, Abschnitt „Regelablage" | `<TBD>` | `<TBD>` | `<TBD>` |
| R3 | Regeln lassen sich an Dateimuster binden, damit ein Technology Pack nur bei passenden Dateien lädt | Ebene 5 | `<TBD>` | `<TBD>` | `<TBD>` |
| R4 | Regelinhalte unterliegen einem bekannten Zeichenlimit, das das Framework einhalten kann | Laufzeit-README der Regelablage | `<TBD>` | `<TBD>` | `<TBD>` |
| R5 | Die geladenen Regelquellen sind vollständig aufzählbar | D-34, `CR-2026-031` | `<TBD>` | `<TBD>` | `<TBD>` |
| R6 | Das Framework importiert keine Regel- und Skillquellen fremder Werkzeugformate | D-37, `CR-2026-038` | `<TBD>` – kennt der Client keine Importsteuerung, ist die Zeile `[NICHT ABBILDBAR]`, und es bleibt bei der Auskunft in Abschnitt 7 | `<TBD>` | `<TBD>` |

### S – Skills

| ID | Zusage des Frameworks | Quelle | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|---|
| S1 | Standardaufgaben liegen als versionierte Skills im Repository | `leitwerk-core/framework/core/08-skill-conventions.md` | `<TBD>` | `<TBD>` | `<TBD>` |
| S2 | Ein Skill ist gezielt aufrufbar | dito | `<TBD>` | `<TBD>` | `<TBD>` |
| S3 | Ein Skill kann die ihm erlaubten Werkzeuge einschränken (lesende Skills schreiben nicht) | dito | `<TBD>` | `<TBD>` | `<TBD>` |
| S4 | Schreibende Skills sind nur benutzergetriggert, nicht modellgetriggert – die Zusage gilt für die Skill-Ablage, die das Framework schreibt | dito | `<TBD>` | `<TBD>` | `<TBD>` |
| S5 | Die geladenen Skills sind vollständig aufzählbar, samt Herkunft und Aufrufbarkeit | `CR-2026-032` | `<TBD>` | `<TBD>` | `<TBD>` |

### B – Berechtigungen

> **`[TECHNISCH]` heißt in diesem Block:** Die Engine setzt die Regel durch, **solange der Betriebsmodus die Berechtigungsprüfung nicht abschaltet.** Im Modus ohne Rückfragen, den D-05 untersagt, ist diese Linie bei mindestens einem Client nachweislich aus; dann trägt allein der Schutz-Hook (D-35, `AP2-DD-12`). Diese Vorbemerkung ist **Pflicht** in jedem Pack; sie ist je Client um den eigenen Belegstand zu ergänzen – erhoben oder ausdrücklich nicht erhoben.

Die mit **Kern** markierten Zeilen entsprechen `_core_rules_integrity` in der Berechtigungsdatei. Eine Abweichung von `[TECHNISCH]` ist dort begründungspflichtig.

| ID | Zusage des Frameworks | Kern | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|---|
| B1 | Berechtigungen liegen versioniert im Repository, nicht nur je Arbeitsplatz | ja | `<TBD>` | `<TBD>` | `<TBD>` |
| B2 | Dreistufige Semantik: verweigern vor rückfragen vor erlauben | ja | `<TBD>` | `<TBD>` | `<TBD>` |
| B3 | Lesezugriff auf Secret-Dateien ist per Pfadmuster verweigerbar (`.env`, `*.pem`, `*.key`, `secrets/**`) | ja | `<TBD>` | `<TBD>` | `<TBD>` |
| B4 | Schreibzugriff auf Framework- und Overlay-Artefakte ist verweigerbar, einschließlich des Kernverzeichnisses als Ganzes | ja | `<TBD>` | `<TBD>` | `<TBD>` |
| B5 | Schreibzugriff auf CI-, Quality-Gate- und Lockdateien ist verweigerbar | ja | `<TBD>` | `<TBD>` | `<TBD>` |
| B6 | Befehle sind per Muster verweigerbar (`git push`, `git merge`, `rm -rf`, `sudo`) | ja | `<TBD>` | `<TBD>` | `<TBD>` |
| B7 | Schreiboperationen lösen standardmäßig eine Rückfrage aus | – | `<TBD>` | `<TBD>` | `<TBD>` |
| B8 | Netzwerkzugriff ist standardmäßig unterbunden | – | `<TBD>` | `<TBD>` | `<TBD>` |
| B9 | Eine nutzerlokale Konfiguration kann nur verschärfen, nicht lockern | – | `<TBD>` | `<TBD>` | `<TBD>` |

### H – Hooks

| ID | Zusage des Frameworks | Quelle | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|---|
| H1 | Vor einer Werkzeugausführung kann eine eigene Prüfung laufen | Hook-Konfiguration | `<TBD>` | `<TBD>` | `<TBD>` |
| H2 | Diese Prüfung kann die Ausführung **blockieren** (nicht nur protokollieren) | dito | `<TBD>` | `<TBD>` | `<TBD>` |
| H3 | Beim Sitzungsstart kann eine Statusmeldung erzeugt werden (Overlay aktiv, Version) | dito | `<TBD>` | `<TBD>` | `<TBD>` |

### A – Agentenprofile

| ID | Zusage des Frameworks | Quelle | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|---|
| A1 | Ein rein lesendes Reviewprofil ist definierbar | `.devin/agents/fw-reviewer.md` | `<TBD>` | `<TBD>` | `<TBD>` |

### M – Modi und Sitzungsfreigaben

| ID | Zusage des Frameworks | Quelle | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|---|
| M1 | Es gibt einen Standardmodus, der bei Schreiben und Befehlen rückfragt | D-05 | `<TBD>` | `<TBD>` | `<TBD>` |
| M2 | Ein Modus, der alle Rückfragen übergeht, lässt sich organisatorisch oder technisch ausschließen | D-05 | `<TBD>` | `<TBD>` | `<TBD>` |
| M3 | Eine erteilte Freigabe lässt sich auf die Sitzung begrenzen, statt sie dauerhaft zu speichern | Laufzeit-README | `<TBD>` | `<TBD>` | `<TBD>` |
| M6 | Ein Modus mit automatischer Übernahme von Dateiänderungen lässt sich begrenzen | D-05 | `<TBD>` | `<TBD>` | `<TBD>` |
| M7 | Ein Modus, der selbst beurteilt, was sicher ist, lässt sich begrenzen | D-05 | `<TBD>` | `<TBD>` | `<TBD>` |

### X – Externe Anbindung

| ID | Zusage des Frameworks | Quelle | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|---|
| X1 | Externe Systeme sind standardmäßig nicht angebunden; jede Anbindung ist eine Einzelfreigabe | K-10, D-10 | `<TBD>` | `<TBD>` | `<TBD>` |
| X2 | Ob und wohin Quellcode zur Indexierung abfließt, ist bekannt und dokumentiert | K-20 | `<TBD>` | `<TBD>` | `<TBD>` |

## 3. Zusammenfassung der Durchsetzungstiefe

| Klasse | Anzahl | davon Kernzusagen |
|---|---|---|
| `[TECHNISCH]` | `<TBD>` | `<TBD>` |
| `[TEXTUELL]` | `<TBD>` | `<TBD>` |
| `[NICHT ABBILDBAR]` | `<TBD>` | `<TBD>` |

## 4. Kernzusagen ohne technische Durchsetzung

Jede Kernzusage (Spalte **Kern** = ja) mit einer anderen Einstufung als `[TECHNISCH]` wird hier einzeln geführt. Ohne Eintrag in dieser Tabelle darf das Pack nicht in Betrieb gehen.

| ID | Einstufung | Warum der Client das nicht durchsetzt | Ersatzmaßnahme | Freigabe |
|---|---|---|---|---|
| `<TBD>` | `<TBD>` | `<TBD>` | `<TBD: z. B. Hook, externe Prüfung, verschärfter Prozessschritt>` | `<SECURITY_CONTACT>` |

## 5. Bekannte Abweichungen im Verhalten

`<TBD: Was sich gegenüber anderen Client Packs unterscheidet, ohne eine Zusage zu verletzen – etwa fehlende Ladetrigger, andere Skill-Auffindung, abweichende Frontmatter-Felder>`

## 6. Installation und Prüfung

```text
python leitwerk-core/install.py --client <TBD: Kurzname>
python leitwerk-core/tests/scripts/validate-framework.py
```

Vor der ersten produktiven Nutzung sind die Basistests des Testkatalogs (`leitwerk-core/tests/TEST_CATALOG.md`, Kennzeichnung „Basis") gegen diesen Client zu fahren und zu protokollieren.

## 7. Anweisungs- und Konfigurationsquellen außerhalb des Projekts

**Pflichtabschnitt.** Er führt, was dieser Client aus Ablagen **außerhalb des Repositoriums** lädt. Solche Quellen haben nach Regel 2.6 der Prioritätshierarchie **keine Ebene**: Sie dürfen einschränken, nie über die Ebenen 1 bis 4 hinaus erweitern und keine Governance-, Datenschutz- oder Sicherheitsregeln setzen (D-34). Prüfung 19 meldet ein Pack ohne diesen Abschnitt.

**Erhebungsstand: `<TBD: JJJJ-MM-TT>`**, Clientversion `<TBD>`, erhoben mit `<TBD: Kommandos oder Messweg>`.

### 7.1 Anweisungsquellen

Regeltexte, Skills, Agentenprofile. Je bekannter Quelle eine Zeile – **oder** die ausdrückliche Angabe „keine bekannt" mit Datum und Erhebungsweg. Ein Abwesenheitsbeleg ist ein Ergebnis; ein leerer Abschnitt ist keines.

| Quelle | Ladebedingung | Belegstatus | Maßnahme des Frameworks |
|---|---|---|---|
| `<TBD: Pfad>` | `<TBD>` | `<TBD>` | `<TBD>` |

### 7.2 Konfigurationsquellen

Berechtigungen, Hooks und Einstellungen außerhalb des Repositoriums – sie betreffen genau die Linien, auf denen B1 bis B6 stehen (`CR-2026-038`).

| Quelle | Wirkung | Belegstatus |
|---|---|---|
| `<TBD: Pfad>` | `<TBD>` | `<TBD>` |

### 7.3 Was dieser Abschnitt nicht leistet

**Eine Auskunft ist keine Schranke**, und ein **Abwesenheitsbeleg altert**: Am Tag der nächsten Clientversion ist er eine Aussage über die Vergangenheit. Prüfung 19 prüft die **Anwesenheit** dieser Auskunft, nicht ihre Richtigkeit – die hängt an einer Erhebung, nicht an einem Skript.

## 8. Änderungsverlauf

| Version | Datum | Änderung | Autor (Rolle) |
|---|---|---|---|
| 0.1.0 | `<TBD>` | angelegt | `<TBD>` |
