# 28 Vorgehen zur Übernahme in weitere Projekte

Die Übernahme ist als wiederholbarer, geprüfter Vorgang gestaltet: Ein Projekt übernimmt ein Framework-**Release** in das Repository-Wurzelverzeichnis, füllt ausschließlich die Overlay-Bestandteile, härtet projektlokal (Sperrbegriffe, zusätzliche Pfadsperren), validiert strikt, besteht die Basistests des Testkatalogs, organisiert Rollen und Onboarding – und setzt erst dann den Overlay-Status auf `aktiv` (verbindlicher Nachweis: Checkliste FW-CL-10, Kap. 22.10). Aktualisierungen auf neue Releases ersetzen die Core-Bestandteile byte-gleich und prüfen die Overlay-Kompatibilität anhand der Migrationshinweise; Mehr-Repository-Projekte und der spätere Werkzeugwechsel sind geregelt.

{{EMBED-RAW:leitwerk-core/docs/ADOPTION_GUIDE.md:1}}
