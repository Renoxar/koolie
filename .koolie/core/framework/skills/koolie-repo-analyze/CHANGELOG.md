# koolie-repo-analyze – Änderungsverlauf

| Version | Datum | Änderung | Autor (Rolle) |
|---|---|---|---|
| 0.1.0 | 2026-09-01 | Erstfassung (Status entwurf) | Framework-Erstellung |
| 0.1.1 | 2026-09-10 | Pfadnennungen dem umbenannten Kernverzeichnis angepasst (`CR-2026-009`); Versionsanhebung nachgeholt (`CR-2026-015`) | `<FRAMEWORK_OWNER>` |
| 0.1.2 | 2026-09-10 | „Devin“ als Akteursbezeichnung durch den werkzeugneutralen Begriff „KI-Client“ ersetzt (`CR-2026-020`) | `<FRAMEWORK_OWNER>` |
| 0.1.3 | 2026-09-13 | Vorbedingung nennt neben dem Übungsrepositorium das Quellrepositorium des Frameworks (`CR-2026-053`, B07, D-56) | `<FRAMEWORK_OWNER>` |
| 0.1.4 | 2026-09-19 | Version der Ausgabevorlage wird aus dem Steckbrief abgeleitet statt gepflegt (`CR-2026-094`, D-185) | `<FRAMEWORK_OWNER>` |
| 0.1.5 | 2026-09-22 | Pfadnennungen der Umbenennung auf `Koolie` angepasst; Kernverzeichnis `.koolie/core/`, Overlay `.koolie/project-overlay/` (`CR-2026-122`, D-299). **Keine Anweisung beruehrt** - die Zellen des Testblatts bleiben abgenommen (D-303) | `<FRAMEWORK_OWNER>` |
| 0.1.6 | 2026-10-02 | Art: *Namensanpassung*. Der Skill heißt `koolie-repo-analyze` (bis 1.25.0 `fw-repo-analyze`); mitgelieferte Skills tragen das Präfix `koolie-` (`CR-2026-173`, D-539). **Keine Anweisung berührt** – die Zellen des Testblatts bleiben abgenommen (D-303) | `<FRAMEWORK_OWNER>` |
| 0.1.7 | 2026-10-06 | Art: *Anweisung*. Die lesenden Git-Befehle (`git status`, `git diff`, `git log`, `git show`, `git blame`) sind erlaubt; `exec` steht nicht mehr in `permissions.deny`, wird aber nicht vorab freigegeben – die Shell folgt den Regeln der Sitzung (`CR-2026-175` E4). **Anweisung berührt** – die Zellen des Testblatts sind offen und werden nachgemessen (D-303) | `<FRAMEWORK_OWNER>` |
| 0.1.8 | 2026-10-06 | Art: *Anweisung*. Eine Datei, die als K3 gekennzeichnet ist oder nach Name, Kennzeichnung oder Suchergebnis K3 enthält, wird nicht geöffnet und nur als Fundstelle genannt; die Analyse des übrigen Bestands geht weiter. Anlass: Im Nachlauf zu `2.2.0` öffnete ein Lauf eine als K3 gekennzeichnete Fixture (`K-221`, `CR-2026-175`). **Anweisung berührt** – die Zellen des Testblatts werden nachgemessen (D-303) | `<FRAMEWORK_OWNER>` |
