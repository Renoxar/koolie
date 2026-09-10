# Client Pack `<CLIENT_PACK_NAME>` – Vorlage

<!-- AUSFÜLLHINWEIS: Kopiere dieses Verzeichnis nach ../<client-name>/, ersetze alle Platzhalter
     und lege ../<client-name>/root-template/ mit den Wurzelartefakten dieses Clients an.
     Trage das Pack in ../README.md Abschnitt 6 und in devin-core-framework/OWNERS.md ein.
     Ein Client Pack führt keine Verhaltensregeln ein (../README.md Abschnitt 2). -->

| Attribut | Wert |
|---|---|
| Modul-ID | `CP-<CLIENT_PACK_CODE>` |
| Ebene | keine – Abbildungsschicht |
| Version | 0.1.0 |
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

Die Regelmenge liegt werkzeugneutral im Kern (`devin-core-framework/framework/runtime/permissions.json`, `hooks.json`) und wird bei der Installation übersetzt (D-18). Diese Tabelle ist die menschenlesbare Fassung der Abbildungsfelder im `manifest.json`.

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
| R2 | Weitere Regeldateien lassen sich mit Ladebedingungen versehen (immer, bei Relevanz, manuell) | `.devin/rules/README.md` | `<TBD>` | `<TBD>` | `<TBD>` |
| R3 | Regeln lassen sich an Dateimuster binden, damit ein Technology Pack nur bei passenden Dateien lädt | Ebene 5 | `<TBD>` | `<TBD>` | `<TBD>` |
| R4 | Regelinhalte unterliegen einem bekannten Zeichenlimit, das das Framework einhalten kann | `.devin/rules/README.md` | `<TBD>` | `<TBD>` | `<TBD>` |

### S – Skills

| ID | Zusage des Frameworks | Quelle | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|---|
| S1 | Standardaufgaben liegen als versionierte Skills im Repository | `devin-core-framework/framework/core/08-skill-conventions.md` | `<TBD>` | `<TBD>` | `<TBD>` |
| S2 | Ein Skill ist gezielt aufrufbar | dito | `<TBD>` | `<TBD>` | `<TBD>` |
| S3 | Ein Skill kann die ihm erlaubten Werkzeuge einschränken (lesende Skills schreiben nicht) | dito | `<TBD>` | `<TBD>` | `<TBD>` |
| S4 | Schreibende Skills sind nur benutzergetriggert, nicht modellgetriggert | dito | `<TBD>` | `<TBD>` | `<TBD>` |

### B – Berechtigungen

Die mit **Kern** markierten Zeilen entsprechen `_core_rules_integrity` in der Berechtigungsdatei. Eine Abweichung von `[TECHNISCH]` ist dort begründungspflichtig.

| ID | Zusage des Frameworks | Kern | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|---|
| B1 | Berechtigungen liegen versioniert im Repository, nicht nur je Arbeitsplatz | ja | `<TBD>` | `<TBD>` | `<TBD>` |
| B2 | Dreistufige Semantik: verweigern vor rückfragen vor erlauben | ja | `<TBD>` | `<TBD>` | `<TBD>` |
| B3 | Lesezugriff auf Secret-Dateien ist per Pfadmuster verweigerbar (`.env`, `*.pem`, `*.key`, `secrets/**`) | ja | `<TBD>` | `<TBD>` | `<TBD>` |
| B4 | Schreibzugriff auf Framework- und Overlay-Artefakte ist verweigerbar | ja | `<TBD>` | `<TBD>` | `<TBD>` |
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
| M3 | Eine erteilte Freigabe lässt sich auf die Sitzung begrenzen, statt sie dauerhaft zu speichern | `.devin/README.md` | `<TBD>` | `<TBD>` | `<TBD>` |

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
python devin-core-framework/install.py --client <TBD: Kurzname>
python devin-core-framework/tests/scripts/validate-framework.py
```

Vor der ersten produktiven Nutzung sind die Basistests des Testkatalogs (`devin-core-framework/tests/TEST_CATALOG.md`, Kennzeichnung „Basis") gegen diesen Client zu fahren und zu protokollieren.

## 7. Änderungsverlauf

| Version | Datum | Änderung | Autor (Rolle) |
|---|---|---|---|
| 0.1.0 | `<TBD>` | angelegt | `<TBD>` |
