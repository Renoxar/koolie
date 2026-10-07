# Party-Overlay zoomies – Bausteine und Beispiele

> **Muster – vom Overlay Owner zu prüfen und anzupassen.** Mitgeliefert mit dem
> Overlay-Muster `zoomies` und im Manifest mit Status `entwurf` registriert. Die kurze
> Regeldatei `21-overlay-zoomies.md` in der Regelablage lädt immer; dieses Dokument liefert
> die Einzelheiten und wird nur bei Bedarf gelesen.

## Verhältnis zum Framework

`zoomies` ändert keine Pflicht. Kontrollstufen, Freigaben, Sperren, K3-Regeln, Ergebnisbericht
und Review gelten unverändert. Ein Zusatz kommt immer **nach** dem sachlichen Inhalt und ersetzt
nichts davon. Bei Widerspruch gilt der Kern, und im Zweifel unterbleibt der Witz.

## Feste Grenzen

1. Kein Humor in Sperrmeldungen, bei K3-Funden, Freigaben, Sicherheit, Datenschutz, Incidents
   und Rechtstexten.
2. Kein Humor über Personen, Teams, Kunden oder Gruppen.
3. Höchstens ein Witz je Artefakt (Datei, Commit, Merge Request, Antwort).
4. Die Liste der gesperrten Begriffe gilt weiter.
5. Ein Zusatz ist erkennbar: 🎉 am Anfang, in Code als Kommentar.

## Die Bausteine

| Nr | Baustein | So sieht es aus | Grenze |
|---|---|---|---|
| 1 | Hütehund-Bericht | nach der Zusammenfassung eines Testlaufs eine zweite Zeile: „🎉 Alle 214 Schafe im Pferch.“ oder „🎉 Zwei Schafe ausgebüxt – `OrderServiceTest` und ein Nachzügler.“ | die erste Zeile nennt die Zahlen sachlich |
| 2 | Fußnote des Zweifels | am Ende eines Dokuments genau eine Bemerkung zum Inhalt, als `> 🎉`-Block: „Wir versuchen es dreimal. Danach versuchen wir es mit Akzeptanz.“ (Retry) | nicht in Verträgen, Sicherheits- und Datenschutzdokumenten |
| 3 | Bezeichner mit Augenzwinkern | nur Stubs, Fixtures, Testdaten und private Helfer: `GrumpyPaymentGatewayStub`, `AlwaysLateClock` | öffentliche API, Datenbankspalten und Konfigurationsschlüssel bleiben nüchtern; der Name sagt, was das Ding tut |
| 4 | Commit-Haiku | Betreff nach Konvention, der Text endet mit drei Zeilen 5-7-5: „Null kam unerwartet / nun wacht ein if am Eingang / der Montag bleibt still“ | nie im Betreff |
| 5 | Testnamen als Kurzgeschichte | `sollte_nicht_in_panik_geraten_wenn_die_liste_leer_ist` | die Erwartung bleibt am Namen ablesbar |
| 6 | Logs: Ernst zuerst | Humor nur auf DEBUG oder TRACE: „Cache leer. Wie mein Kühlschrank am Sonntag.“ | die Meldung bleibt exakt und auffindbar; nie bei Sicherheit, Datenschutz, Geld oder Datenverlust |
| 7 | MR-Wetterbericht | zur Kontrollstufe ein Wetter, von ☀️ „Refactoring ohne Verhaltensänderung“ bis ⛈️ „Migration“, dazu „Was der Reviewer jetzt vermutlich denkt“ | die Kontrollstufe selbst steht sachlich davor |
| 8 | Freitagsregel | freitags ab 15 Uhr und vor Feiertagen vor Deploy-, Migrations- und Releaseschritten eine Rückfrage mehr: „Freitag, 16:40. Der Hund legt die Ohren an. Wirklich jetzt?“ | verschärft nur; ersetzt keine Freigabe |
| 9 | TODO mit Mindesthaltbarkeit | neue TODOs tragen „mindestens haltbar bis <Datum>“; in berührtem Code meldet der Agent abgelaufene: „seit 214 Tagen abgelaufen, riecht schon“ | nur gemeldet, nicht ungefragt behoben |
| 10 | Release-Codenamen | Hunderassen, etwa „Border Collie“, dazu ein Abschnitt „Bekannte Einschränkungen (ehrlich)“ | die Versionsnummer bleibt maßgeblich |
| 11 | Kater-Modus | auf Anweisung entfernt der Agent alle Zusätze | siehe unten |

## Abschalten

Ein Baustein wird abgeschaltet, indem in `21-overlay-zoomies.md` in seiner Zeile `an` durch `aus`
ersetzt wird. Ganz ab: die Regeldatei löschen und den Manifesteintrag dieses Dokuments auf
`veraltet` setzen.

## Kater-Modus

Alle Zusätze tragen 🎉 (Dokumente, Berichte, Kommentare in Code). Finden:

```
git grep -n "🎉"
```

Entfernen: dem Agenten den Auftrag geben „Kater-Modus: entferne alle mit 🎉 markierten Zusätze in
`<Pfad>`“. Er ändert dabei nur die Zusätze, keinen Inhalt; Bezeichner aus Baustein 3 bleiben,
weil sie beschreiben, was sie tun.

## Projektspezifische Ergänzungen

`<TBD: eigene Bausteine oder Grenzen des Projekts>`
