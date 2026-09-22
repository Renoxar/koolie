# Änderungsantrag `CR-2026-059`

| Feld | Inhalt |
|---|---|
| Titel | Die drei Lücken aus `CR-2026-058` sind geschlossen – die restriktivere Liste gewinnt, die Sperre gilt im Hintergrund und zwei Ebenen tief |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-13 |
| Betroffene Artefakte | `clients/claude-code/CLIENT_PACK.md` (Zeilen **S3**, **A1**), `framework/core/05-working-model.md` (M1 und die Regel zu Hintergrund-Subagenten), `tests/scripts/validate-framework.py` (Prüfung 35 neu), `tests/scripts/probe-pruefungen.py`, `tests/EDGE_CASES.md` |
| Ebene laut Entscheidungsbaum 6 | **Client Pack** (Matrix) und **Core** (Arbeitsmodell) |
| Art | Nachtrag zu `CR-2026-058`: die drei dort ausdrücklich als **nicht gemessen** ausgewiesenen Punkte; **erhoben am 2026-09-13**, sieben Läufe, davon drei Kontrollläufe |
| Dringlichkeit | **Paket 6.** Kein P1: Alle vier Befunde fallen **zugunsten** der Durchsetzung aus. Der Antrag schließt Belegzusagen ab, die bis hierher als Erwartung dastanden |

## 1. Anlass

`CR-2026-058` hat drei Punkte ausdrücklich offen ausgewiesen, und die Roadmap nennt den ersten
davon „die billigste Anschlussmessung". Sie sind gemessen:
`tests/protocols/2026-09-13-erhebung-unteragent-tiefe.md`.

**Alle drei Aufbauten haben je einen eigenen Kontrolllauf**, und die Sonden schreiben diesmal
das Werkzeug vor – die Lehre aus Lauf V-M des Vortags, wo der Gegenstand sich sein Werkzeug
selbst gesucht hat.

### 1.1 Befund 1: Die restriktivere Liste gewinnt

| Lauf | Aufbau | Ergebnis |
|---|---|---|
| **ZS** | Skill sperrt `Write, Edit`; Profil nennt `tools: Read, Grep, Glob, **Write**` | **`Write` fehlte im Vorrat** |
| **ZS-K** | **Kontrolllauf:** derselbe Skill ohne das Feld | Unteragent zählte vier Werkzeuge auf und schrieb |

**Die Skill-Sperre schneidet aus dem Profilvorrat heraus.** Dieselbe Semantik, die D-64
gegenüber der `allow`-Liste gemessen hat: **Eine Erlaubnis holt ein entferntes Werkzeug nicht
zurück** – gleich, ob sie in der Berechtigungsdatei steht oder im Agentenprofil. Praktisch:
**Man kann die Liste nur enger machen, nie weiter.**

### 1.2 Befund 2: Die Sperre gilt im Hintergrund

`run_in_background: True` ist im Rekorder beider Läufe belegt. Messlauf: `Write` fehlte.
Kontrolllauf: derselbe Hintergrund-Unteragent schrieb.

**Das war die plausibelste Vermutung für eine Lücke** – ein Hintergrundlauf ist vom aufrufenden
Turn entkoppelt, und die Sperre gilt für den Turn. Sie besteht nicht.

### 1.3 Befund 3: Sie reicht mindestens zwei Ebenen tief

Der Start der zweiten Ebene **gelang** (zwei `Agent`-Aufrufe im Rekorder, der zweite mit
eigener `agent_id`), und `Write` fehlte auch dort. Der Kontrolllauf zeigt im selben Aufbau, wie
die zweite Ebene schreibt.

**„Mindestens zwei" ist wörtlich gemeint** – drei Ebenen sind nicht gemessen.

### 1.4 Befund 4, nicht gesucht: Ein beschränktes Profil kann keine Ebene öffnen

Das Profil `tools: Read, Grep, Glob` – **genau die Form, die `fw-reviewer` nach der Abbildung
trägt** – hat **kein Startwerkzeug**. Der Rekorder zeigt einen einzigen `Agent`-Aufruf, den des
Hauptagenten.

> **Das trägt die Zusage A1 an einer Stelle, an der sie sonst offen wäre:** Ein „rein lesendes"
> Reviewprofil könnte sich sonst über eine zweite Ebene erweitern, deren Profil weniger
> beschränkt ist. Es kann nicht – die Erweiterung bräuchte ein Werkzeug, das ihm fehlt.

**Und genau daran hängt eine stille Annahme.** Sie hält heute, weil
`agent_frontmatter.tool_names` kein Startwerkzeug abbildet. Erweitert jemand diese Abbildung,
fällt die Zusage **lautlos** – niemand prüft es. Das ist der Anlass für E1.

### 1.5 Beobachtung: Der Wortlaut des Clients überzeichnet seine eigene Reichweite

```text
Error: No such tool available: Write. Write is disabled for this session, in subagents
as well as here.
```

**Die zweite Hälfte bestätigt diese Erhebung. Die erste überzeichnet:** „for this session" ist
nicht gemessen – D-64 hat belegt, dass Turn 2 derselben Sitzung wieder schreiben konnte.

Das ist eine Aussage des Clients, **kein Messwert**. Es ändert an der Turngrenze nichts. Es
gehört trotzdem benannt: **Jede Nutzerin bekommt diese Zeile zu sehen, das Protokoll nicht.**

## 2. Was heute im Repositorium steht

| Stelle | Heutiger Stand | Warum das nicht bleiben kann |
|---|---|---|
| Zeile **S3** | „Nicht gemessen: Hintergrund-Unteragenten und zwei Ebenen tief" | Beides ist gemessen; der Satz beschreibt einen Stand von gestern |
| Zeile **A1** | keine Aussage zur zweiten Ebene | Die Zusage „rein lesend" ließe sich sonst durch eine untergeordnete Ebene aushebeln – gemessen geht das nicht, und das gehört dazugesagt |
| `05-working-model.md`, M1 | das Profil ist „der belastbarere Weg" | Richtig, und jetzt stärker belegbar: Es kann sich nicht selbst erweitern |
| `05-working-model.md`, Hintergrund-Subagenten | „technisch nicht abbildbar" | Bleibt richtig für „nur Hintergrund". **Neu ist:** Sperrt man ein Werkzeug, gilt das auch im Hintergrund – die Regel ist damit nicht so schutzlos, wie der Satz allein klingt |
| nichts | die stille Annahme aus 1.4 | Sie hält an einer Abbildung, die niemand gegen sie prüft |

## 3. Vorgeschlagene Änderung

1. **Zeile S3**: Die beiden „nicht gemessen"-Punkte werden durch die Messung ersetzt, und die
   Widerspruchsregel kommt dazu (die restriktivere Liste gewinnt).
2. **Zeile A1**: Befund 4 und die Beobachtung aus 1.5.
3. **`05-working-model.md`**: M1 und die Regel zu Hintergrund-Subagenten werden nachgezogen.
4. **Prüfung 35 (neu)**: Die erzeugte `tools`-Liste eines Agentenprofils darf keinen Namen aus
   `agent_start_tools` des Packs führen, und `agent_frontmatter.tool_names` darf keinen
   abbilden.
5. **`EDGE_CASES.md`**: ein Grenzfall zum Widerspruch zwischen Profil und Skill.

## 4. Auswirkungen

- **Keine Einstufung ändert sich.** S3 und A1 bleiben `[TECHNISCH]`; die Summen bleiben.
- **Vier Punkte wandern von „nicht gemessen" auf gemessen.**
- **Prüfung 35 fängt heute nichts** – siehe E1, und das steht so im Nachweis.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Vorschlag | Preis |
|---|---|---|---|
| **E1** | Soll eine Prüfung durchsetzen, dass ein Agentenprofil kein Startwerkzeug bekommt? | **Ja, Prüfung 35.** Die Zusage aus Befund 4 hängt heute allein daran, dass `agent_frontmatter.tool_names` kein Startwerkzeug abbildet – eine Erweiterung dieser Abbildung ließe sie **lautlos** fallen | **Sie fängt heute nichts**, weil die Abbildung das Werkzeug gar nicht kennt. Das ist dieselbe Bauart wie der fünfte Gegenstand der Prüfung 32 und **mit derselben Ehrlichkeit zu begründen: eine Verankerung, keine Behebung.** Wer sie als Risikoabwehr verkauft, überzeichnet |
| **E2** | Wird der irreführende Wortlaut des Clients ins Pack aufgenommen? | **Ja, als Beobachtung bei S3.** „for this session" ist nicht, was gemessen ist | Die Zeile wird noch länger, und sie zitiert eine fremde Fehlermeldung. **Dafür steht die Abweichung dort, wo jemand sie sucht** – wer die Meldung sieht und ihr glaubt, nimmt mehr Reichweite an, als belegt ist |
| **E3** | Wird der umgekehrte Widerspruch (Profil sperrt, Skill erlaubt) mitgemessen? | **Nein, und er wird als Erwartung ausgewiesen.** Nach Befund 1 ist er vorhersagbar; eine Vorhersage ist aber keine Messung, und das muss dastehen | Eine Lücke bleibt offen. **Die Alternative wäre, sie mit einer Erwartung zu schließen** – genau das, was sich dieses Projekt abgewöhnt hat |
| **E4** | Wird „mindestens zwei Ebenen" so formuliert, oder allgemein? | **Wörtlich „mindestens zwei".** Drei sind nicht gemessen | Die Formulierung wirkt kleinlich. Sie ist genau: Der Mechanismus legt mehr nahe, gemessen sind zwei |
| **E5** | Ein Release oder an 0.36.0 anhängen? | **Ein eigenes Release, `0.37.0`.** 0.36.0 ist gemergt; ein Nachtrag in dessen Protokoll würde verwischen, was wann gemessen wurde | Ein elftes Release am selben Tag. Der Preis ist Buchhaltung, der Gewinn ist eine saubere Belegkette |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle fünf Fragen wie vorgelegt.** E1 Prüfung 35, begründet als Verankerung und nicht als Risikoabwehr; E2 der Wortlaut des Clients kommt als Beobachtung in S3; E3 der umgekehrte Widerspruch bleibt ungemessen und wird als Erwartung ausgewiesen; E4 „mindestens zwei Ebenen" wörtlich; E5 eigenes Release `0.37.0` |
| Datum | 2026-09-13 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | D-72 (die restriktivere Liste gewinnt; Hintergrund und zweite Ebene sind mitgemessen), D-73 (ein Agentenprofil bekommt kein Startwerkzeug, und Prüfung 35 hält es fest) |
| Auflagen | **Die Grenzen der Messung bleiben in jeder Nennung stehen:** „mindestens zwei Ebenen", der ungemessene umgekehrte Widerspruch, und dass der Schutz-Hook nur für die **erste** Ebene als blockierend gemessen ist. **Die Begründung für Prüfung 35 wird nicht zur Risikobehauptung aufgewertet** – sie fängt heute nichts, und der Wirkungsnachweis sagt das. **Und die Clientmeldung wird als Zitat kenntlich gemacht**, nicht als Belegsatz des Frameworks |
| Ziel-Release | `0.37.0` |
| Umsetzung | umgesetzt mit `0.37.0` |
