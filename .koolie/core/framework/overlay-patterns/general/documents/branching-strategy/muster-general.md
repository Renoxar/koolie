# Branching und Integration – allgemeine Grundsätze

> **Muster – vom Overlay Owner zu prüfen und anzupassen.** Mitgeliefert mit dem
> Overlay-Muster `general` und im Manifest mit Status `entwurf` registriert. Verbindlich
> wird das Dokument erst, wenn der Overlay Owner es freigibt und in der Laufzeitfassung
> als K1-Dokument führt; bis dahin ist es ein Vorschlag.
>
> Es enthält nur, was auf jedes Softwareprojekt passt, und legt **kein** Branching-Modell
> fest. Modell, Standard-Branch, Namensschema, Commit-Konvention und Merge-Strategie
> stehen in `OVERLAY.md` Abschnitt 10.

## Verhältnis zum Framework

Für den KI-Client gilt zusätzlich: Er arbeitet nie auf einem geschützten Branch, und
Push sowie Merge Request erfolgen durch den Menschen
(`.koolie/core/checklists/03-before-code-change.md`,
`.koolie/core/checklists/08-merge-request.md`). Das wird hier nicht wiederholt.

## Grundsätze

1. **Der Standard-Branch ist jederzeit baubar** und besteht die Prüfungen des Projekts.
   Wer ihn bricht, repariert ihn vorrangig.
2. **Branches leben kurz.** Je länger ein Branch vom Standard-Branch getrennt ist, desto
   teurer wird seine Integration. Große Vorhaben werden in kleine, einzeln
   integrierbare Schritte zerlegt.
3. **Integriert wird über einen Merge Request** mit Review und grünen Prüfungen, nicht
   durch direktes Schreiben auf geschützte Branches.
4. **Eine Änderung hat ein Ziel.** Sachfremde Änderungen gehören in einen eigenen
   Branch.
5. **Commits sind in sich schlüssig.** Jeder Commit beschreibt einen nachvollziehbaren
   Schritt; seine Nachricht sagt, was sich ändert und warum.
6. **Die gemeinsame Historie wird nicht umgeschrieben.** Was andere bereits bezogen
   haben, wird nicht per Force-Push überschrieben.
7. **Der Branch wird aktuell gehalten.** Konflikte werden früh und auf dem eigenen
   Branch gelöst, nicht beim Merge.
8. **Erledigte Branches werden gelöscht.** Die Historie bleibt im Standard-Branch.
9. **Stände, die ausgeliefert werden, sind benannt** – durch eine Marke oder einen
   Release-Branch nach dem Modell des Projekts –, damit sie reproduzierbar sind.

## Projektspezifische Ergänzungen

`<TBD: Festlegungen des Projekts, sofern nicht in OVERLAY.md Abschnitt 10, zum Beispiel
Umgang mit Hotfixes oder Release-Branches>`
