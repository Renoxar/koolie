# 8 Trennung zwischen Core und Projektkonfiguration

## 8.1 Das Trennprinzip

Die Wiederverwendbarkeit des Frameworks steht und fällt mit einer harten Regel: **Ein Projektwechsel tauscht ausschließlich Ebene 4 (Project Overlay); er darf niemals Anpassungen am Framework Core erzwingen.** Umgekehrt enthält der Core keine einzige projektspezifische Angabe – wo er Projektwissen braucht, definiert er eine benannte Schnittstelle in Form eines registrierten Platzhalters (`<ALLOWED_PATHS>`, `<TEST_COMMAND>`, `<APPROVAL_ROLE>` …), die das Overlay füllt.

## 8.2 Mechanik der Trennung

| Mechanismus | Wirkung |
|---|---|
| Platzhalter-Schnittstellen (Anhang 31.2) | Core-Regeln bleiben generisch formulierbar; Projekte füllen Werte ausschließlich im Overlay und in `.devin/config.json` |
| Verschärfungsprinzip (Kap. 25) | Das Overlay darf konkretisieren und verschärfen, nie lockern – Core-Garantien gelten damit projektübergreifend |
| Getrennte Ablage und Ownership | Core: Framework Owner über Releases; Overlay: Overlay Owner über den Projektprozess; technische Schreibsperren (`Write(devin-core-framework/framework/**)`, `Write(.devin/**)`, `Write(AGENTS.md)`, `Write(project-overlay/**)` als `deny` für Devin) |
| Dokumenten-Manifest | Projektwissen wird als registriertes Dokument mit Klasse und Ladeverhalten eingebunden – nie durch Editieren von Core-Dateien (Kap. 17) |
| Integritätsprüfung | `validate-framework.py` prüft unter anderem, dass die Kernregeln in `.devin/config.json` unverändert enthalten sind (`_core_rules_integrity`) und Overlay-Pflichtfelder gefüllt sind (`--strict-overlay`) |
| Release-Abgleich | Bei Übernahme und Aktualisierung werden Core-Bestandteile byte-gleich aus dem Release übernommen (Adoption Guide, CL-10/CL-11) |

## 8.3 Grenzfälle und ihre Auflösung

Regeln mit gemischtem Charakter werden getrennt: die generische Logik wandert mit Platzhalter in den Core, der Wert in das Overlay (**Beispiel (synthetisch):** „Devin führt nur freigegebene Testbefehle aus" ist Core; „der Testbefehl lautet `build-tool test`" ist Overlay). Stellt ein Projekt fest, dass eine Core-Regel für alle denkbaren Projekte falsch oder unvollständig ist, ist das ein Änderungsantrag an den Framework Owner – bis zur Entscheidung gilt die Regel oder eine dokumentierte, befristete Ausnahme (nie eine stille lokale Abweichung). Die vollständige Einordnungslogik – einschließlich Ebene B (Organisationsvorgaben werden eingebunden, nicht kopiert) und Ebene E (Aufgabenkontext bleibt außerhalb des Repositorys) – bildet Entscheidungsbaum 6 ab (Kap. 23).

## 8.4 Nachweis der Trennung in dieser Erstfassung

Alle 155 Markdown-Dateien des Referenz-Repositorys wurden automatisiert auf Projektneutralität geprüft (Sperrbegriffs-, E-Mail-, IP-, Hostnamen- und URL-Prüfungen; Kap. 26); sämtliche variablen Inhalte laufen über das Platzhalterregister; das Overlay ist eine reine Vorlage mit Ausfüllhinweisen und `<TBD>`-Feldern. Synthetische Beispiele sind als solche gekennzeichnet und verwenden offensichtlich fiktive Bezeichner.
