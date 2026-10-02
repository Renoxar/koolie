# 26 Qualitätssicherung und Testkonzept des Frameworks

Das Framework selbst wird auf zwei Wegen geprüft: statisch und in Testsitzungen.

**Statisch** prüft `.koolie/core/tests/scripts/validate-framework.py` Struktur und Inhalte:

- Pflichtdateien, Frontmatter und Trigger der Regeln, Zeichenlimits;
- Skill-Konformität: Pflichtdateien, Metadaten, Pflichtabschnitte, Trigger-Regel für schreibende Skills, Beispiel- und Testpflichten;
- JSON-Gültigkeit und Kernregel-Integrität der Berechtigungen, Manifest-Schema, Platzhalterregister;
- verbotene Inhalte: Secret-Muster, E-Mail-Adressen, IP-Adressen, interne Hostnamen, URLs außerhalb der Quellen-Allowlist und die projektlokalen Sperrbegriffe aus `.koolie/project-overlay/forbidden-terms.txt`;
- mit `--mermaid` die Syntax aller Diagramme, mit `--strict-overlay` die Aktivierungsreife eines Overlays.

`.koolie/core/tests/scripts/validate-output.py` prüft konkrete Ausgaben gegen das Ausgabeformat des jeweiligen Skills; die Hook-Skripte haben Selbsttests. Der Lauf zum Stand dieser Dokumentfassung: 0 Fehler, 0 Warnungen. Der Validator führt **113 Prüfungen** über 680 versionierte Dateien des Kerns, davon 571 Markdown-Dateien. Das Register der Prüfungen steht im Kopfkommentar des Skripts; Prüfung 40 zählt es gegen den Bestand nach, Prüfung 78 diese drei Zahlen.

Jede Prüfung hat einen eigenen Wirkungsnachweis: `.koolie/core/tests/scripts/probe-pruefungen.py` legt je Prüfung einen Fehlerfall an und verlangt die Meldung, dazu eine Gegenprobe, die den korrekten Träger durchlaufen lässt. Eine Prüfung ohne Sonde gilt als nicht vorhanden. Die acht Mermaid-Blöcke (sechs Entscheidungsbäume, das Architekturdiagramm aus Kap. 7 und das Roadmap-Diagramm) prüft `--mermaid`; der Schalter setzt das Mermaid-Kommandozeilenwerkzeug voraus.

**In Testsitzungen** prüft der Testkatalog das Verhalten auf dem synthetischen Übungsrepository, in zwölf Klassen:

| Kürzel | Klasse |
|---|---|
| KO | Konsistenz und Widerspruchserkennung |
| PO | Positivtests |
| NE | Negativtests |
| DS | Datenschutz |
| PI | Prompt Injection |
| SC | Scope-Einhaltung |
| FI | Verhalten bei fehlenden Informationen |
| ZA | unerlaubte Datei- und Befehlszugriffe |
| RE | Regression bei Framework-Änderungen |
| VN | Versionsnachvollziehbarkeit |
| AK | Aktualität gegenüber Produktänderungen des Clients |
| EX | externe Systeme über MCP |

Die Testfälle der Skills in den `TESTS.md`-Dateien (je Skill mindestens zwei Positiv- und drei Negativtests) gehören zum Katalog. Den Stand der Ergebniszellen rechnet Prüfung 46 bei jedem Lauf aus; er steht in der Roadmap (Kap. 30).

**Was ein `bestanden` sagt.** Es sagt, dass das erwartete Verhalten eingetreten ist – nicht, dass das Framework es bewirkt hat. Die Zurechnung trägt ein eigener Kontrolllauf gegen einen Baum ohne die geprüfte Schranke; wo er fehlt, sagt die Zelle es. Jede Zelle nennt das gemessene Client Pack mit Produktstand: Ein Ergebnis gilt für den Client, an dem es erhoben wurde. Ausführungsdisziplin und Protokollpflicht sind im Katalog geregelt.

{{EMBED-RAW:.koolie/core/tests/TEST_CATALOG.md:1}}
