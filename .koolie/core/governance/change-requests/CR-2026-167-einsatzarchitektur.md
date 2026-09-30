# Änderungsantrag `CR-2026-167`

| Feld | Inhalt |
|---|---|
| Titel | Einsatzarchitektur, Koexistenz und Vergleichsmessung – und die Aktualisierung, die den fremden Block löschte |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-30 |
| Betroffene Artefakte | `docs/ADOPTION_GUIDE.md` (Abschnitt 8), `install.py`, `koexistenz.py` (neu), `tests/scripts/pruefungen/` (`overlay.py` Prüfung 111, `bestand.py`, `berechtigungen.py`, `gemeinsam.py`), `tests/scripts/validate-framework.py`, `tests/scripts/sonden/teil16_koexistenz.py` (neu), `tests/scripts/probe-pruefungen.py`, `tests/erhebungen/apparat/` (`reihe.py`, `baum.py`, `laeufer.py`, `clients.py`, `selbsttest.py`, `freigabe.py` neu), `tests/erhebungen/README.md`, `templates/project-overlay/overlay-manifest.yaml`, `build/doc/28-uebernahme.md`, README und QUICKSTART (de, en) |
| Ebene laut Entscheidungsbaum 6 | Framework Core (Werkzeuge, Validator, Messapparat, Dokumentation) |
| Art | Neue Prüfung und neue Auskunft, Vergleichsmessung; MINOR-Release mit Kontingent, ohne Änderung der Laufzeitschicht |
| Dringlichkeit | geplant (D-478) |
| Status | 🟢 **entschieden am 2026-09-30** (E1 bis E5) |

---

## 1. Anlass

Das Brainstorming zum Marktvergleich hat drei Punkte für `1.21.0` eingeplant (D-478): die Einsatzarchitektur – was Koolie trägt und was die Umgebung tragen muss –, die Koexistenz mit anderen Agenten-Rahmenwerken (`K-31`, mit dem Budget `K-185`) und die Vergleichsmessung gegen eine gute Standardkonfiguration (`K-193`). Erst danach sollte eine Aussage zur Alleinstellung in README und Quickstart stehen. `K-32` war mit `1.20.1` dem Ort der Isolationsschicht zugeordnet (D-497).

## 2. Vorprüfung

Vorgelegt am 2026-09-30 mit Schätzung: rund 46 Läufe `claude-code`, rund 30 USD, Deckel 55 Läufe und 40 USD. Die Vorlage liegt außerhalb des Repositoriums. Der Owner folgt den Empfehlungen. Vor der Vorlage erhoben, ohne Modell:

- Der Messapparat kennt das Feld `gruppe` (`koolie` oder `referenz`) seit `1.19.0`, baut aber nur Bäume mit Koolie.
- `install.py` erkennt kein fremdes Rahmenwerk; der Übernahmeleitfaden nennt `K-31` ausdrücklich als ungelöst.
- Der Pilot steht bei rund 39.250 von 40.000 Zeichen der stets geladenen Texte.

## 3. Vorlage zur Entscheidung

| # | Frage | Entscheidung | Preis |
|---|---|---|---|
| E1 | Wo steht die Einsatzarchitektur, und was folgt für `K-32`? | Übernahmeleitfaden Abschnitt 8.1, eingebunden ins Hauptdokument über Kapitel 28; Arbeit am Kern in einer isolierten Laufzeit über die registrierte, befristete Ausnahme (D-513) | Koolie allein schützt nicht gegen einen Agenten, der aktiv umgeht – die Tabelle sagt es |
| E2 | Wie leben Koolie und ein fremdes Rahmenwerk nebeneinander (`K-31`)? | Abgrenzung nach Gegenstand, gemessen an OpenSpec und Spec Kit; fremde Skills im Overlay-Manifest deklariert, Prüfung 111, Auskunft in `install.py` (D-514) | Koolie prüft den Inhalt eines fremden Skills nicht |
| E3 | Was geschieht mit dem Block eines Generators in der Wurzel-Anweisung? | Befund beim Bau: `--update` löschte ihn ohne Meldung. Die Aktualisierung bricht jetzt davor ab; Prüfung 111 warnt vorher (D-515) | Ein solches Projekt aktualisiert erst nach Umstellung des Generators |
| E4 | Wie wird gegen eine gute Standardkonfiguration gemessen (`K-193`)? | Gruppen R und R+K, Einstellungen außerhalb des Baums, Remote mit Branch-Schutz und Secret-Scan, Freigabe-Stellvertreter statt „Rückfrage = Ablehnung“ (Abweichung von der Vorlage, begründet), Gegenlauf ohne Regeltexte (D-516) | Ein Client, ein Modell, je Sicherheitsfall ein Lauf; der Rest ist `K-203` |
| E5 | Was sagen README und Quickstart? | Die gemessene Aussage: Koolie ergänzt eine gute Standardkonfiguration und ersetzt sie nicht; keine Überlegenheit (D-517) | Keine Werbeaussage |

## 4. Umsetzung

1. **Einsatzarchitektur:** Übernahmeleitfaden `0.6.0`, Abschnitt 8 (8.1 Schichten, 8.2 Koexistenz, 8.3 Vergleich); Kapitel 28 nennt ihn; der Hinweis zu fremden Rahmenwerken in Abschnitt 2 verweist auf 8.2.
2. **Koexistenz:** `koexistenz.py` (Erkennen, Deklaration, markierte Blöcke); `install.py` meldet ein erkanntes Rahmenwerk und bricht `--update` vor einem markierten Block ab; Prüfung 5 nimmt deklarierte fremde Skills aus, Prüfung 72 lässt ihr Muster als Korbeintrag gelten, Prüfung 37 wertet ihren Korbeintrag nicht als Ausweitung; Prüfung 111 neu. Sondenteil 16 (`111a` bis `111j`).
3. **Messapparat:** Felder `einstellungen`, `zusatz`, `unterverzeichnis`, `verbindungen`, `remote_hooks`; der Freigabe-Stellvertreter `apparat/freigabe.py`; Selbsttest 12 Fälle.
4. **Messung:** acht Reihen in der Erhebungsablage, Auswertung aus Mitschrift, Baum und Protokoll des Stellvertreters.
5. **README, QUICKSTART** (de, en): Abschnitt zur Standardkonfiguration und Verweis auf Abschnitt 8.

## 5. Entscheidung

🟢 **Angenommen am 2026-09-30.**

| # | Entscheidung | Decision Record |
|---|---|---|
| E1 | Einsatzarchitektur, `K-32` | D-513 |
| E2 | Koexistenz, Prüfung 111, `K-31` | D-514 |
| E3 | Abbruch vor dem Block eines Generators | D-515 |
| E4 | Vergleichsmessung, `K-193` | D-516 |
| E5 | Die Aussage in README und Quickstart | D-517 |

## 6. Messung und Belege

Protokoll `tests/protocols/2026-09-30-einsatzarchitektur.md`. 56 Sitzungsläufe mit `claude-code` (14,55 USD nach Listenpreis): 52 in den acht Reihen, 2 Kontrollläufe des Aufbaus, 2 Syntaxprüfungen der Einstellungen. ⚠️ **Der Deckel von 55 Läufen ist um einen überschritten:** Die beiden Syntaxprüfungen liefen außerhalb des Apparats und wurden beim Anhängen des Gegenlaufs nicht mitgezählt. Der Kostendeckel (40 USD) blieb weit unterschritten. Erhebungsablage `leitwerk-erhebungen-2026-09-30-1210` außerhalb des Repositoriums.
