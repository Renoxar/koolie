# Änderungsantrag `CR-2026-035`

| Feld | Inhalt |
|---|---|
| Titel | Die erklärende README der Regelablage steht im Regelregister des Clients |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-11 |
| Betroffene Artefakte | `clients/devin-desktop/root-template/.devin/rules/README.md`, `clients/claude-code/root-template/.claude/rules/README.md`, beide `manifest.json` (`core_paths`), `clients/README.md` (Abschnitt 5), `tests/scripts/validate-framework.py` (optional, siehe E3) |
| Ebene laut Entscheidungsbaum 6 | Abbildungsschicht – Inhalt der Regelablage; betrifft **beide** Client Packs |
| Art | Behebung von `AP2-DD-17` (Schwere: niedrig) |
| Dringlichkeit | regulär |

## 1. Anlass und Problem

`devin rules list` führt die Regelablage als Regelmenge auf – und darin:

```text
README [Devin] manual
```

Die Datei lädt **nicht** automatisch. Sie steht aber im Register und ist mit dem Trigger `manual`
**auf ausdrückliche Erwähnung hin ladbar**. Eine erklärende Datei in einem Verzeichnis, dessen
Inhalt der Client als Regelmenge liest.

### Warum das trotz niedriger Schwere zählt

**Was in ihr steht, ist keine Regel, sondern Belegstand.** Die Datei führt `[DOK]`-Tabellen,
VERIFY-Marker, ein Nummernschema und – bemerkenswert – die Zeichenlimits „12.000 je
Workspace-Regeldatei, 6.000 für globale Regeln", also genau die Angabe, deren Einstufung
`CR-2026-027` als für Devin Local unbelegt beanstandet.

Wird die Datei geladen, tragen damit Aussagen **mit ausgewiesenem Belegvorbehalt** den Rang eines
Regeltexts der Ebene 3. Das Verzeichnis ist die Regelablage; alles darin ist möglicher Kontext.
Ein Belegstand gehört in ein Dokument, das erklärt – nicht in eines, das anweist.

### Was das Register über die Ablage sagt

Gegenprobe G-1 zählt in der Oberfläche **sechs** geladene beziehungsweise geführte Regeln: die
vier Framework-Regeln, `global_rules` aus dem Benutzerprofil (`AP2-DD-15`) und diese README. Die
**zweite** README des Packs – `.devin/README.md`, eine Ebene über der Regelablage – erscheint
nicht.

Daraus folgt, was die Abhilfe trägt: **Der Client registriert, was in der Regelablage liegt, und
nicht, was daneben liegt.** Erschlossen aus der Zählung der Gegenprobe, nicht eigens gemessen.

### Offen: das Frontmatter

Die Datei trägt **kein Frontmatter**, der Client führt sie dennoch mit Trigger `manual`. Ob
`manual` die dokumentierte Vorgabe für Regeldateien ohne `trigger` ist, ist nicht belegt – neue
Klärungsfrage **K-25**. Für die Abhilfe ist das gleichgültig: Eine Datei, die nicht angewiesen
werden soll, gehört nicht in die Ablage, unabhängig davon, mit welchem Trigger der Client sie
führt.

## 2. Vorgeschlagene Änderung

**Empfohlen – die erklärende Datei verlässt die Regelablage.** Ihr Inhalt geht in die bestehende
Laufzeit-README eine Ebene höher (`<RUNTIME_DIR>/README.md`) auf, als eigener Abschnitt
„Regelablage". In der Regelablage bleibt damit nur, was Regel ist.

Beide Packs sind betroffen; für `claude-code` ist die Wirkung unerhoben (**K-26**: Führt dieser
Client eine README der Regelablage ebenfalls im Register?). Die Änderung ist dort trotzdem
richtig – sie folgt aus der Zuständigkeit des Verzeichnisses, nicht aus dem Verhalten eines
Clients.

Beide Dateien stehen in `core_paths` der Manifeste. **`install.py --update` erneuert sie**; die
Änderung erreicht bestehende Installationen ohne Handgriff, die alte Datei ist bei der Migration
jedoch zu entfernen – sie wird durch das Update nicht gelöscht (Migrationshinweis erforderlich).

Zwei Alternativen, mit ihren Kosten, damit die Entscheidung nicht ohne sie fällt:

| Weg | Wirkung | Kosten |
|---|---|---|
| **A – verschieben (empfohlen)** | Die Regelablage enthält nur Regeln | Ein Migrationshinweis; ein Ort mehr, an dem der Belegstand zu suchen ist |
| **B – Frontmatter `trigger: manual` und erster Satz „Dies ist keine Regel"** | Der Trigger ist ausdrücklich statt implizit | Sie bleibt im Register. Eine Datei, die sagt, sie sei keine Regel, ist eine Regel, die das sagt |
| **C – unverändert lassen, in Abschnitt 5 des Packs ausweisen** | Nichts zu migrieren | Der Belegvorbehalt bleibt ladbar; der Befund wird beschrieben statt behoben |

## 3. Was dieser Antrag nicht ändert

- **Den Inhalt der README.** Der Belegstand der Regelmechanismen ist wertvoll und bleibt
  vollständig erhalten – er wechselt nur den Ort.
- **Die Regeltexte, das Nummernschema und die Ladetrigger.** Unverändert.
- **Die Aussage über die Zeichenlimits.** Sie steht und fällt mit `CR-2026-027`; dieser Antrag
  nimmt ihr nur den Rang eines ladbaren Regeltexts.

## 4. Grenze der Zusage

**Die Ablage wird sauber, der Kanal bleibt.** Wer eine beliebige Datei in die Regelablage legt,
erzeugt weiterhin einen Registereintrag. Das Framework kann das für seine eigenen Dateien
entscheiden, nicht für fremde – und für Quellen außerhalb des Projekts schon gar nicht
(`CR-2026-031`).

**Für `claude-code` ist die Wirkung nicht gemessen** (K-26). Die Änderung ist dort begründet,
aber nicht belegt veranlasst.

**Der Befund ist niedrig und bleibt es.** Die Datei lädt nicht von selbst; es braucht eine
ausdrückliche Erwähnung. Gemeldet wird hier eine Möglichkeit, kein beobachteter Schaden.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Welcher der drei Wege? | **A – verschieben.** Ein Verzeichnis, das als Regelmenge gelesen wird, enthält nur Regeln | Migrationshinweis nötig; `install.py --update` legt die neue Fassung an, entfernt die alte aber nicht |
| E2 | Auch bei `claude-code` ändern, obwohl dort unerhoben? | **Ja.** Die Begründung ist die Zuständigkeit des Verzeichnisses, nicht das Verhalten eines Clients | Eine Änderung ohne Befund am betroffenen Pack – vertretbar, aber nicht durch eine Messung veranlasst |
| E3 | Prüfung aufnehmen, die Nicht-Regeltexte in der Regelablage meldet? | **Ja.** In `clients/*/root-template/<Regelablage>/` darf nur liegen, was dem Nummernschema folgt. Sonde nach D-23: eine Fremddatei in einer Kopie – die Prüfung meldet | Sie prüft die **Vorlage**, nicht die installierte Ablage: Was ein Projekt dort selbst ablegt, sieht sie nicht |
| E4 | K-25 (Trigger-Vorgabe ohne Frontmatter) jetzt klären? | **Nein, nur erfassen.** Für die Abhilfe ist die Antwort gleichgültig | Eine unbeantwortete Frage mehr in der Klärungstabelle; sie wird erst wichtig, wenn ein Pack sich auf den Standardtrigger verlassen will |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** |
| Datum | 2026-09-11 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | E1 bis E4 wie vorgelegt: **Weg A** – der erklärende Text verlässt die Regelablage und geht in die Laufzeit-README eine Ebene höher auf; die Änderung gilt für **beide** Packs, auch wenn die Wirkung bei `claude-code` unerhoben ist (K-26); die Prüfung auf Nicht-Regeltexte in der Vorlage der Regelablage wird aufgenommen; K-25 wird nur erfasst. Migrationshinweis erforderlich – `install.py --update` löscht die alte Datei nicht. Ziel-Release 0.26.0 |
| Umsetzung | **mit Release 0.26.0** – Einzelheiten und Nachweise in `leitwerk-core/CHANGELOG.md` |
