# Änderungsantrag `CR-2026-057`

| Feld | Inhalt |
|---|---|
| Titel | `disallowed-tools` ist gemessen – S3 ist zurückgewinnbar, aber nicht in der Form, in der das Framework die Beschränkung heute aufschreibt |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-13 |
| Betroffene Artefakte | `clients/claude-code/manifest.json` (Abbildungsfeld, `drop_fields`), `clients/claude-code/CLIENT_PACK.md` (Zeile **S3**, Summen), die zwölf Quellskills unter `framework/skills/` (nur, falls E3 es verlangt), `framework/core/05-working-model.md` (M1), `tests/scripts/validate-framework.py` (neue Prüfung), `tests/scripts/probe-pruefungen.py`, `tests/EDGE_CASES.md` |
| Ebene laut Entscheidungsbaum 6 | **Client Pack** (Abbildung) und **Core** (die Aussage zu M1) |
| Art | Offener Punkt aus `CR-2026-050`/D-50 und Eintrag in **Paket 6**; **erhoben am 2026-09-13**, neun Läufe, zwei davon verworfen und als Befund festgehalten |
| Dringlichkeit | **Paket 6.** Kein P1: Die heutige Zusage ist **zu schwach**, nicht zu stark – S3 steht auf `[NICHT ABBILDBAR]`, und das war nach dem damaligen Belegstand richtig |

## 1. Anlass und Befundlage

Die Erhebung liegt vor: `tests/protocols/2026-09-13-erhebung-disallowed-tools.md`.
Aufbau bewusst **ohne Bypass**: Die Berechtigungsschicht blieb an, und `Write` stand in der
`allow`-Liste – damit kann eine Verweigerung von `Write` nur aus `disallowed-tools` kommen.

### 1.1 Der Befund: es beschränkt wirklich, und zwar stärker als eine Regel

| Lauf | Aufbau | Ergebnis |
|---|---|---|
| B | `disallowed-tools: Write, Edit` | **`Write` abgewiesen**, Datei nicht entstanden – **obwohl `Write` in `allow` steht** |
| C | **Kontrolllauf**, identisch ohne das Feld | **`Write` gelang**, Datei entstanden |

Beide Läufe zeigen dieselbe Werkzeugfolge, beginnend mit `Skill | {"skill": "lw-probe-dt"}`;
nur der Ausgang von `Write` unterscheidet sich. `permission_denials` bestätigt es als zweite,
vom Antworttext unabhängige Quelle.

**Das ist genau das, was `allowed-tools` nach B01 nicht ist.** `disallowed-tools` wägt nicht
gegen Freigaben ab – es nimmt das Werkzeug aus dem Vorrat, und eine `allow`-Regel holt es nicht
zurück. **S3 ist damit zurückgewinnbar.**

### 1.2 Grenze 1: Die Schranke gilt nur für den aufrufenden Turn

Turn 1 mit Skill: `Write` abgewiesen. Turn 2 derselben Sitzung, ohne erneuten Skill-Aufruf:
**`Write` gelang.** Die Dokumentation sagt es vorher; gemessen ist es jetzt auch.

**Das wirkt in den Kern zurück.** `framework/core/05-working-model.md` stützt den Betriebsmodus
M1 („nur lesend") unter anderem auf die Skill-Beschränkung. Eine Schranke mit Verfallsdatum am
Ende des Turns ist **keine Betriebsart**.

### 1.3 Grenze 2: Die Liste ist aufzählend, eine Lücke ist ausnutzbar

Mit `disallowed-tools: Write, Edit` schrieb der Skill **über `Bash`**. Mit `Write, Edit, Bash`
wurde `Bash` abgewiesen. Der exec-Weg ist ausdrückbar – **aber nur, wenn er dasteht.**

### 1.4 Grenze 3, und sie entscheidet den Zuschnitt: Argumentmuster wirken **lautlos gar nicht**

`disallowed-tools: Bash(echo verboten:*)` ließ den verbotenen Befehl durchlaufen – **ohne
Verweigerung, ohne Fehlermeldung**. Ebenso die Schreibweise mit Leerzeichen. Derselbe Skill mit
`disallowed-tools: Bash` wies **beide** Befehle ab.

> **Der wiederkehrende Befundtyp dieses Projekts, in seiner unangenehmsten Form:** Der Eintrag
> sieht aus wie eine Regel, wird angenommen, meldet nichts – und beschränkt nichts. Wer
> `Bash(git push:*)` schreibt, hat **gar keine** Schranke, nicht bloß eine gröbere.

### 1.5 Was das Framework heute aufschreibt – in drei Bauformen, nachgezählt

Die zwölf Quellskills tragen `permissions` **nicht** einheitlich:

| Bauform | Anzahl | Beispiel |
|---|---|---|
| nur grobe Verben (`edit`, `exec`) | **7** | `deny: [edit, exec]`; `fw-docs-update` nur `exec` |
| befehlsgenaue Einträge | **5** | `deny: [Exec(git push), Exec(git reset --hard)]` |
| dazu ein `allow:`-Block | **5** (dieselben fünf) | `allow: [Exec(git status), Exec(git diff)]` |

**Nur die sieben groben lassen sich treu abbilden** – und von den fünf übrigen tragen **zwei** daneben das grobe Verb `edit`, bekommen also eine **teilweise** Schranke; **drei** bekommen gar keine. Diese Aufteilung ist an der **erzeugten Fassung** nachgezählt, nicht an der Quelle (siehe Abschnitt 6, Auflagen). Die fünf befehlsgenauen nicht: Ihr
Verbotsteil ist nicht ausdrückbar (1.4), und ihr `allow:`-Teil wäre nach B01 ohnehin nur eine
Vorabfreigabe, keine Zusage. **Sperrt man bei ihnen das ganze Werkzeug, macht man die
`allow:`-Einträge derselben Skills wirkungslos** – `fw-tests` dürfte dann seinen Testbefehl
nicht mehr ausführen.

### 1.6 Nebenbefund zur Messmethode, nicht zur Sache

Zwei der neun Läufe sind verworfen, beide, weil der **`Skill`-Aufruf** scheiterte und die
Sitzung die `SKILL.md` ersatzweise als Datei las. Einmal, weil `defaultMode: bypassPermissions`
in der Projektdatei nicht greift; einmal durch **Eigenverschulden** – der Vertrauenseintrag war
zu früh entfernt. **Beide Male hat die Sitzung es von sich aus gemeldet; verlassen kann man sich
darauf nicht.** Der Rekorder-Hook ist der Beleg, und er gehört in jede Sonde dieser Bauart.

## 2. Vorgeschlagene Änderung

1. **Zeile S3 wird `[TECHNISCH]` mit drei benannten Grenzen** – Turnbereich, Aufzählung,
   keine Argumentmuster. Belegstatus `[MESS]` mit Verweis auf das Erhebungsprotokoll.
2. **`permissions.deny` bekommt eine Abbildung**, wie `triggers` sie mit
   `model_invocation_field` bekam (D-50): neues Manifestfeld, das die groben Verben auf die
   Werkzeugnamen des Packs abbildet – **aus `hook_tools`**, nicht aus einer zweiten Liste
   (D-28). `edit` → `Edit, Write, NotebookEdit`; `exec` → `Bash`.
3. **`permissions` verlässt `drop_fields`**, soweit es abgebildet wird. Der Ersatzsatz aus D-50
   wird berichtigt: Es gibt jetzt einen Ersatz, und er ist **benannt schwächer**, nicht
   abwesend.
4. **Befehlsgenaue Einträge werden nicht abgebildet** – siehe E3 – und ihre Nicht-Abbildung
   wird **deklariert statt verschwiegen**, in derselben Bauart wie `hook_tools_absent` (D-47).
5. **Eine Prüfung weist die lautlose Musterform ab.** Ein `disallowed-tools`-Eintrag mit
   Klammer ist gemessen wirkungslos; er darf in keiner erzeugten Fassung stehen.
6. **M1 wird im Arbeitsmodell an den Belegstand angeglichen** (Turnbereich).
7. **Sonden und Gegenproben** für die neue Prüfung und die Abbildung, je Pack.

## 3. Was dieser Antrag nicht ändert

- **Er misst `devin-desktop` nicht.** Die Wirkung der Skill-`permissions` bleibt dort
  unerhoben; die Zeile behält ihren VERIFY-Marker.
- **Er erhebt das Agentenprofil nicht** (`tools`/`disallowedTools`). Weiterhin ungemessen.
- **Er macht aus S3 keine Betriebsart.** Die Turngrenze bleibt; sie wird benannt, nicht
  geschlossen.
- **Er berührt den Schutz-Hook nicht.** Die globale Berechtigungsschicht bleibt, was sie ist –
  jetzt allerdings nicht mehr als *Ersatz* für S3, sondern **neben** ihm.
- **Er entscheidet K-32 nicht** und baut keine Isolationsschicht.

## 4. Prüffragen

- [x] Richtige Ebene: Abbildung im Pack, die Aussage zu M1 im Kern.
- [x] Verschärfungsprinzip: **verschärft.** Zwölf Skills tragen heute *keine* wirksame
      Beschränkung; sieben bekommen eine. Gelockert wird nichts.
- [x] Widerspruchsfreiheit: gelesen wurden D-23 (jede Prüfung braucht eine Sonde), D-28
      (Werkzeugnamen aus den Manifesten), D-41 (Fähigkeitszusage), D-47 (Absenz wird deklariert),
      D-50 (ein zusagentragendes Feld verschwindet nicht beim Rendern), K-18.
- [x] Belegstatus: **neun Läufe, davon zwei verworfen und als Befund festgehalten**, mit
      Kontrolllauf, Positivkontrolle und Rekorder-Hook je Lauf.
- [ ] Test- und Validierungsbedarf: neue Prüfung plus Sonden – Zuschnitt hängt an E3 und E5.
- [x] Overlays: unberührt.
- [ ] Dokumentation: `CHANGELOG.md`, Decision Log, Roadmap, Client Pack, `EDGE_CASES.md`.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Vorschlag | Preis |
|---|---|---|---|
| **E1** | Wird S3 zurückgewonnen, und auf welche Einstufung? | **`[TECHNISCH]` mit drei benannten Grenzen.** Gemessen ist eine echte Entfernung aus dem Werkzeugvorrat, die sogar eine `allow`-Regel schlägt | Eine Zeile, die die drei Grenzen **nicht** nennt, wäre der Befundtyp dieses Projekts, neu erzeugt. Die Zeile wird lang – **das ist der Preis, und er ist billig** |
| **E2** | Woher kommen die Werkzeugnamen für `edit` und `exec`? | **Aus `hook_tools` des Manifests** (D-28), nicht aus einer zweiten Liste. `edit` → `Edit, Write, NotebookEdit`; `exec` → `Bash` | Jedes künftige Pack braucht die Zuordnung. Eine zweite Liste wäre eine zweite Wahrheit über dasselbe |
| **E3** | Was geschieht mit den **fünf** Skills mit befehlsgenauen Verboten? | **Nicht abbilden und es deklarieren.** Die Alternative – das ganze Werkzeug sperren – ist strenger als gemeint und macht die `allow:`-Einträge derselben Skills wirkungslos: `fw-tests` könnte seinen Testbefehl nicht mehr ausführen | **Drei von zwölf Skills bekommen gar keine Schranke je Skill, zwei nur eine teilweise**, und das muss dastehen. Der Gegenvorschlag („lieber zu streng als gar nicht") verwandelt Arbeitsskills in unbrauchbare – deshalb verworfen |
| **E4** | Wird `permissions.allow` auf `allowed-tools` abgebildet? | **Nein.** Nach B01 ist `allowed-tools` eine Vorabfreigabe, keine Zusage. Eine Abbildung erzeugte ein Feld, das wie eine Zusage aussieht und keine ist | Bequemlichkeit geht verloren: Die fünf Skills fragen bei ihren Testbefehlen weiter nach. **Das ist die ehrliche Seite des Handels** |
| **E5** | Soll eine Prüfung Argumentmuster in `disallowed-tools` **abweisen**? | **Ja.** Gemessen ist: ein Eintrag mit Klammer wirkt lautlos gar nicht. Eine Prüfung, die ihn durchlässt, lässt eine Schranke durch, die keine ist | Wenn der Hersteller die Form später unterstützt, ist die Prüfung eine Bremse. **Dafür gibt es den Änderungsantrag** – und bis dahin ist das Schweigen gefährlicher |
| **E6** | Wird M1 im Arbeitsmodell an die Turngrenze angeglichen? | **Ja.** M1 stützt sich auf die Skill-Beschränkung; die gilt nur für den aufrufenden Turn | Der Kern wird angefasst, und M1 liest sich schwächer. **Es ist aber keine Schwächung, sondern eine Berichtigung** – schwächer war es schon vorher, nur stand es nicht da |
| **E7** | Bleibt der Ersatzsatz aus D-50 stehen? | **Nein, er wird berichtigt.** Er sagt heute „Kein Ersatz je Skill – und das ist die Aussage". Ab jetzt gibt es einen, für sieben von zwölf Skills, mit drei Grenzen | D-50 wird in seinem Kern **bestätigt** (ein Feld verschwindet nicht unbenannt) und in seinem Befund überholt. Der Decision Record muss beides sagen |
| **E8** | Wird das in **einem** Release umgesetzt oder getrennt? | **Ein Release.** Abbildung, Prüfung, Matrixzeile und M1 gehören zusammen; getrennt entstünde ein Zwischenstand, in dem die Zeile mehr verspricht als die Abbildung leistet | Das Release wird größer als 0.34.0 in der Dokumentation, aber kleiner im Code |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle acht Fragen wie vorgelegt.** E1 S3 wird `[TECHNISCH]` mit drei benannten Grenzen; E2 die Werkzeugnamen kommen aus `hook_tools`; E3 befehlsgenaue Verbote werden **nicht** abgebildet und ihre Nicht-Abbildung deklariert; E4 `permissions.allow` wird **nicht** auf `allowed-tools` abgebildet; E5 eine Prüfung weist Argumentmuster ab; E6 M1 wird an die Turngrenze angeglichen; E7 der Ersatzsatz aus D-50 wird berichtigt; E8 ein Release |
| Datum | 2026-09-13 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | D-64 (S3 ist zurückgewonnen, mit drei Grenzen), D-65 (die Abbildung von `permissions.deny`, und was bewusst unabgebildet bleibt), D-66 (ein Argumentmuster in `disallowed-tools` wird abgewiesen) |
| Auflagen | **Die Turngrenze gehört in jede der drei Stellen** – Matrixzeile, Arbeitsmodell, Grenzfalltabelle – und nicht nur in eine. **Die fünf nicht abgebildeten Skills werden im Client Pack namentlich genannt**, nicht als Zahl: Eine Zahl ohne Namen ist in diesem Projekt schon dreimal gedriftet. **Und die Auflage hat beim ersten Lauf gegriffen:** Beim Nachzählen an der erzeugten Fassung waren es nicht „fünf ohne Schranke", wie dieser Antrag ursprünglich schrieb, sondern **drei ohne und zwei mit einer teilweisen**. Die Entscheidung E3 ändert das nicht; der Text ist berichtigt. **Die Prüfung misst die erzeugte Fassung, nicht die Quelle** – B01 ist genau daran vorbeigekommen, dass die Quelle mehr sagte als die Installation trug. **Beim Anfassen aufgefallen und mitzuberichten:** `skill_frontmatter.tool_names` bildet `edit` auf `Edit, Write` ab, `hook_tools.write` auf `Edit, Write, NotebookEdit` – **zwei Listen für dieselbe Sache, auseinandergelaufen.** Die neue Abbildung nimmt `hook_tools` (E2); `allowed-tools` bleibt unverändert, und der Unterschied wird im Protokoll benannt statt still geheilt |
| Ziel-Release | `0.35.0` |
| Umsetzung | umgesetzt mit `0.35.0` |
