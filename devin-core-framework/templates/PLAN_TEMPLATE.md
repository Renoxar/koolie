# Änderungsplan – Vorlage (Betriebsmodus M2 Guided Planning)

<!-- Verwendung: Ausgabeformat des Skills fw-plan und Grundlage der Planbestätigung (Schritt 9 des
     Standardarbeitsablaufs). Der Plan wird vom Menschen bestätigt (Stufe mittel) oder durch
     <APPROVAL_ROLE> freigegeben (Stufe hoch). Jede Planänderung nach Bestätigung erfordert eine
     erneute Bestätigung. Keine Personen, keine internen Adressen, keine Secrets. -->

## Änderungsplan: <Kurztitel> (<Ticket-Referenz oder Platzhalter>)

| Attribut | Wert |
|---|---|
| Erstellt mit | `fw-plan` v<Version> |
| Betriebsmodus der Umsetzung | M3 / M4 / M5 |
| Kontrollstufe | <niedrig / mittel / hoch> (auslösender Faktor <R#>) |
| Bestätigungsstatus | entwurf / bestätigt durch <Rolle> am <Datum> / abgelehnt |

### 1. Ziel und Akzeptanzkriterien
- Ziel: <...>
- Akzeptanzkriterien: <...>

### 2. Ist-Zustand (Befunde mit Fundstellen)
- <pfad/datei:zeile – Befund>

### 3. Annahmen (gekennzeichnet) und offene Fragen
- Annahme A1: <...> (Auswirkung, falls falsch: <...>)
- Offene Frage F1: <...> → benötigte Entscheidung durch <Rolle>

### 4. Bewertete Optionen
| Option | Beschreibung | Risiko | Aufwand | Reversibilität | Konsistenz mit Architektur | Empfehlung (Vorschlag) |
|---|---|---|---|---|---|---|
| A | <...> | <...> | <...> | <...> | <...> | <...> |
| B | <...> | <...> | <...> | <...> | <...> | <...> |

### 5. Schritte der Umsetzung (klein, einzeln prüfbar)
| Nr. | Schritt | Betroffene Dateien | Erwartetes Zwischenergebnis | Prüfung nach dem Schritt |
|---|---|---|---|---|
| 1 | <...> | <...> | <...> | <Test/Lint/manuell> |

### 6. Teststrategie
- Neue oder geänderte Tests: <...>
- Auszuführende Befehle: `<TEST_COMMAND>`, `<LINT_COMMAND>`
- Nicht automatisiert prüfbar: <...> → manueller Prüfschritt: <...>

### 7. Risiken und Gegenmaßnahmen
| Risiko | Auswirkung | Gegenmaßnahme |
|---|---|---|
| <...> | <...> | <...> |

### 8. Rollback
- <Wie wird die Änderung vollständig zurückgenommen (Revert, Reihenfolge)>

### 9. Abbruchkriterien während der Umsetzung
- <z. B. Berührung weiterer Komponenten, fehlgeschlagene Tests außerhalb des Scopes>

### 10. Freigabe
- Erforderlich: <Bestätigung Bearbeiter / Reviewer | Freigabe <APPROVAL_ROLE> (+ <SECURITY_CONTACT>)>
- Erteilt durch (Rolle) / Datum / Referenz: <...>
