# 28 Vorgehen zur Übernahme in weitere Projekte

Die Übernahme ist ein wiederholbarer, geprüfter Vorgang. Ein Projekt übernimmt ein Framework-**Release**, und zwar nur den Kern `.koolie/core/`, nie ganz `.koolie/`:

1. **Installieren** – über eine Paketquelle (`uvx koolie`, `pipx run koolie` oder `npx @renoxar/koolie` im Projektverzeichnis), über den Starter `install.cmd` (Windows) beziehungsweise `install.command` (macOS) aus dem Release-Archiv oder direkt mit `install.py --target`. Dabei entstehen die Wurzelbestandteile des gewählten Client Packs; `--lieferumfang nutzung` kopiert den Kern ohne Nachweisschicht.
2. **Overlay füllen** – nur die Overlay-Bestandteile; dazu projektlokal härten (Sperrbegriffe, zusätzliche Pfadsperren).
3. **Prüfen** – strikt validieren und die Basistests des Testkatalogs bestehen.
4. **Organisieren** – Rollen besetzen, Onboarding durchführen.
5. **Aktivieren** – erst dann den Overlay-Status auf `aktiv` setzen. Verbindlicher Nachweis ist die Checkliste FW-CL-10 (Kap. 22.10).

Ein neues Release ersetzt `.koolie/core/` als Ganzes (`install.py --target … --update` oder Kopie plus `install.py --update`), zieht die Wurzelbestandteile nach und prüft die Overlay-Kompatibilität anhand der Migrationshinweise. Mehr-Repository-Projekte und der spätere Werkzeugwechsel sind geregelt. Abschnitt 8 nennt, was die Umgebung neben Koolie tragen muss (verwaltete Einstellungen, Branch-Schutz und CI, Isolation), regelt das Nebeneinander mit einem anderen Agenten-Rahmenwerk und berichtet die Vergleichsmessung gegen eine gute Standardkonfiguration.

{{EMBED-RAW:.koolie/core/docs/ADOPTION_GUIDE.md:1}}
