# Änderungsantrag `CR-2026-020`

| Feld | Inhalt |
|---|---|
| Titel | Der werkzeugneutrale Kern nannte einen Client als Handelnden |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | 93 Dateien des Kerns; `tests/scripts/validate-framework.py` (Prüfung 14 neu) |
| Ebene laut Entscheidungsbaum 6 | Framework Core und Kerndokumentation; keine neue Regelebene |
| Art | Neutralisierung mit Durchsetzung; Folgearbeit zu D-15 und D-19 |
| Dringlichkeit | regulär |

## 1. Anlass und Problem

D-02 ordnet einen werkzeugneutralen Kern an. D-15 und D-19 haben ihn eingelöst, soweit es
**Pfade** betraf: 63 Client-Bindungen und 994 Pfadnennungen ersetzt, ein Glossar als Abbildung.
Die **Akteursbezeichnung** lag außerhalb dieses Umfangs und blieb stehen.

Der Kern schrieb deshalb nicht vor, was ein KI-Client tun MUSS, sondern was **Devin** tut – in
normativen Sätzen, in Rollenspalten, in der Delegationsverbotsliste, in den Abbruchbedingungen.
Ein zweites Client Pack existiert seit 0.6.0; für dessen Nutzer benannten diese Regeln ein
Produkt, das sie nicht einsetzen.

**Der Umfang war größer als angenommen.** Die Roadmap führte den Punkt seit 0.13.0 mit „76
Nennungen in elf Modulen" – gezählt allein in `framework/core/`. `docs/RUNTIME_GLOSSARY.md`
definiert den Kern jedoch ausdrücklich weiter: `framework/`, `governance/`, `checklists/`,
`prompts/`, `decision-trees/`, `onboarding/`, `docs/`, `templates/`, `examples/`, `tests/`.
Danach gezählt waren es **248 Akteursnennungen in 78 Dateien**, dazu die Quellen des
Hauptdokuments unter `build/doc/` und vier Skripte unter `tests/scripts/`.

Der größte Einzelposten war `templates/project-overlay/OVERLAY.md` mit 19 Nennungen – die
Vorlage, die **jedes aufnehmende Projekt** ausfüllt und in der der Produktname damit in jede
Übernahme weitergereicht wurde.

Derselbe Befundtyp wie `CR-2026-018` und `CR-2026-019`: eine Zusage, die nie vollständig gegen
ihren eigenen Gegenstand gehalten wurde. Die Zählung, die den Rest offen hielt, war selbst zu
klein – und niemand hat sie nachgerechnet.

## 2. Vorgeschlagene Änderung

**Der Kern nennt den Handelnden beim Begriff: „der KI-Client".** Der Begriff steht bereits in
`docs/RUNTIME_GLOSSARY.md` und war im Kern an sieben Stellen in Gebrauch; er wird jetzt
durchgängig verwendet. Komposita folgen dem im Kern schon vorhandenen Präfix `KI-`
(`KI-Aufgabe`, `KI-Vorschlag`, `KI-Ergebnis`, `KI-Sitzung`) – die Kurzform verwendete
`KI-Ergebnis` und `KI-Nutzung` bereits.

**Der Produktname bleibt, wo ein Produkt gemeint ist.** „Devin Desktop", „Devin Local",
„Devin-Desktop-Installation", die Pack-Kennungen, die Laufzeitpfade und die Quellen-Domains
sind unverändert: Sie benennen ein Produkt, nicht den Handelnden. Muss ein Kerntext den Namen
selbst tragen, steht dort `<CLIENT_NAME>`.

**Historische Dokumente bleiben unverändert** – `CHANGELOG.md` (auch die der Skills),
`governance/change-requests/`, `governance/DECISION_LOG.md`, `tests/protocols/`. Sie beschreiben
einen vergangenen Zustand; ihn nachträglich zu glätten, zerstört die Nachvollziehbarkeit
(`RUNTIME_GLOSSARY.md`, Abschnitt „Regel").

**Prüfung 14 setzt das durch.** Ohne sie wäre die Neutralität eine Zusage, die beim nächsten
von Hand geschriebenen Absatz verfällt – genau das Muster, das D-25 für Versionsfelder
beschreibt. Die Prüfung leitet die Clientnamen aus den **Pack-Kennungen** ab, nicht aus einer
gepflegten Liste: Ein künftiges Client Pack bringt seinen Namen damit selbst mit und wird ohne
Änderung an der Prüfung erfasst.

**62 Versionsfelder sind um eine PATCH-Stelle gehoben.** `08-skill-conventions.md` Abschnitt 7
führt „Korrekturen und Formulierungen" als PATCH und verlangt bei jeder Versionsänderung die
erneute Ausführung der Testfälle. Sechs Skills haben zusätzlich einen Eintrag in ihrem
Änderungsverlauf; der Validator hat ihn eingefordert.

## 3. Was dieser Antrag nicht ändert

- **Keine Regel, keine Zusage, kein Mechanismus.** Die Sätze sagen dasselbe über einen anders
  benannten Handelnden. Berechtigungsdatei, Hooks, Ladetrigger und Fähigkeitsmatrix sind
  unberührt.
- **Die Laufzeitschicht war schon frei davon** (seit 0.12.0, D-24). Was in eine Sitzung geladen
  wird, ändert sich nicht – deshalb ist dies eine Konsistenz-, keine Verhaltensänderung.
- **Die Pfadnennungen bleiben Sache von Prüfung 12.** `~/.devin/plans/` in
  `05-working-model.md` und die clientspezifischen Inhalte der Zeile „Umsetzung beim KI-Client"
  sind weiterhin client-gebunden; dieser Antrag benennt sie, löst sie nicht (siehe 5.).

## 4. Vorlage zur Entscheidung

Fünf Auflösungen mit Ermessensspielraum, jede einzeln. E1 und E2 sind bereits durch
`<FRAMEWORK_OWNER>` entschieden und hier nur festgehalten.

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Welcher Begriff? | „der KI-Client" durchgängig – er steht im Glossar und war im Kern in Gebrauch | Sperriger als ein Eigenname; die Kurzform vermeidet den Akteur ganz, die Langform kann das nicht überall |
| E2 | Nur `framework/core/` oder der ganze Kern? | Der ganze Kern nach der Definition des Glossars | Ein großes Release. Der halbe Weg hätte einen Kern hinterlassen, der seine eigene Zusage nachweislich nicht einlöst |
| E3 | 62 Versionsfelder heben? | Ja – `08-skill-conventions.md` 7 führt Formulierungen als PATCH | Die Testpflicht je Artefakt wird erneuert. Sie ist seit 0.13.0 ohnehin offen und hängt an AP2; der Preis ist derselbe, den E2 aus `FW-VN-01` ausdrücklich akzeptiert hat |
| E4 | AP2-Titel „Validierung der Devin-Funktionalitäten"? | Zu „Validierung der Clientfunktionalitäten" geändert | Der Titel war seit 0.14.0 falsch: AP2 ist für `claude-code` gefahren worden. Die Roadmap führte die Nennung unter „bewusst offen gelassen" – diese Begründung trägt nicht mehr |
| E5 | Dateiname `decision-trees/02-may-devin-do-task.md`? | **Nicht** umbenannt | Der Name trägt die Akteursbezeichnung weiter, an vier Stellen verlinkt. Eine Umbenennung berührt Querverweise, `FW-KO-04` und die Assemblierung des Hauptdokuments – eigener Vorgang mit eigenem Nachweis |

## 5. Nebenbefunde

- **`<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` ist an fünf Kernstellen weiter in Gebrauch**,
  obwohl `docs/PLACEHOLDER_REGISTRY.md` die clientneutrale Form
  `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>` bereits führt. Ausgewiesen, nicht geschlossen:
  Eine Markerumbenennung berührt Prüfung 7 und beide Client Packs.
- **Prüfung 13 prüft die Versionsfelder der Kernartefakte nicht.** Der Kopfkommentar sagt
  „jedes Versionsfeld gegen `MAJOR.MINOR.PATCH`" zu; tatsächlich deckt sie die Overlay-Version,
  `VERSION` und die Steckbriefangabe ab. Ein Checklisten-Versionsfeld `0.1` oder `abc` läuft
  glatt durch – belegt durch die Regressionsprobe R1. Derselbe Befundtyp wie `FW-KO-01`:
  eine Prüfung, die mehr zusagt, als sie leistet. Ausgewiesen, nicht geschlossen.
- **Ein Folgefehler im Code**, den Prüfung 14 aufgedeckt hat: `tests/scripts/validate-output.py`
  suchte den Abschnittstitel `Devin-Ergebnisbericht`, der mit diesem Antrag zu `Ergebnisbericht`
  wird. Ohne die Prüfung hätte das Skript ab sofort einen Abschnitt verlangt, den kein Skill
  mehr erzeugt.

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | `<TBD: angenommen / abgelehnt / mit Auflagen>` |
| Datum | `<TBD>` |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | `<TBD: E3, E4 und E5 einzeln entscheiden>` |
