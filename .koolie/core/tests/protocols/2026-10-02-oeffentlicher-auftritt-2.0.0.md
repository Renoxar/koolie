# Protokoll: Stichprobe zur Umbenennung auf `koolie-*` (2.0.0)

| Feld | Inhalt |
|---|---|
| Datum | 2026-10-02 |
| Änderungsantrag | `CR-2026-173` (F9), D-539 |
| Client | `claude-code` 2.1.287, Modell `claude-opus-5-5`, Druckmodus, Berechtigungsmodus `default` |
| Kern | Arbeitsbaum des Branches `feature/oeffentlicher-auftritt-2.0.0` |
| Übungsrepositorium | Stand `d8c5b9b` (Kern 1.25.0) |
| Messort | `C:\lw-2000` (außerhalb des Benutzerprofils) |
| Kontingent | 5 Läufe / 4 USD (Owner, F9); verbraucht 3 Läufe / 1,49 USD |
| Ablage | `leitwerk-erhebungen-2026-10-02-2000` außerhalb des Repositoriums (Skripte `aufbau-2000.py`, `reihe-2000.py`, Belege je Lauf) |

## 1. Zweck

Die Umbenennung der mitgelieferten Skills ist eine Namensanpassung: Keine Anweisung ändert sich, und nach D-303 öffnet sich keine Zelle der Testblätter. Die Stichprobe prüft, ob der Client die Skills unter dem neuen Namen findet und aufruft – per Schrägstrich, modellseitig und in einem Projekt, das mit `install.py --update` von 1.25.0 gehoben wurde.

## 2. Aufbau

- **`basis-frisch`:** Übungsrepositorium, Kern per `install.py --target --update` aus dem Arbeitsbaum getauscht (die Migration des Packs `devin-desktop` im Archiv wurde gemeldet), `devin-desktop` entfernt, `claude-code` installiert, Overlay mit `cc-overlay-fuellen.py` gefüllt und aktiv.
- **`basis-gehoben`:** dasselbe Archiv, `claude-code` aber mit dem **Kern 1.25.0** installiert – `Skill(fw-code-explain)` in `allow` geprüft –, danach mit dem Kern des Arbeitsbaums `install.py --target --update`. Die Ausgabe meldete 13 umbenannte Skillordner, das entfernte Agentenprofil und die ersetzten Einträge der Berechtigungsdatei (`migration-basis-gehoben.log`).
- Wächter beider Basen: 13 Skills, alle `koolie-*`; kein `fw-` in der Berechtigungsdatei; `Skill(koolie-code-explain)` in `allow`; Agentenprofil `koolie-reviewer`, kein `fw-reviewer`; Hooks vorhanden; Overlay aktiv; Aufzeichnungen geschnitten.
- Die Migration nannte drei Projektdateien mit alten Namen (Overlay, Laufzeitfassung, README des Übungsrepositoriums). Sie wurden in den Messbäumen nachgezogen, wie der Hinweis es verlangt.
- Messbäume `s1` und `s2` aus `basis-frisch`, `s3` aus `basis-gehoben`, je mit eigener Historie. Vorprüfung vor jedem Lauf: Overlay aktiv, Vertrauen, Hook-Probe, Skill im `allow`-Korb, kein alter Name, Baum sauber.

## 3. Ergebnisse

| Lauf | Baum | Prompt | Werkzeugaufrufe | Abweisungen | Kosten | Ergebnis |
|---|---|---|---|---|---|---|
| `s1` | frisch | `/koolie-code-explain gebuehrErwachsene` | Skill clientseitig expandiert (`<command-name>/koolie-code-explain`); Grep, Read ×3, Grep | 0 | 0,54 USD | **trägt** – Ausgabe im Format des Skills, Kopf `koolie-code-explain v0.1.7` |
| `s2` | frisch | „Erklaere mir, wie die Methode gebuehrErwachsene funktioniert.“ | `Skill(koolie-code-explain)`, Grep, Read ×2 | 0 | 0,47 USD | **trägt** – das Modell wählt den Skill unter dem neuen Namen, die Regel in `allow` lässt ihn durch |
| `s3` | gehoben | „Erklaere mir, wie die Methode zaehleOffene funktioniert.“ | `Skill(koolie-code-explain)`, Grep, Read ×2 | 0 | 0,48 USD | **trägt** – die migrierte Berechtigungsdatei lässt den Aufruf ohne Rückfrage durch |

## 4. Bewertung

Alle drei Stichproben tragen. Die Umbenennung bleibt eine Namensanpassung; die Zellen der Testblätter bleiben abgenommen. Die Migration durch `install.py --update` wirkt an einer echten Installation von 1.25.0: Skillordner, Agentenprofil und Berechtigungsdatei tragen danach die neuen Namen, und der Client ruft den Skill ohne Rückfrage auf.

**Grenzen:** Ein Client, ein Skill, je Weg ein Lauf. Der Pack-Skill `koolie-ticket` und die übrigen Clients sind nicht gefahren; ihre Migration belegen die Sonden D539a bis D539h ohne Modell.

## 5. Aufräumen

Vertrauenseinträge für `C:\lw-2000\s1` bis `s3` wieder entfernt; Sicherung `C:\lw-2000\claude.json.vor-2000`. `C:\lw-2000` ist löschbar.
