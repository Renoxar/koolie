# Kennzeichen des Quellrepositoriums

Diese Datei kennzeichnet das Repositorium von Koolie selbst – im Unterschied zu einem
Projekt, das Koolie übernommen hat. Ihr Inhalt ist nebensächlich; dass sie da ist, ist
die Aussage.

Der Validator erkennt an ihr, wo er läuft. Im Quellrepositorium prüft er alle
versionierten Dateien und die Lizenz an beiden Stellen; in einem Projekt nur das, was
ausgeliefert wird.

**In ein Projekt gehört sie nicht.** `install.py` kopiert nur `.koolie/core/` und legt
diese Datei nicht an. Wer von Hand ganz `.koolie/` kopiert, nimmt sie mit – dann meldet
`install.py` sie, und sie wird im Projekt gelöscht.
