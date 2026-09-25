# Definition of Done – allgemeine Kriterien

> **Muster – vom Overlay Owner zu prüfen und anzupassen.** Mitgeliefert mit dem
> Overlay-Muster `general` und im Manifest mit Status `entwurf` registriert. Verbindlich
> wird das Dokument erst, wenn der Overlay Owner es freigibt und in der Laufzeitfassung
> als K1-Dokument führt; bis dahin ist es ein Vorschlag.
>
> Es enthält nur, was auf jedes Softwareprojekt passt: keine Abdeckungsgrenzen, keine
> Werkzeuge, keine Freigabestufen. Was das Projekt zusätzlich verlangt, gehört unten in
> die projektspezifischen Ergänzungen.

## Verhältnis zum Framework

Diese Kriterien sind die **projektweite** Definition of Done, auf die `OVERLAY.md`
Abschnitt 12 verweist. Für Aufgaben mit dem KI-Client gilt **zusätzlich**
`.koolie/core/framework/core/04-quality.md` Abschnitt 3 – Ergebnisbericht, Selbstreview
nach der Review-Checkliste, KI-Nutzungsvermerk. Diese Punkte werden hier nicht
wiederholt.

## Kriterien

Eine Aufgabe ist erledigt, wenn:

1. **Die Akzeptanzkriterien sind erfüllt** und die Erfüllung ist nachvollziehbar belegt.
2. **Die Änderung ist getestet.** Neue und geänderte Logik ist durch automatisierte
   Tests abgesichert, die Verhalten prüfen; nicht automatisierbare Anteile sind mit einem
   beschriebenen Prüfschritt geprüft.
3. **Alle Prüfungen des Projekts sind grün** – Build, Tests, Analyse, Quality Gate.
   Keine Prüfung wurde abgeschaltet oder abgeschwächt, um das zu erreichen.
4. **Die Änderung ist begutachtet.** Ein Review hat stattgefunden, seine Befunde sind
   aufgelöst oder mit Begründung zurückgestellt.
5. **Keine neuen Warnungen**, und keine bekannten Fehler ohne Vermerk.
6. **Die Dokumentation ist nachgezogen**: Nutzerdokumentation, Schnittstellenbeschreibung,
   Betriebshinweise und Änderungsprotokoll, soweit die Änderung sie berührt.
7. **Die Änderung ist integriert** in den Standard-Branch oder in den Zweig, den das
   Projekt dafür vorsieht, und der integrierte Stand ist baubar.
8. **Offene Punkte sind sichtbar.** Bewusst eingegangene Vereinfachungen, technische
   Schulden und Folgeaufgaben sind erfasst, nicht nur bekannt.
9. **Nichts Überflüssiges bleibt zurück**: keine Debug-Ausgaben, keine temporären
   Dateien, kein toter Code aus der Umsetzung.

## Umgang

- „Fast fertig“ ist nicht fertig. Eine Aufgabe, die ein Kriterium verfehlt, bleibt
  offen oder wird mit dem verbleibenden Rest als neue Aufgabe geteilt.
- Wird ein Kriterium dauerhaft nicht erfüllt, wird die Definition geändert – offen und
  mit Begründung –, nicht stillschweigend übergangen.

## Projektspezifische Ergänzungen

`<TBD: zusätzliche Kriterien des Projekts, zum Beispiel fachliche Abnahme, Freigabe
durch eine Rolle, Bereitstellung in einer Testumgebung>`
