# Änderungsantrag `CR-2026-086`

| Feld | Inhalt |
|---|---|
| Titel | Die Grenzfälle gegen die Fassungen gehalten – vier Befunde, drei davon in Trägern, die in jede Sitzung laden |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-18 |
| Betroffene Artefakte | `framework/runtime/rules/20-project-overlay.md`, `framework/runtime/rules/10-privacy-security.md`, `checklists/06-security.md`, `tests/EDGE_CASES.md`, `tests/TEST_CATALOG.md` (`FW-KO-01`, `FW-KO-05`), `docs/ROADMAP.md` (Releaseplan, Rückschau 0.32.0), `tests/scripts/validate-framework.py` (**Prüfung 51, 52 und 53**, Kopfkommentar), `tests/scripts/probe-pruefungen.py` (sieben Sonden, zehn Gegenproben), `governance/DECISION_LOG.md` (D-148 bis D-153, `K-59` bis `K-61`), `tests/protocols/2026-09-18-FW-KO-05.md`, `CHANGELOG.md`, `VERSION` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind normative Laufzeitregeln, eine Checkliste, der Testkatalog und der Prüfapparat |
| Art | Befundbehebung, drei neue Prüfungen, berichtigtes Prüfmittel, Releaseplan |
| Dringlichkeit | **Regulär, mit einem Vorbehalt.** Kein Sicherheitsvorfall – aber einer der vier Befunde stellt ein **Delegationsverbot** (V6) in zwei Fassungen auf die freigebbare Seite, und beide Fassungen sind solche, die ein Client lädt oder ein Mensch abhakt |

## 1. Anlass

Der Releaseplan sah für `0.61.0` den fünften Sitzungstest vor. **Vor dem ersten Lauf ist
wieder die Vorbedingung durchgegangen worden** – die Auflage, die sich seit `UEB-06`
(0.58.0) viermal in Folge getragen hat. Dabei fiel zweierlei auf:

1. **Zwei der neun Zellen des Sitzungstests sind gar keine Sitzungszellen.** `FW-KO-05` und
   `FW-AK-01` tragen Prüfmittel `review`. Sie brauchen kein Sitzungskontingent, und
   `FW-KO-05` ist seit seiner Entstehung (0.32.0) nie gefahren worden.
2. **Der Releaseplan selbst hatte zwei Fehler** – siehe Abschnitt 5.

**Also wurde `FW-KO-05` gefahren.** Die Durchsicht kostete kein Kontingent und hat **vier
Befunde** ergeben, davon **drei in Trägern, die `always_on` in jede Sitzung laden**. Das
vollständige Protokoll: `tests/protocols/2026-09-18-FW-KO-05.md`.

| Befund | Grenzfall | Fundstellen | Alter | Behoben |
|---|---|---|---|---|
| **B1** | G-13 | `rules/20-project-overlay.md` | **33 Releases** | ja, + Prüfung 51 |
| **B2** | G-05, G-06 | `rules/10-privacy-security.md`, `checklists/06-security.md` | **60 Releases** | ja, + Prüfung 52 |
| **B3** | G-02 | `rules/10-privacy-security.md` | **60 Releases** | ja |
| **B4** | G-11 | `root-instruction.md`, `rules/20-project-overlay.md`, `checklists/01-preflight.md` | **34 Releases** | **nein** (`K-59`) |

## 2. B1: Die Overlay-Laufzeitfassung bot an, was ihre eigene Quelle ausschließt

`framework/runtime/rules/20-project-overlay.md` führte bis 0.60.0:

> `- Freigegebene externe Domains: <TBD: Liste oder „keine">`

**Die Quelle derselben Regel legt den Wert seit 0.33.0 fest.**
`templates/project-overlay/OVERLAY.md` Abschnitt 13 trägt in der Freigabespalte **„keine"**
mit der Begründung: *„Eine Freigabe je Domain ist nicht vorgesehen (D-59): `deny` gewinnt,
und bei einem Client ohne Musterunterstützung für die Abrufwerkzeuge ist sie nicht
ausdrückbar."*

🔴 **Der eigentliche Befund ist, warum die Stelle nicht zu finden war.** `0.33.0` (B11,
D-59) hat die Domain-Ausnahme in **sechzehn Trägern** angefasst, davon **acht anweisenden**
– darunter `framework/runtime/rules/10-privacy-security.md`, eine Datei im **selben
Verzeichnis**. `rules/20-project-overlay.md` war nicht darunter, **weil dort kein Satz stand,
sondern ein Ausfüllschlitz.**

➡️ **Eine Regel kann als Satz oder als Ausfüllschlitz ausgedrückt sein, und ein Sweep nach
der Formulierung findet nur den Satz.** Bekannt ist die Bauform als *„eine Suche nach einer
Marke findet nicht, was dieselbe Bedeutung ohne sie ausdrückt"* – neu ist, dass die zweite
Ausdrucksform ein **Schlitz** ist.

**Und die Release-Nachricht von 0.33.0 hat es gesagt:** *„Ein Overlay, das freigegebene
externe Domains führt, verliert seine Grundlage – sie hat nie gewirkt."* Dreiunddreißig
Releases lang hat die Datei, die in jede Sitzung lädt, dazu eingeladen.

## 3. B2 und B3: Zweimal derselbe Mechanismus in derselben Datei

**B2 ist der schwerere.** `rules/10-privacy-security.md` und `checklists/06-security.md`
führten *Security-Konfiguration* in derselben Aufzählung wie Authentifizierung und
Kryptografie – und die Rechtsfolge dieser Aufzählung lautete *„Umsetzung ausschließlich nach
dokumentierter Freigabe"*.

**G-05 und G-06 sagen das Gegenteil:** Eine Berechtigungsmatrix eines laufenden Systems,
eine Firewall-Regel und Sicherheitskonfiguration als Code sind **V6 – nicht delegierbar,
auch nach Freigabe nicht.** Die Wurzel-Anweisungsdatei trennt seit D-53 zwei Sätze, die
Langform zieht die *Abgrenzung zu V6*. **Die Regelablage und die Checkliste hat die
Trennung nie erreicht.**

**B3 ist derselbe Mechanismus, dieselbe Datei.** Ihr Regelsatz zu den Kontextklassen lautete
*„Mischinhalte tragen die höchste enthaltene Klasse."* – der Langform fehlt dort das
*„bis die höher eingestuften Bestandteile entfernt oder ersetzt sind"*. Damit ist **G-02**
(die bereinigte Ableitung ist ein eigener Inhalt, D-52) aus dieser Fassung nicht mehr
ableitbar; ein Leser kommt zur gegenteiligen Einstufung.

➡️ **Eine Kurzfassung, die den einschränkenden Halbsatz der Langform weglässt, kehrt ihre
Aussage um** (D-152). Zweimal in einer Datei. **Prüfung 29 hätte beides nicht gefunden:**
Sie prüft die K3-Kategorien auf **Vollständigkeit** und auf **Bedingungswörter** – ein
fehlender Vorbehalt ist das Gegenteil davon.

## 4. B4: Der zweite Einsatzkontext – nicht behoben, und das ist Absicht

G-11 hält *„eine Analyse im Quellrepositorium ohne aktives Overlay, als Protokoll abgelegt"*
für **zulässig** – M1 für die Analyse, **M5 für das Protokoll** (D-56). Drei Fassungen sagen
etwas anderes: Die Wurzel-Anweisungsdatei (*„arbeitest du nur lesend"*), die
Overlay-Laufzeitfassung und die Preflight-Checkliste (*„MUSS Overlay-Status ist `aktiv`
(Ausnahme: Onboarding-Übung auf dem Übungsrepository)"*).

**Den zweiten Einsatzkontext kennen von den sechs Fassungen allein die fünf Analyseskills** –
seit 0.32.0, also vierunddreißig Releases.

🔴 **Die Lage ist nicht theoretisch:** Jede Sitzung an diesem Framework steht in diesem
Kontext und legt ihr Ergebnis unter `tests/protocols/` ab. Die Texte, die sie lädt, sagen,
sie dürfe nur lesen. **Siehe E5.**

## 5. Der Releaseplan hatte zwei Fehler, und sie stammen aus `0.60.0`

`CR-2026-085` E5 hat entschieden, `FW-RE-01` als Sammelzelle in den Posten der Testblätter
zu verschieben; Kriterium 2 geht damit von 93 auf **84** statt auf 83. **Die Zahl wurde
nachgezogen, die Aufzählung nicht:**

- Die Zeile `0.61.0` führte weiter **`RE` (1)** in ihrem Gegenstand – **die Zeile
  widersprach ihrer eigenen Zahl**, und die Folgezeile nennt `FW-RE-01` ausdrücklich unter
  den Sammelzellen.
- Die Folgezeile begann bei **83** statt bei 84. **Die Kette riss um eins.**

**Nachgezählt am zentralen Katalog:** `FI` 3, `KO` 2, `PO` 2, `AK` 2, `NE` 1, `SC` 1, `RE` 1
= 12 offene Zellen. Sitzungstest 5 nimmt neun davon (ohne die drei Sammelzellen), also
93 → 84; es bleiben `FW-NE-04`, `FW-PO-03`, `FW-RE-01`.

➡️ **Eine Zahl, die nicht zur Erwartung passt, ist der billigste Prüfstein dieses
Projekts** – hier hat sie zweimal gegriffen, und beide Male in einem Release, das gerade
erst gemergt war.

## 6. Vorlage zur Entscheidung

| Nr. | Frage | Vorschlag | Preis |
|---|---|---|---|
| **E1** | **Ist `FW-KO-05` ein Sitzungstest oder ein Dokumentenreview?** | **Ein Dokumentenreview.** Vier von fünf Zellen seiner Zeile beschreiben einen Textvergleich, die Prüfmittelzelle sagt `review`, und die Legende des Katalogs definiert `review` wörtlich als *„strukturiertes Dokumentenreview durch eine zweite Rolle"* – genau das, was der Steckbrief von `EDGE_CASES.md` seit jeher sagt. Die vier Träger, die eine Sitzung behaupten, werden berichtigt | **Der Antrag, der die Zeile geschaffen hat, sagt zweimal das Gegenteil** (`CR-2026-052` Abschnitt 3 und E6). Er stellte *Sitzung* gegen *Skript* – **die dritte Prüfmethode war nicht im Blick.** Das ist eine Vorlage, deren Antwortmenge kleiner war als ihr Gegenstand, und es gehört hingeschrieben, nicht überspielt |
| **E2** | **Und die Frage, ob ein KI-Client die Grenzfälle wirklich so einstuft?** | **Bleibt ungemessen und wird als `K-60` geführt.** Keine neue Zelle | **Kriterium 2 bekäme sonst eine Zelle dazu**, und der Gegenstand ist über die Klassen `KO` und `SC` in Einzelfällen bereits gemessen. **Der Preis der Vertagung:** Die Grenzfalltabelle bleibt eine Aussage über Texte, nicht über Verhalten – und sie sagt das jetzt selbst |
| **E3** | **Gehört die Regelablage in den Gegenstand von `FW-KO-05`?** | **Ja, als sechste Fassung.** Sie ist die einzige Schicht, die `always_on` lädt; `FW-KO-02` nennt sie seit jeher | **Der Gegenstand wächst um vier Träger.** Er war es ohnehin: **Vier der sieben Fundstellen dieser Durchsicht liegen dort**, und ohne die Nennung hätte die Durchsicht sie übergehen dürfen |
| **E4** | **Wie wird „lässt den Fall offen" gelesen?** | **Schweigen ist kein Befund.** Der unzulässige Ausgang gilt einer Fassung, die das **Sachgebiet** des Falles führt und die Entscheidung trotzdem nicht trägt | **Die Abgrenzung ist Ermessen**, und deshalb steht die Zuordnung je Fall als **Aufzählung** im Protokoll. **Ohne sie wäre die Zelle nie abnehmbar:** Keine Overlay-Vorlage stuft je die Werkzeugvererbung an einen Unteragenten ein (G-18, G-19) |
| **E5** | **Wird B4 (G-11) in diesem Release behoben?** | **Nein.** `K-59`, mit beiden Wegen und beiden Preisen | **Eine Abweichung bleibt stehen, und `FW-KO-05` bleibt damit `offen`** – Kriterium 2 bewegt sich nicht. **Der Gegenpreis der Gegenseite ist schwerer:** Den Text nachzuziehen hieße, eine Ausnahme in **jede Installation** auszuliefern – die Bauform, die `FRAMEWORK_DEV_PROFILE.md` Abschnitt 5 selbst ablehnt –, und sie hinge an einer Bedingung, die der Client nach Abschnitt 2.2 nicht selbst feststellen darf. **Das ist ein eigener Antrag wert, kein Nebenprodukt** |
| **E6** | **Bekommen die Befunde Prüfungen?** | **Zwei. Prüfung 51** für B1: Trägt die Overlay-Vorlage für ein Feld einen festen Wert, führt die Laufzeitfassung dafür keinen Schlitz – Feldmenge **abgeleitet**. **Prüfung 52** für B2: Kein Gegenstand der V6-Zeile in einer Einheit, die zugleich `Kontrollstufe hoch` und eine Umsetzungsfreigabe trägt – Begriffe **abgeleitet**, ausgenommen ist die Langform, die sie trägt | **B3 bekommt keine.** Ein fehlender Halbsatz ist maschinell nicht zu finden, ohne Bedeutung zu lesen; was mechanisch geht, deckt Prüfung 52 ab. **Das ist eine ausdrückliche Lücke** – sie bleibt `review`-prüfbar und hängt an `FW-KO-02` und `FW-KO-05`. **Und Prüfung 52 liest Wörter, keine Bedeutung:** Ein Text, der dieselbe Aussage ohne diese Begriffe trifft, entgeht ihr – dieselbe Grenze wie bei Prüfung 29 |
| **E7** | **Wie wird der Fehler im Releaseplan behoben?** | **Die `0.61.0`-Zeile wird zu diesem Release, Sitzungstest 5 wandert auf `0.62.0` ohne `RE`, die Testblätter auf `0.63.0 bis ~0.67.0` mit `84 → 0`.** Die Rückschau auf 0.32.0 bekommt einen **Nachtrag**, keine Berichtigung | **Die exakten Nummern verschieben sich zum zweiten Mal**, die Tilde-Posten um zwei. Das ist dieselbe Entscheidung wie bei `CR-2026-085` E6: exakte Nummern wandern, geschätzte nicht. **Die Anmerkung unter der Tabelle sagt es** |
| **E9** | **Bekommt die Kriterium-2-Kette des Releaseplans eine Prüfung?** | **Ja, Prüfung 53.** Was ein Posten erreicht, ist der Ausgangswert des nächsten, und der letzte Wert ist null | 🔴 **Das Protokoll zu 0.56.0 hat ausdrücklich das Gegenteil entschieden:** *„Die Zwischenstände im Plan sind Vorhersagen … sie tragen keinen Anspruch, den eine Prüfung einlösen müsste.“ **Die Begründung trug die Wahrheit der Vorhersage, nicht ihre innere Widerspruchsfreiheit** – und nur die zweite ist prüfbar. **Die zweite Hälfte des Befundes bleibt ungeprüft:** Die Zeile nannte weiter `RE`, das ihre eigene Zahl nicht mehr enthielt. Das ist Prosa und bleibt Gegenstand des Durchgangs vor dem Commit |
| **E8** | **Was folgt aus `FW-KO-02`?** | **`K-61`.** Sein `bestanden` vom 2026-09-10 nennt die Regelablage im Auslöser; drei der vier Befunde liegen dort und sind **nach** seiner Abnahme entstanden | **Nicht entschieden.** Drei Wege stehen im Registereintrag, keiner ist offensichtlich richtig – und der billigste (Datumsvergleich gegen den letzten Commit) meldete bei jeder Formulierungsänderung |

## 7. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle neun Fragen wie vorgelegt.** |
| Datum | 2026-09-18 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | **D-148** (`FW-KO-05` ist ein Dokumentenreview; `K-60` für den anderen Gegenstand), **D-149** (die Regelablage gehört zum Gegenstand; Schweigen ist kein Befund), **D-150** (Prüfung 51), **D-151** (Prüfung 52), **D-152** (der weggelassene einschränkende Halbsatz kehrt die Aussage um), **D-153** (Prüfung 53) |
| Neue Klärungspunkte | `K-59` (zweiter Einsatzkontext in drei Fassungen nicht abgebildet), `K-60` (stuft ein Client die Grenzfälle wirklich so ein?), `K-61` (ein `bestanden` eines Konsistenztests altert) |
| Auflagen | **Wer eine Regel sweept, sucht sie in beiden Ausdrucksformen – als Satz und als Ausfüllschlitz.** Und: **Wer eine Kurzfassung schreibt oder prüft, hält jeden Satz gegen seinen Ursprung in der Langform – nicht auf Vollständigkeit der Aufzählung, sondern auf den Vorbehalt** |
| Ziel-Release | `0.61.0` |
| Umsetzung | umgesetzt mit `0.61.0` |

## 8. Abnahme

- Validator `0 Fehler, 0 Warnungen`, **beide Kodierungsumgebungen**.
- Sondenlauf: **sieben neue Sonden** (`51a`, `51b`, `52a`, `52b`, `53a` bis `53c`) und
  **zehn neue Gegenproben** (`51a` bis `51c`, `52a` bis `52d`, `53a` bis `53c`); Spanne
  `6, 14 und 18 bis 53` in allen drei Trägern **ausgerechnet**, nicht gepflegt.
- **Gegenbeweis gegen den unberührten Vorstand:** Beide Sonden stellen den Stand vor 0.61.0
  **wörtlich** wieder her – die Domainzeile und den Satz über sicherheitsrelevante
  Änderungen. Sie messen damit den Befund, den dieses Release behoben hat, nicht einen
  nachgebauten. **Sonde `53a` stellt den Fehler her, den `0.60.0` gemergt hat** – die
  Folgezeile beginnt bei 83 statt 84 – und die Meldung nennt beide Posten beim Namen.
- **Der Zuschnitt beider Prüfungen ist durch Gegenproben belegt und nicht nur behauptet:**
  `51b` lässt die **Quelle** den Wert offen und der Schlitz wird zulässig – das belegt, dass
  die Prüfung die Vorlage liest und kein verdrahtetes Feld. `52d` legt der Langform einen
  Absatz bei, der beide Seiten nennt, und sie bleibt ausgenommen – die Ausnahme ist
  abgeleitet, nicht gepflegt.
- Protokoll der Durchsicht: `tests/protocols/2026-09-18-FW-KO-05.md`, mit der
  Zuordnung je Grenzfall.
