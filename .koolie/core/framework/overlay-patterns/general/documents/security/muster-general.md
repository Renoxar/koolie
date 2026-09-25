# Sicherheit – allgemeine Grundsätze der Entwicklung

> **Muster – vom Overlay Owner zu prüfen und anzupassen.** Mitgeliefert mit dem
> Overlay-Muster `general` und im Manifest mit Status `entwurf` registriert. Verbindlich
> wird das Dokument erst, wenn der Overlay Owner es freigibt und in der Laufzeitfassung
> als K1-Dokument führt; bis dahin ist es ein Vorschlag.
>
> Es enthält nur, was auf jedes Softwareprojekt passt: keine Werkzeuge, keine
> Verfahren oder Bibliotheken, keine Schutzkonfiguration. Schutzkonfigurationen und
> konkrete Sicherheitsvorgaben des Projekts sind K3 oder gehören in eigene, bereinigte
> Dokumente.

## Verhältnis zum Framework

Die Prüfpunkte für einzelne Änderungen – Eingabevalidierung, Autorisierung in jedem
Pfad, keine Injection-Vektoren, keine hartcodierten Geheimnisse, Logging ohne
Geheimnisse, Kryptografie nur über freigegebene Verfahren – stehen in
`.koolie/core/checklists/06-security.md`; die Regeln für neue Abhängigkeiten in
`.koolie/core/checklists/07-new-dependency.md`. Sie werden hier nicht wiederholt.
Dieses Dokument beschreibt die Grundsätze, aus denen sie folgen.

## Grundsätze

1. **Sicherheit ist eine Anforderung**, keine Nacharbeit. Sie wird bei der Beschreibung
   einer Aufgabe betrachtet (Definition of Ready) und nicht erst im Review entdeckt.
2. **Jeder Eingabe wird misstraut**, die über eine Vertrauensgrenze kommt – von
   Nutzerinnen und Nutzern, anderen Systemen, Dateien oder Konfiguration.
3. **Minimale Rechte.** Jede Komponente, jedes Konto und jeder Prozess erhält nur die
   Rechte, die für seine Aufgabe nötig sind, und nur so lange wie nötig.
4. **Gestaffelte Abwehr.** Keine einzelne Schutzmaßnahme wird als ausreichend
   betrachtet; fällt eine aus, greift die nächste.
5. **Sicher scheitern.** Tritt ein Fehler in einer Sicherheitsprüfung auf, wird der
   Zugriff verweigert, nicht gewährt.
6. **Sichere Voreinstellungen.** Neue Funktionen und Schalter beginnen im
   restriktiven Zustand; Lockerungen sind eine bewusste Entscheidung.
7. **Kleine Angriffsfläche.** Was nicht gebraucht wird – Endpunkte, Funktionen,
   Abhängigkeiten, Berechtigungen –, wird entfernt oder gar nicht erst eingeführt.
8. **Bewährtes statt Eigenbau** für Authentifizierung, Sitzungen und Kryptografie.
9. **Geheimnisse gehören nicht in den Code** und nicht in die Versionsverwaltung. Ein
   versehentlich veröffentlichtes Geheimnis gilt als kompromittiert und wird ersetzt,
   nicht nur gelöscht.
10. **Abhängigkeiten werden gepflegt.** Bekannte Schwachstellen werden zeitnah bewertet
    und behoben; nicht mehr gepflegte Abhängigkeiten werden ersetzt.
11. **Sicherheitsentscheidungen werden festgehalten** – mit Begründung, damit sie später
    geprüft und nicht versehentlich rückgängig gemacht werden.
12. **Schwachstellen werden gemeldet**, nicht still behoben. Der Meldeweg des Projekts
    gilt auch für Funde im eigenen Code.

## Projektspezifische Ergänzungen

`<TBD: Festlegungen des Projekts, zum Beispiel Schutzbedarf, Meldeweg über die
Sicherheitsrolle aus OVERLAY.md Abschnitt 15, verbindliche Richtlinien der Organisation>`
