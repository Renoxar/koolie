# Kennzeichen des Quellrepositoriums

Diese Datei kennzeichnet das **Framework-Repositorium selbst** – im Unterschied zu einem
Projekt, das das Framework übernommen hat. Sie trägt keinen Inhalt, der gelesen werden
muss; ihr **Vorhandensein** ist die Aussage (D-351).

Der Validator unterscheidet an ihr, wo er läuft. Im Quellrepositorium prüfen die
Prüfungen 75 und 81 alle versionierten Dateien und Prüfung 79 die Lizenz an beiden
Stellen; in einem übernehmenden Projekt beschränken sie sich auf das Ausgelieferte, und
Prüfung 78 enthält sich.

**Sie wandert nicht in ein Projekt.** Sie liegt neben dem Kern, nicht in ihm: Das Heben
kopiert nur `.koolie/core/`, und `install.py` legt sie nicht an. Bis `1.4.0` war dieses
Kennzeichen die Übergabe `UEBERGABE.md`; seit `1.4.1` ist die Übergabe ein lokales
Arbeitsdokument und nicht mehr versioniert (D-350).
