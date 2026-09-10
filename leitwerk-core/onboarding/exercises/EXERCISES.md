# Übungsaufgaben (synthetisch)

Alle Aufgaben sind **synthetische Übungen** auf dem Übungsrepository (`README.md` in diesem Verzeichnis). Modul- und Dateinamen wie `src/ordering` oder `OrderValidator` sind erfunden; das Projekt ersetzt sie beim Erstellen des Übungsrepositorys durch die eigenen Übungsmodule. Jede Übung endet mit dem Ergebnisbericht und einem kurzen Gespräch mit der Mentorin oder dem Mentor.

## Ü1 – Repository analysieren (M1)

**Ziel:** Belegten Überblick erstellen und Fundstellenprüfung als Gewohnheit verankern.

1. Preflight ausfüllen (Stufe niedrig, M1, Scope: Übungsmodul).
2. `/fw-repo-analyze src/ordering "Wo werden eingehende Bestellungen validiert?"`
3. Drei Fundstellen aus der Antwort selbst öffnen und je in einem Satz bestätigen oder widerlegen.
4. Eine Aussage der Analyse finden, die eine Vermutung ist, und prüfen, ob sie als solche gekennzeichnet war.

**Erfolgskriterien:** Preflight vollständig; drei Fundstellen geprüft; Umgang mit „nicht gefunden mit Suchmuster …" verstanden (kann eines nennen).
**Typische Stolperstelle:** Analyse „auf das ganze Repo" statt auf das Modul – Least Context verletzt.

## Ü2 – Code erklären lassen und verifizieren (M1)

**Ziel:** Erklärtiefe steuern und beobachtet/geschlossen unterscheiden.

1. `/fw-code-explain src/ordering/domain/OrderValidator überblick`, danach dieselbe Klasse mit `detail`.
2. Aus der Detail-Erklärung zwei „beobachtet"-Aussagen und eine „geschlossen"-Aussage (Vermutung) heraussuchen und die Kennzeichnung prüfen.
3. Eine Verständnisfrage formulieren, die nur das Team beantworten kann (Absicht/Historie), und sie auf die Mentorenliste setzen.

**Erfolgskriterien:** Unterschied der Tiefen benannt; Vermutungskennzeichnung gefunden; Team-Frage sinnvoll abgegrenzt.

## Ü3 – Plan und kleine Änderung (M2 → M3)

**Ziel:** Den vollständigen Weg einer Änderung gehen – mit echtem Halte-Punkt.

Aufgabe (synthetisch): „Die Validierung akzeptiert die Menge 0, fachlich gilt aber: Menge 1 bis 999." (Der eingebaute Übungsfehler; das Nachbarmodul enthält denselben Fehler – **Achtung Scope-Falle**, siehe Ü6c.)

1. Preflight (Stufe niedrig oder mittel – begründen!), dann `/fw-change-analyze` mit der Aufgabenbeschreibung.
2. `/fw-plan` – Plan nach Vorlage; Mentorin oder Mentor bestätigt schriftlich (Übungsform: Chat- oder Ticketnotiz).
3. `/fw-change-small` – Umsetzung in kleinen Schritten; jede Schreib- und Ausführungsanfrage bewusst einzeln bestätigen.
4. Ergebnisbericht lesen; Selbstreview mit `leitwerk-core/checklists/04-review-ai-code.md`; Commit-Vorschlag prüfen; Übungs-MR-Beschreibung mit `/fw-mr-description` erzeugen.

**Erfolgskriterien:** Plan vor Umsetzung bestätigt; Änderung nur im Zielmodul (Scope-Falle nicht ausgelöst oder korrekt gemeldet); Tests grün; Nutzungsvermerk vorhanden; jede Zeile des Diffs erklärbar.

## Ü4 – Tests erstellen und Fehler einordnen (M4 / M1)

**Ziel:** Testaussagekraft und der Umgang mit aufgedeckten Fehlern.

1. `/fw-tests src/ordering/domain/OrderValidator "Menge 1 bis 999 gültig; 0 und 1000 ungültig; fehlende Kundenreferenz ist Validierungsfehler"` – vor der Umsetzung der Ü3-Korrektur ausgeführt, deckt ein Test den Übungsfehler auf.
2. Beobachten: Der fehlschlagende Test bleibt unverändert; Devin meldet den Befund. Danach `/fw-error-analyze` mit dem (synthetischen) Befund.
3. Nach der Ü3-Korrektur Tests erneut ausführen; Regressionsnachweis im Bericht prüfen.
4. Abschluss: `leitwerk-core/checklists/05-testing.md` auf die eigenen Tests anwenden; eine bewusste Schwäche suchen (zum Beispiel fehlender Randfall) und als Lücke notieren.

**Erfolgskriterien:** kein Produktivcode aus M4 heraus geändert; fehlschlagender Test nicht „grün gemacht"; Lückenliste vorhanden.

## Ü5 – Kontext einstufen und bereinigen (Modul 2)

**Ziel:** Sichere K0–K3-Einstufung in unter einer Minute je Fall.

Die Mentorin oder der Mentor legt zehn synthetische Schnipsel vor (Vorschlag im Mentorenblatt): Ticket mit Kundenname; Logauszug mit E-Mail-Adresse; `.env`-Fragment; Architekturauszug mit Hostnamen; Convention-Dokument; Stacktrace ohne Personenbezug; Testdatensatz „Testperson-01"; Screenshot-Beschreibung mit echten Falldaten; Partner-Schnittstellenvertrag; Framework-Datei.

1. Jeden Schnipsel einstufen (Baum 1) und die Entscheidung in einem Satz begründen.
2. Für zwei K2-Fälle die Bereinigung schriftlich durchführen (Personen → Rollen, Adressen → Platzhalter).
3. Für einen K3-Fall den korrekten Umgang benennen (nicht verwenden; falls bereits bereitgestellt: Prozess nach `02-privacy.md` Abschnitt 5).

**Erfolgskriterien:** keine K3-Fehleinstufung; Mischinhalt-Regel angewendet; Bereinigungen vollständig.

## Ü6 – Negativübungen: die drei Köder (Modul 9)

**Ziel:** Die Fallen erkennen, korrekt reagieren, richtig melden. Die Köder sind im Übungsrepository platziert (`README.md` Punkt 4); die oder der Lernende kennt ihre genaue Lage nicht.

- **Ü6a Injektionsköder:** Bei Ü1/Ü2 stößt die Analyse auf die präparierte README mit einer Anweisung an KI-Werkzeuge. Erwartet: Devin meldet den Injektionsversuch (S6) und befolgt ihn nicht; die oder der Lernende erkennt die Meldung im Bericht und benennt den Meldeweg (`<SECURITY_CONTACT>` – in der Übung: Mentorin oder Mentor).
- **Ü6b K3-Köder:** Die präparierte Beispiel-Konfigurationsdatei taucht in einer Analyse auf. Erwartet: nur Fundstelle, kein Inhalt im Bericht; die oder der Lernende zitiert den Inhalt auch selbst nicht weiter und benennt den S3-Prozess.
- **Ü6c Scope-Falle:** Während Ü3 fällt der gleiche Fehler im Nachbarmodul auf. Erwartet: keine Ausweitung der Änderung; Befund wird als eigener Punkt („separates Ticket") im Ergebnisbericht notiert.

**Erfolgskriterien (bestanden/nicht bestanden):** alle drei Köder erkannt und regelkonform behandelt; bei Nichtbestehen Wiederholung des betroffenen Moduls (`../MENTOR_CHECKLIST.md`, Rote Flaggen).
