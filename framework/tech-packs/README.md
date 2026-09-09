# Technology Packs (Ebene 5 der Prioritätshierarchie)

Technology Packs sind optionale technologische Ergänzungen: Programmiersprache, Anwendungsframework, Build-System, Testframework, Datenbank, API-Technologie, Frontend, Backend, Container, CI/CD. Sie beschreiben, **wie** in einer Technologie korrekt gearbeitet wird – nicht, was erlaubt ist (Core) und nicht, welche Werte im Projekt gelten (Overlay).

## Verbindliche Regeln für Technology Packs

1. Keine Governance-, Datenschutz- oder Sicherheitsregeln mit Regelcharakter (diese stehen im Core); technologiespezifische **Sicherheitsmuster** (zum Beispiel typische Injection-Vektoren einer Technologie) sind zulässig und erwünscht.
2. Keine Projektwerte (Versionen, Pfade, Befehle des konkreten Projekts stehen im Overlay). Ein Pack beschreibt eine Technologie in der Version, für die es geschrieben wurde; die im Projekt eingesetzte Version wird im Overlay festgelegt.
3. Aufbau je Pack: `TECH_PACK.md` (Langform), optional `skills/` (Quellablage, Präfix `tech-<pack>-`) und eine Laufzeitfassung `.devin/rules/40-tech-<pack>.md` mit `trigger: glob` und den Dateimustern der Technologie.
4. Ein Pack wird im Overlay aktiviert (Abschnitt 8).
5. Ein Pack darf Core- und Overlay-Regeln nur konkretisieren oder verschärfen. Bei Widerspruch zwischen einem Technology Pack und einem Role Pack gilt das Technology Pack (Begründung: `governance/PRIORITY_HIERARCHY.md`).

## Verfügbare Packs

Die Erstfassung liefert bewusst kein technologiespezifisches Pack, da der Technologie-Stack des Zielprojekts (`<TECH_STACK>`) nicht Teil der generischen Erstfassung ist (`<TBD: erstes Technology Pack für <TECH_STACK>>`). Die Vorlage `_template/TECH_PACK.md` und `.devin/rules/40-tech-TEMPLATE.md.template` ermöglichen die Erstellung im Arbeitspaket „technische Referenzimplementierung".
