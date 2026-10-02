# Architekturentscheidungen (Rückfallablage)

Eine Datei je Entscheidung: `ADR-<JJJJ-MM-TT>-<kurzname>.md` mit Kontext, Entscheidung, Alternativen, Folgen und Status. Zwei Arbeitsplätze, die zugleich entscheiden, erzeugen zwei Dateien statt eines Merge-Konflikts (Overlay Abschnitt 13.1). Jede Datei wird im Overlay-Manifest registriert. Ist `<DOCUMENTATION_PLATFORM>` führend, liegt hier höchstens ein Verweisblatt.
