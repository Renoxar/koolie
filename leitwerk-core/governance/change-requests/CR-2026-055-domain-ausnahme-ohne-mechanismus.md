# Änderungsantrag `CR-2026-055`

| Feld | Inhalt |
|---|---|
| Titel | Die Domain-Ausnahme stand an fünf Stellen im Kern, hatte keinen Mechanismus und keine Matrixzeile |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-13 |
| Betroffene Artefakte | `framework/core/03-security.md` (Abschnitt 4), `framework/core/02-privacy.md` (Regel 3.7), `framework/runtime/rules/10-privacy-security.md`, `checklists/02-privacy-context.md`, `templates/project-overlay/OVERLAY.md` (Abschnitt 11), beide `CLIENT_PACK.md` (neue Zeile **B10**, Zusammenfassung), `tests/scripts/validate-framework.py` (Fetch-Allow aus dem Manifest, Prüfung 31), `tests/scripts/probe-pruefungen.py` |
| Ebene laut Entscheidungsbaum 6 | **Core** (Sicherheitsregel, Ebene 3) und Client Packs |
| Art | Befund **B11** des unabhängigen Reviews vom 2026-09-12, P2; **gegengeprüft, bestätigt und um zwei eigene Befunde erweitert** |
| Dringlichkeit | **Paket 5**, gemeinsam mit `CR-2026-054` |

## 1. Anlass und Problem

### 1.1 Die Widerlegung steht fünf Zeilen unter der Zusage

`framework/core/03-security.md` Abschnitt 4, in einer Tabelle und ihrem Nachsatz:

| Zeile | Text |
|---|---|
| 54 | `\| Netzwerkzugriff \| Fetch(*) \| deny; **Ausnahmen je Domain im Overlay** \|` |
| 57 | „Regeln aus höheren Ebenen haben Vorrang, **`deny` gewinnt immer** `[DOK]`.“ |
| 59 | „Der Grund ist mechanisch: In der Berechtigungsdatei gewinnt `deny` immer, und keine der abgebildeten Clientformen kennt ein Ausnahmemuster innerhalb eines deny.“ |

**Zeile 59 buchstabiert das Argument aus, das Zeile 54 widerlegt** – für das Kernverzeichnis, zu
einem anderen Zweck. Eine zusätzliche `allow`-Regel für eine Domain hebt ein bestehendes
`Fetch(*)`-Verbot nicht auf. Der Befund ist damit nicht bloß bestätigt, sondern **im eigenen
Dokument vorweggenommen**.

### 1.2 Eigene Feststellung: Die Zusage steht an fünf Stellen und hat keine Zeile

| Stelle | Wortlaut |
|---|---|
| `framework/core/03-security.md:54` | „deny; Ausnahmen je Domain im Overlay“ |
| `framework/core/02-privacy.md` Regel 3.7 | „Freigaben erfolgen domainbezogen über das Overlay und die Berechtigungskonfiguration (`Fetch(domain:...)` **`[DOK]`**)“ |
| `framework/runtime/rules/10-privacy-security.md:31` | „ohne domainbezogene Freigabe im Overlay“ |
| `checklists/02-privacy-context.md:39` | MUSS-Punkt, dieselbe Formulierung |
| `templates/project-overlay/OVERLAY.md` Abschnitt 11 | „`Fetch(domain:...)`-Regeln in `<PERMISSIONS_FILE>`“ |

**Keine Fähigkeitsmatrix führt eine Zeile dazu.** B8 deckt das *Verbot* ab und steht für die
Abrufwerkzeuge auf `[TECHNISCH]`; die zugesagte *Ausnahme* kommt in keinem Pack vor. Das ist
dieselbe Bauform wie der Suchkanal aus 0.30.0: **eine Zusage, die keine Schicht kennt.** Und die
Angabe `[DOK]` in `02-privacy.md` belegte eine Schreibweise, nicht ihre Wirkung gegen ein
bestehendes `deny`.

### 1.3 Eigene Feststellung: Bei einem Pack ist die Zusage nicht ausdrückbar

`clients/claude-code/manifest.json` führt `WebFetch` und `WebSearch` in
`permission_tools_bare`. Damit wird das Muster beim Rendern **verworfen**; die erzeugte Datei
trägt – am 2026-09-13 nachgeprüft an einer frischen Installation:

```
"deny": [ …, "WebFetch", "WebSearch" ]
```

Das ganze Werkzeug, nicht ein Ziel. Eine Domain-Angabe ist dort **überhaupt nicht ausdrückbar**.
Dazu führt `permission_tools.fetch` beide Werkzeuge zusammen – **für eine Websuche gibt es kein
Domain-Ziel**, eine Domain-Liste wäre dort auch künftig sinnlos.

Das Verwerfen ist im Manifest deklariert und für sich richtig. **Unbenannt blieb die Folge** – dass
damit eine Kernaussage bei diesem Pack nicht einlösbar ist. Wörtlich dasselbe Muster wie B01 bei
`permissions` in `drop_fields` (D-50), nur über einen anderen Mechanismus.

### 1.4 Eigene Feststellung: Der Validator entschied dieselbe Absicht je Pack verschieden

`check_config` führte eine feste Namensliste: `"Fetch(*"`, `"WebFetch"`, `"WebSearch"`. Nachgerechnet:

| Regel in `allow` | Ergebnis bis 0.32.0 |
|---|---|
| `Fetch(*)` | abgelehnt |
| `Fetch(domain:docs.example.invalid)` | **zulässig** |
| `WebFetch(domain:docs.example.invalid)` | abgelehnt |

**Dieselbe Absicht, zwei Packs, zwei Entscheidungen** – und niemand hat das entschieden. Es ist
derselbe Fehlertyp wie B02 und B10: eine Prüfung, die Clientnamen festschreibt, statt sie aus dem
Manifest zu nehmen.

### 1.5 Beim Einfügen der Matrixzeile aufgefallen: die Zusammenfassung überzeichnet

Die Zeile **B10** musste in die Fachmatrix – und damit in die Summen von Abschnitt 3. Dabei zeigte
sich: **Die Zusammenfassung war zwei Releases hinterher und zählte nach einer Regel, die D-47
widerspricht.**

| Angabe bis 0.32.0 (`claude-code`) | Nachgerechnet |
|---|---|
| `[TECHNISCH]` 25 von 29 | **20** von 30 |
| `[TEXTUELL]` 3 von 29 | **7** von 30 |
| `[NICHT ABBILDBAR]` 1 von 29 (S5) | **3** von 30 (S3, S5, B10) |

S3 steht seit 0.31.0 auf `[NICHT ABBILDBAR]` (`CR-2026-050`), ohne dass die Summen nachgezogen
wurden. Und die vier Zeilen mit einer Kanalgrenze – B3, B4, B5, B8 – zählten als `[TECHNISCH]`,
obwohl D-47 sie je Kanal ausweist und ihr Shell-Teil nur als Anweisung trägt. **Die Überschrift
desselben Abschnitts sagte „Alle sechs Kernzusagen sind technisch abgebildet"** – seit 0.30.0 zu
weit gefasst: Drei davon (B3, B4, B5) sind es nur für den direkten Zugriff.

**Es ist der dritte Drift dieser Summen.** Das Pack `devin-desktop` dokumentiert selbst einen
früheren: „Die Zeilenzahl ist mit 0.26.0 nachgezählt worden – sie stimmte vorher nicht.“ Eine Zahl,
die dreimal von Hand stimmen musste, gehört ausgerechnet.

## 2. Vorgeschlagene Änderung

1. **Die Zusage wird zurückgezogen.** Alle fünf Stellen sagen: Das generelle Verbot steht, eine
   Ausnahme je Domain gibt es **nicht**. `03-security.md` bekommt einen normativen Absatz, der die
   Mechanik nennt und den einzigen Weg beschreibt: **Ersatz statt Zusatz** – die Verbotsregel selbst
   wird über einen Änderungsantrag (V10) durch eine nachgewiesen gleichwertige Beschränkung
   ersetzt. Ein Overlay darf das nicht.
2. **Zeile B10 in beiden Packs**, nach D-41 mit benanntem Ersatz: bei `claude-code`
   `[NICHT ABBILDBAR]`, Ersatz ist das vollständige Verbot – **strenger** als die Zusage, deshalb
   kein Schutzverlust; bei `devin-desktop` `[TEXTUELL]` mit VERIFY-Marker, weil die Form das
   Rendern überlebt und ihre Wirkung unerhoben ist.
3. **Das Fetch-Allow-Verbot des Validators kommt aus dem Manifest** (`permission_tools.fetch`)
   statt aus einer Namensliste. Damit ist jede `allow`-Regel auf ein Abrufverb unzulässig, bei
   jedem Pack gleich.
4. **Die Summen der Fachmatrix werden ausgerechnet** – **Prüfung 31**, mit einer benannten
   Zählregel: eine Zeile zählt bei ihrer **schwächsten** Einstufung. Beide Zusammenfassungen und
   die Überschrift von `claude-code` werden berichtigt.

## 3. Was dieser Antrag nicht ändert

- **Er baut kein Domain-Profil.** Das Zwei-Profil-Modell des Reviews ist die größere Arbeit und
  gehört dorthin, wo die Netz- und Isolationsarbeit liegt (Paket 6) – samt URL-Normalisierung,
  Hostvergleich ohne Teilzeichenfolgen, Weiterleitungsprüfung und einem Nachweis, der ohne echte
  Netzwerkisolation nichts belegt.
- **Er trennt das Abrufverb nicht von der Websuche.** Solange keine Domain-Steuerung zugesagt
  wird, richtet die Zusammenlegung keinen Schaden an: Beide Werkzeuge sind verweigert, und das ist
  die Absicht. Die Matrixzeile hält fest, dass eine Websuche **keinen** Domain-Begriff kennt.
- **Er prüft keine Einstufung.** Prüfung 31 prüft die Arithmetik. Eine Matrix, in der jede Zeile
  falsch eingestuft ist, besteht sie.
- **Er beseitigt die Shell-Lücke im Netzverbot nicht.** B8 weist sie je Kanal aus; jedes andere
  netzfähige Programm als `curl`, `wget`, `ssh`, `scp` ist nicht erfasst (D-47).

## 4. Prüffragen

- [x] Richtige Ebene: Sicherheitsregel im Core, Abbildung im Pack.
- [x] Verschärfungsprinzip: **verschärft dreifach.** Eine Ausnahme, die nie wirkte, verschwindet;
      das Fetch-Allow-Verbot wird symmetrisch und damit strenger für ein Pack; die Summen hören auf,
      die Durchsetzungstiefe zu überzeichnen. **Gelockert wird nichts** – es gab nichts zu lockern.
- [x] Widerspruchsfreiheit: gelesen wurden D-30, D-41 (Ausfall mit benanntem Ersatz), D-47 (Zusagen
      je Zugriffskanal), D-50 (ein verworfenes Feld nennt seine Folge), D-59-Kandidat,
      `governance/PRIORITY_HIERARCHY.md` Regel 2.1, `framework/runtime/permissions.json`.
- [x] Laufzeitfassungen: Die erzeugten Regeln ändern sich **nicht** – `deny` auf die
      Abrufwerkzeuge stand und steht. Geändert wird, was darüber behauptet wird.
- [x] Belegstatus: **im Code und an einer frischen Installation nachgeprüft** – die erzeugte
      Regelmenge beider Packs, die Namensliste des Validators durchgerechnet, die Summen der
      Matrizen ausgezählt.
- [x] Test- und Validierungsbedarf: **eine Sonde und eine Gegenprobe je Pack** für das
      Fetch-Allow-Verbot; **vier Sonden und eine Gegenprobe** für Prüfung 31.
- [x] Overlays: Ein Overlay, das freigegebene Domains führt, verliert seine Grundlage. Sie hat nie
      gewirkt – der Migrationshinweis sagt das.
- [ ] Dokumentation: `CHANGELOG.md`, Decision Log (D-59, D-60), Roadmap, beide Packs.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Wird eine Domain-Ausnahme zugesagt? | **Nein – die Zusage wird zurückgezogen.** Sie hat nie gewirkt, bei einem Pack ist sie nicht ausdrückbar, und keine Matrixzeile hat sie je getragen. Der einzige dokumentierte Weg ist der **Ersatz** der Verbotsregel per Änderungsantrag, nicht ihre Ergänzung | Ein Projekt, das öffentliche Dokumentation braucht, bekommt in 0.33.0 keinen Weg; freigegebene Auszüge werden lokal bereitgestellt. **Das ist der ehrliche Stand, nicht eine neue Einschränkung** – funktioniert hat es nie |
| E2 | Was tritt an die Stelle der Zusage? | **Das vollständige Verbot**, und es ist **strenger** als die zurückgezogene Zusage. Deshalb ist der Ausfall kein Schutzverlust und die Inbetriebnahme nicht betroffen (D-41). Die Matrixzeile B10 sagt es je Pack | Der Ersatzsatz muss sagen, dass er strenger ist – ein Ersatzsatz, der seine Richtung verschweigt, wäre derselbe Befundtyp eine Ebene höher (Auflage aus `CR-2026-050`) |
| E3 | Wann kommt das Domain-Profil? | **Mit Paket 6**, wo die Isolationsschicht und die Pfaddurchsetzung liegen. Vorher ist es nicht messbar, und ein Profil, das man nicht messen kann, ist genau die Zusage, die dieses Projekt sich abgewöhnt | Eine bewusste Schuld. Der Eintrag steht in der Roadmap, mit den drei Vorarbeiten: Trennung von Abruf und Websuche, Hostvergleich, Weiterleitungen |
| E4 | Wird das Abrufverb jetzt von der Websuche getrennt? | **Nein.** Ohne zugesagte Domain-Steuerung ändert die Trennung an den erzeugten Regeln **nichts** – beide Werkzeuge bleiben verweigert. Ein neues Verb erzwänge Anpassungen in beiden Packs, im Validator und in jedem künftigen Pack, für einen Nutzen, der erst mit Paket 6 entsteht | Die Zusammenlegung bleibt stehen, und wer das Profil später baut, muss sie zuerst auflösen. Die Matrixzeile benennt es |
| E5 | Bleibt das Fetch-Allow-Verbot eine Namensliste? | **Nein, es kommt aus dem Manifest.** Die Asymmetrie – `Fetch(domain:…)` zulässig, `WebFetch(domain:…)` abgelehnt – war keine Entscheidung, sondern eine Nebenwirkung fest verdrahteter Namen. Derselbe Fehlertyp wie B02 und B10 | Ein Pack, das `permission_tools.fetch` leer lässt, entgeht der Prüfung. Das ist bei `hook_tools_absent` entschieden (D-47, Prüfung 26): Eine erklärte Abwesenheit muss folgerichtig sein – die Prüfung dort gilt weiter |
| E6 | Werden die Summen der Fachmatrix ausgerechnet? | **Ja, Prüfung 31, mit benannter Zählregel: schwächste Einstufung.** Das ist die einzige Regel, die D-47 nicht widerspricht – eine Zeile, deren Zusage in einem Kanal nur als Anweisung trägt, ist nicht technisch durchgesetzt. Die Summen sind **dreimal** gedriftet | Die ausgewiesene Durchsetzungstiefe **sinkt** – bei `claude-code` von 25 auf 20 technische Zeilen, und die Überschrift verliert den Satz, alle sechs Kernzusagen seien technisch abgebildet. **Das ist keine Verschlechterung, sondern das Ende einer Überzeichnung**; die Zeilen selbst sagten es seit 0.30.0 |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle sechs Fragen wie vorgelegt.** E1 die Zusage wird zurückgezogen; E2 Ersatz ist das vollständige Verbot, ausdrücklich als das strengere benannt; E3 das Domain-Profil kommt mit Paket 6; E4 keine Verbtrennung jetzt; E5 das Fetch-Allow-Verbot kommt aus dem Manifest; E6 Prüfung 31 rechnet die Summen nach, Zählregel schwächste Einstufung |
| Datum | 2026-09-13 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | D-59 (keine Ausnahme je Domain; Ersatz statt Zusatz), D-60 (die Summen der Fachmatrix werden ausgerechnet) |
| Auflagen | **Der Rückzug gehört in den Migrationshinweis**, und zwar mit dem Satz, dass die Freigabe nie gewirkt hat – sonst liest es sich wie eine neue Einschränkung. **Die Summen sind mitzuberichtigen, obwohl der Befund sie nicht nennt:** Sie sind beim Einfügen der Zeile B10 aufgefallen, sie waren zwei Releases hinterher, und die Überschrift behauptete eine Durchsetzungstiefe, die D-47 seit 0.30.0 widerlegt. **Nachgewiesen:** eine Sonde und eine Gegenprobe je Pack für das Fetch-Allow-Verbot, vier Sonden und eine Gegenprobe für Prüfung 31; gegen 0.32.0 meldet Prüfung 31 fünf Fundstellen in den unveränderten Packs, und Prüfung 30 eine sechste, weil die Grenzfalltabelle des Vorstands D-59 nicht kennt. **Offen bleibt:** das Domain-Profil (Paket 6), die Trennung von Abrufverb und Websuche, und die Shell-Lücke des Netzverbots (D-47) |
| Ziel-Release | `0.33.0` |
| Umsetzung | umgesetzt mit `0.33.0` |
