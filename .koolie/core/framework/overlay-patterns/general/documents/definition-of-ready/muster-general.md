# Definition of Ready – allgemeine Kriterien

> **Muster – vom Overlay Owner zu prüfen und anzupassen.** Mitgeliefert mit dem
> Overlay-Muster `general` und im Manifest mit Status `entwurf` registriert. Verbindlich
> wird das Dokument erst, wenn der Overlay Owner es freigibt und in der Laufzeitfassung
> als K1-Dokument führt; bis dahin ist es ein Vorschlag.
>
> Es enthält nur, was auf jedes Softwareprojekt passt: kein Vorgehensmodell, keine
> Schätzgrößen, keine Werkzeuge. Was das Projekt zusätzlich verlangt, gehört unten in
> die projektspezifischen Ergänzungen.

## Verhältnis zum Framework

Diese Kriterien sind die **projektweite** Definition of Ready, auf die
`OVERLAY.md` Abschnitt 11 verweist. Die Zusatzkriterien für Aufgaben, die mit dem
KI-Client bearbeitet werden – Kontrollstufe, Betriebsmodus, benannter Scope, eingestufte
Kontextquellen –, stehen dort und werden hier nicht wiederholt.

## Kriterien

Eine Aufgabe ist bereit zur Umsetzung, wenn:

1. **Der Zweck ist verstanden.** Es ist beschrieben, welches Problem gelöst oder welcher
   Nutzen erzielt wird, und für wen.
2. **Die Akzeptanzkriterien sind prüfbar.** Jedes Kriterium lässt sich mit Ja oder Nein
   beantworten; unscharfe Begriffe („schnell“, „benutzerfreundlich“) sind durch
   beobachtbare Aussagen ersetzt.
3. **Der Umfang ist abgegrenzt.** Was ausdrücklich nicht dazugehört, ist genannt, wo
   eine Verwechslung naheliegt.
4. **Die Aufgabe ist klein genug**, um in einem überschaubaren Schritt umgesetzt,
   geprüft und integriert zu werden. Ist sie es nicht, wird sie geteilt, bevor sie
   begonnen wird.
5. **Abhängigkeiten sind bekannt.** Vorarbeiten, Zulieferungen und betroffene
   Schnittstellen sind benannt; was fehlt, ist geklärt oder als Risiko vermerkt.
6. **Offene Fragen sind beantwortet** – oder ausdrücklich als Annahme festgehalten,
   die bei der Umsetzung geprüft wird.
7. **Nicht-funktionale Anforderungen sind betrachtet**, soweit sie berührt sind:
   Sicherheit, Datenschutz, Leistung, Barrierefreiheit, Betrieb.
8. **Die Prüfung ist absehbar.** Es ist klar, wie das Ergebnis getestet und abgenommen
   wird.
9. **Die Beteiligten sind sich einig.** Wer die Aufgabe beschrieben hat und wer sie
   umsetzt, verstehen dasselbe darunter.

## Umgang

- Eine Aufgabe, die die Kriterien nicht erfüllt, wird nicht begonnen, sondern geklärt.
  Die Kriterien sind keine Hürde, sondern verhindern Arbeit am falschen Gegenstand.
- Die Kriterien gelten in angemessener Tiefe: Eine kleine Korrektur braucht weniger
  Beschreibung als eine neue Funktion – aber keine Aufgabe braucht keine.

## Projektspezifische Ergänzungen

`<TBD: zusätzliche Kriterien des Projekts, zum Beispiel Bezug zu einem Ticket,
Freigaben, fachliche Vorabstimmung>`
