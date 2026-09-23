# Protokoll: Vorbereitung des Freigabelaufs `1.0.0` – `FW-CL-11`, gemessener Stand je Prüfpunkt

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-23 |
| Release | Vorbereitung für `1.0.0` (`AP12`), erstellt im Release `0.90.0` |
| Änderungsantrag | `CR-2026-125` (Vorbereitung), `CR-2026-127` (offene Rollenfrage) |
| Art | **Vorbereitung, keine Freigabe.** Jeder Prüfpunkt der Checkliste `FW-CL-11` auf seinem gemessenen Stand |
| Gegenstand | `checklists/11-framework-release.md` Version `0.2.3`, 22 Prüfpunkte |
| Ergebnis | 🟢 **18 von 22 gedeckt.** 🔴 **Vier brauchen einen Menschen**, und einer davon ist blockierend |

> 🔴 **Dies ist NICHT die abgelegte Checkliste des Releases `1.0.0`.** Es ist die
> Vorbereitung dafür: Was maschinell gedeckt ist, ist gemessen; was ein Mensch tun muß,
> steht als solches da und ist **nicht** abgehakt. *Eine Checkliste, die sich selbst
> abhakt, ist keine.*

---

## 1. Der Stand je Prüfpunkt

Legende: 🟢 gedeckt und gemessen · 🔴 braucht einen Menschen · ⚪ fällt in den
Freigabelauf selbst

### Inhalt und Konsistenz

| Prüfpunkt | Stand am 2026-09-23 |
|---|---|
| Änderungsanträge abgeschlossen oder verschoben | ⚪ **Im Freigabelauf zu prüfen.** Gemessen: **127** Anträge, davon `CR-2026-127` **ausdrücklich offen** (Rollenfrage) |
| Konsistenz Core ↔ Laufzeitfassung je Client Pack | 🔴 **Stichprobe durch einen Menschen.** Prüfung 2, 4, 13, 21 und 76 decken die maschinellen Anteile; die Checkliste verlangt zusätzlich Stichproben je geändertem Modul |
| Skills konsistent zum Skill-Standard | 🟢 Prüfung 5, 25, 47, 61, 64 – Validator 0 Fehler |
| Version je geänderter Checkliste und Prompt gepflegt | 🟢 Prüfung 13 (Artefaktversionen) |
| Prioritätshierarchie unverändert oder begründet | ⚪ Im Freigabelauf |
| Templates, Checklisten, Entscheidungsbäume abgeglichen | ⚪ Im Freigabelauf (`SOLL`) |

### Projektneutralität

| Prüfpunkt | Stand am 2026-09-23 |
|---|---|
| `validate-framework.py` ohne Fehler, Warnungen bewertet | 🟢 **0 Fehler, 0 Warnungen** |
| `forbidden-terms.txt` im Release leer | 🟢 **gemessen: nur Kommentarzeilen, keine Begriffe** |
| Manuelle Stichprobe auf projekt-/kunden-/personenspezifische Inhalte | 🔴 **Braucht einen Menschen.** Die Checkliste sagt ausdrücklich *„zusätzlich zur automatischen Prüfung"* |
| Beispiele synthetisch gekennzeichnet, Platzhalterregister aktuell | 🟢 Prüfung 7, 14 |

### Produktstand der KI-Client

| Prüfpunkt | Stand am 2026-09-23 |
|---|---|
| Aktualitätsprüfung gegen die offizielle Clientdokumentation | 🔴 **Braucht einen Menschen.** Sie verlangt Abruf der Herstellerdokumentation und ein Urteil darüber; beides liegt außerhalb des freigegebenen Arbeitsbereichs (`AGENTS.md` Abschnitt 4: *„kein Web, keine externen Systeme ohne Freigabe"*) |
| Produktänderungen mit Regelwirkung als Änderungsanträge behandelt | ⚪ Folgt aus dem vorigen Punkt |

### Tests

| Prüfpunkt | Stand am 2026-09-23 |
|---|---|
| Testkatalog vollständig ausgeführt | 🟢 **125 Ergebniszellen**, sechs Meßtage, zwei Nachläufe |
| **(ab 1.0.0)** Kein Testfall auf `offen` | 🟢 **erfüllt** – Kriterium 2 von D-11 steht auf **0** |
| Skill-Testfälle für geänderte Skills erneut ausgeführt | ⚪ Im Freigabelauf; `0.90.0` hat keinen Skill geändert |
| Hook- und Validierungsskripte fehlerfrei | 🟢 Sondenlauf, **beide Kodierungsumgebungen** |
| Vollständiger Durchlauf M1→M2→M3→M4 auf dem Übungsrepositorium | ⚪ `SOLL`. ⚠️ **Braucht ein Kontingent** – ein Modelllauf über vier Betriebsmodi |

### Abschluss

| Prüfpunkt | Stand am 2026-09-23 |
|---|---|
| `VERSION` erhöht, `CHANGELOG.md` ergänzt | ⚪ Im Freigabelauf |
| Release-Archiv erzeugt, übernehmende Projekte informiert | ⚪ Im Freigabelauf |
| **Freigabe durch den Framework Owner dokumentiert** | 🔴 **Braucht einen Menschen.** Nicht delegierbar (`V1`, `V2`, `AGENTS.md` Abschnitt 16) |
| **(ab 1.0.0)** Alle Core-Module, Skills und Packs über `entwurf` | 🟢 **erfüllt** – 81 Träger mit Steckbriefzeile, **77 auf `pilot`**, vier Ausfüllschlitze, **0 auf `entwurf`** |
| **(ab 1.0.0)** Kein Decision Record auf `entschieden (Vorschlag)` | 🟢 **erfüllt** seit `0.49.0` |
| **(ab 1.0.0)** Übernahme in ein zweites Projekt nachgewiesen | 🟢 **erfüllt** – zwei übernehmende Projekte, beide gehoben (`FW-RE-01`) |

---

## 2. 🔴 Der blockierende Posten: die Gegenzeichnung

Er steht in keinem Prüfpunkt der Checkliste, sondern im **Arbeitspaket `AP11`** – und
solange er offen ist, ist `AP11` nicht abgeschlossen und `AP12` nicht fällig.

| Menge | gegengezeichnet | offener Abschnitt | ohne Abschnitt |
|---|---|---|---|
| alle **122** Protokolle | 13 | 45 | 64 |
| die **10** FW-Testprotokolle | 3 | 2 | 5 |

🔴 **Es ist keine Arbeit, sondern eine Rollenfrage.** An diesem Framework arbeitet **eine**
Person; eine Gegenzeichnung ist die Handlung einer **zweiten**. Die drei Wege und ihre
Preise stehen in **`CR-2026-127`**, Abschnitt 4. ➡️ *Eine Pflicht, die niemand erfüllen
kann, ist ein Befund über ihre Formulierung.*

---

## 3. Was die Sitzung braucht – und was sie nicht braucht

**Nicht mehr nötig** (mit `0.90.0` erledigt): Die Word-Fassung ist gebaut, für beide
Client Packs, mit acht eingebetteten Diagrammen.

| Block | Inhalt | Richtwert |
|---|---|---|
| 1 | **Die Rollenfrage entscheiden** (`CR-2026-127` E1 bis E4) | 15 min |
| 2 | Gegenzeichnungen nach dem gewählten Weg eintragen | 20 min |
| 3 | **Manuelle Stichprobe** – die geänderten Träger werden vorgelegt, der Owner sieht durch | 25 min |
| 4 | **Aktualitätsprüfung Clientdokumentation** – der Owner ruft ab, der Abgleich gegen die `[DOK]`-Aussagen läuft daneben | 30 min |
| 5 | Freigabe dokumentieren, `VERSION` auf `1.0.0`, Abnahmelauf | danach |

⚠️ **Der `SOLL`-Prüfpunkt M1→M2→M3→M4 ist der einzige Posten mit Kontingent.** Er ist ein
`SOLL`, kein `MUSS`; wird er nicht gefahren, gehört das ausgewiesen statt weggelassen.

---

## 4. Was hier **nicht** steht, und warum

- **Keine Zahl über die offenen Klärungspunkte.** 🔴 Sie ist mit keinem Werkzeug belastbar
  zu ermitteln: Drei Zählungen ergaben **50**, **64** und 15 nicht erkennbare Zeilen. Die
  Ursache ist `K-100` – die K-Zeilen stehen in **zwei** Tabellenformen mit der Statuszelle
  an verschiedenen Stellen, und die Statuswerte folgen keinem Vokabular. Das Register führt
  **104** Zeilen; die Übergabe nennt 13 offene. *Keine der drei Zahlen ist nachprüfbar
  falsch, und genau das ist der Befund.* **Offene Klärungspunkte sind kein Prüfpunkt von
  `FW-CL-11` und kein Kriterium von D-11** – sie blockieren `1.0.0` nicht.
- **Kein Haken.** Kein Prüfpunkt dieser Vorbereitung ist abgehakt. Das Abhaken geschieht im
  Freigabelauf, durch einen Menschen.
