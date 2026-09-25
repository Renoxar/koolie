# Qualität – allgemeine Grundsätze für Tests und Review

> **Muster – vom Overlay Owner zu prüfen und anzupassen.** Mitgeliefert mit dem
> Overlay-Muster `general` und im Manifest mit Status `entwurf` registriert. Verbindlich
> wird das Dokument erst, wenn der Overlay Owner es freigibt und in der Laufzeitfassung
> als K1-Dokument führt; bis dahin ist es ein Vorschlag.
>
> Es enthält nur, was auf jedes Softwareprojekt passt: keine Abdeckungsgrenzen, keine
> Testwerkzeuge, keine Anzahl Reviewer. Welche Prüfungen das Projekt führt und wie
> streng sie sind, steht in `OVERLAY.md` Abschnitt 7.

## Verhältnis zum Framework

Für Änderungen mit dem KI-Client gelten zusätzlich `.koolie/core/checklists/05-testing.md`
(Aussagekraft und Integrität der Tests) und `.koolie/core/framework/core/07-review-rules.md`
(Prüfpunkte für KI-generierte Änderungen). Beide werden hier nicht wiederholt. Dieses
Dokument beschreibt die Grundsätze, die für **jede** Änderung gelten.

## 1. Tests

1. Tests sind Teil der Änderung, nicht ihr Nachtrag. Wer Verhalten ändert, ändert oder
   ergänzt den Test, der es beschreibt.
2. Ein gemeldeter Fehler wird zuerst durch einen Test nachgestellt, der fehlschlägt, und
   dann behoben. So bleibt er behoben.
3. Tests laufen schnell und lokal, damit sie oft laufen. Langsame Prüfungen werden
   getrennt, nicht weggelassen.
4. Ein Test, der manchmal fehlschlägt, ist ein Fehler – im Test oder im Code – und wird
   behoben. Er wird nicht wiederholt, bis er grün ist.
5. Getestet wird auf der niedrigsten Ebene, die das Verhalten zuverlässig zeigt;
   übergreifende Tests prüfen das Zusammenspiel, nicht jede Einzelheit noch einmal.
6. Testcode ist Code: Er folgt denselben Grundsätzen der Lesbarkeit und wird gepflegt.

## 2. Review

1. Jede Änderung wird von mindestens einer weiteren Person gelesen, bevor sie
   integriert wird. Die Verantwortung für die Änderung bleibt bei ihrer Autorin oder
   ihrem Autor.
2. Reviews sind klein und zeitnah. Eine Änderung, die zu groß zum Prüfen ist, wird
   geteilt.
3. Befunde betreffen den Code, nicht die Person, und sind begründet. Muss-Befunde und
   Anregungen werden unterscheidbar markiert.
4. Das Review prüft, was Werkzeuge nicht prüfen können: Verständlichkeit, fachliche
   Richtigkeit, Entwurf, Randfälle, Sicherheit. Stil und Formatierung prüft das Werkzeug.
5. Wer eine Änderung nicht versteht, gibt sie nicht frei.

## 3. Qualitätsprüfungen

1. Die automatischen Prüfungen des Projekts laufen bei jeder Änderung, und ein roter
   Lauf blockiert die Integration.
2. Schwellenwerte und Regeln der Prüfungen werden nur über den regulären Prozess des
   Projekts geändert, nie im Zuge einer Änderung, um sie passieren zu lassen.
3. Technische Schulden werden sichtbar geführt und bewusst abgebaut, nicht nur bemerkt.
4. Wiederkehrende Fehlerarten führen zu einer neuen Prüfung oder Regel, nicht nur zu
   einer weiteren Korrektur.

## Projektspezifische Ergänzungen

`<TBD: Festlegungen des Projekts, zum Beispiel Testebenen, Anzahl Reviewer, fachliche
Abnahme>`
