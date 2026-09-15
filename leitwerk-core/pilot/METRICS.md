# Metriken für Pilot und Betrieb

| Attribut | Wert |
|---|---|
| ID | `FW-PILOT-METRICS` |
| Version | `0.1.1` |
| Status | `pilot` |
| Owner (Rolle) | Projektleitung des Pilotprojekts mit `<FRAMEWORK_OWNER>` |

> **Alle Metriken sind Vorschläge.** Zielwerte werden ausdrücklich **nicht** durch das Framework vorgegeben; sie sind projektspezifisch festzulegen (`<TBD: Zielwerte je Metrik>`) – und erst, nachdem die Referenzbasis erhoben ist. Einzelne Metriken erlauben keine belastbare Aussage über den Gesamtnutzen; bewertet wird immer das Bündel aus Produktivität, Qualität, Sicherheit und Akzeptanz. Keine Metrik wird zur Personenbewertung verwendet oder personenbezogen berichtet (V7); Befragungen sind freiwillig.

## 1. Erhebungsgrundsätze (normativ)

1. Definition vor Erhebung: Jede verwendete Metrik erhält vor Pilotstart eine schriftliche Definition (Quelle, Formel, Etiketten, Ausschlüsse) – sonst wird sie nicht erhoben.
2. Quellen: `<ISSUE_TRACKER>` (Zeiten, Wiedereröffnungen), `<CI_CD_PLATFORM>` (Pipeline-Läufe), Merge-Request-System (Iterationen, Vermerke), KI-Nutzungsvermerk (Stufe, Modus, Skills, verworfene Vorschläge, Selbsteinschätzungen), Befragungen (Akzeptanz).
3. Vergleiche nur innerhalb gleicher Aufgaben-Etiketten (Kategorie, Kontrollstufe, Größenklasse; `PILOT_CONCEPT.md` Abschnitt 2).
4. Aggregation mindestens auf Teamebene; Rohdaten mit Personenbezug werden nicht verteilt.

## 2. Vorgeschlagene Metriken

### Produktivität und Aufwand

| Metrik | Definition (Vorschlag) | Quelle | Hinweis zur Deutung |
|---|---|---|---|
| Bearbeitungszeit je Aufgabe | Zeit von „in Arbeit" bis „Review bereit", je Etikett | `<ISSUE_TRACKER>` | nur im Etikettvergleich aussagekräftig |
| Nachbearbeitungsaufwand | Selbsteinschätzung je KI-Aufgabe in Kategorien (keiner/gering/erheblich/verworfen) | Nutzungsvermerk | subjektiv, aber trendfähig |
| Review-Aufwand | Anzahl Review-Iterationen je MR; Zeit bis Merge ab Review-Start | MR-System | steigender Review-Aufwand kann Produktivitätsgewinne aufzehren |
| Anzahl notwendiger Rückfragen | Rückfragen je KI-Aufgabe (aus Ergebnisberichten) | Nutzungsvermerk | hohe Werte zeigen unklare Aufgaben, nicht schlechtes Werkzeug |

### Qualität

| Metrik | Definition (Vorschlag) | Quelle | Hinweis zur Deutung |
|---|---|---|---|
| Fehlerquote | Fehlertickets, die auf Änderungen des Zeitraums zurückgehen, je Etikett | `<ISSUE_TRACKER>` | Latenz beachten (Fehler zeigen sich später) |
| Wiedereröffnungen | wieder geöffnete Tickets/MRs je Etikett | `<ISSUE_TRACKER>` | – |
| Testabdeckung geänderter Bereiche | Abdeckung der im Zeitraum geänderten Module laut `<QUALITY_GATE>` | CI | Abdeckung ist notwendig, nicht hinreichend |
| Build- und Pipelinefehler | fehlgeschlagene Läufe je MR bis zum Merge | `<CI_CD_PLATFORM>` | – |
| Verständlichkeit erzeugter Änderungen | Reviewer-Einschätzung je KI-MR (Kategorien gut/mittel/schwer nachvollziehbar) | Review | erhebt der Reviewer, bewertet die Änderung, nicht die Person |

### Nutzung und Steuerung

| Metrik | Definition (Vorschlag) | Quelle | Hinweis zur Deutung |
|---|---|---|---|
| Anteil verworfener KI-Vorschläge | verworfen laut Nutzungsvermerk / alle KI-Aufgaben | Nutzungsvermerk | gesunder Wert ist nicht 0: Verwerfen ist Qualitätsverhalten |
| Verteilung Kontrollstufen und Modi | KI-Aufgaben je Stufe/Modus | Nutzungsvermerk | nur hohe Stufen ohne M1/M2-Anteil deutet auf Preflight-Lücken |
| Eskalationen je Stufe (E0–E4) | Anzahl und Gründe | Ergebnisberichte, Register | E0 ist Alltag; E3/E4-Häufung ist Framework-Signal |
| Checklisten-/Vermerk-Vollständigkeit | Stichprobe: MRs mit vollständigem Nutzungsvermerk | MR-System | Prozesstreue-Indikator |

### Akzeptanz und Entlastung

| Metrik | Definition (Vorschlag) | Quelle | Hinweis zur Deutung |
|---|---|---|---|
| Akzeptanz durch Entwicklerinnen und Entwickler | kurze, freiwillige Befragung je Review-Punkt (Skala + Freitext): Nützlichkeit, Vertrauen in Ergebnisse, Regelpraktikabilität | Befragung | anonym auswertbar; Freitexte sind die wertvollste Quelle |
| Wahrgenommene Entlastung | Befragungsitem: „Der KI-Client entlastet mich bei …/belastet mich bei …" | Befragung | Entlastung bei Analyse und Doku ist häufig der frühste echte Effekt |
| Onboarding-Wirkung | Selbsteinschätzung neuer Teammitglieder zur Einarbeitungsunterstützung | Befragung | Kernziel des Frameworks |

## 3. Auswertung (normativ)

Je Review-Punkt: Bündelbetrachtung gegen Referenzbasis, auffällige Einzelwerte nur als Einstieg in Ursachenanalyse (nie als Urteil), Gegenlesen der Freitexte, Abgleich mit Vorfällen und Feedback. Der Abschlussbericht stellt Nutzen **und** Kosten dar (auch Regel-Reibung, Review-Mehraufwand, Framework-Pflege) und benennt Unsicherheiten der Messung, statt Scheingenauigkeit zu erzeugen.
