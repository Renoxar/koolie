# Checkliste FW-CL-09 – Onboarding

| Attribut | Wert |
|---|---|
| ID | `FW-CL-09` |
| Version | `0.1.0` |
| Status | `entwurf` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Wann | während des Onboardings einer neuen Entwicklerin oder eines neuen Entwicklers; Abschluss vor der Freigabe zur selbstständigen Nutzung |
| Wer | Mentorin oder Mentor gemeinsam mit der oder dem Neuen |
| Dauer (Richtwert, Erläuterung) | verteilt über die Onboarding-Phase – keine verbindlichen Aufwände |
| Nachweis | Onboarding-Protokoll (Ablage gemäß Projekt, ohne Bewertungsdetails zur Person) |

## Zweck

Führt durch das Onboarding-Programm (`devin-core-framework/onboarding/GUIDE.md`) bis zur dokumentierten Freigabe für die selbstständige Devin-Nutzung. Maßstab ist souveräne Nutzung: Aufgaben angemessen abgrenzen, Kontext kontrolliert bereitstellen, Ergebnisse belastbar prüfen – nicht möglichst viel delegieren.

## Prüfpunkte

### Voraussetzungen

- [ ] **MUSS** Zugang zum Projekt-Repository und zu Devin Desktop vorhanden; Overlay-Status und Rollen des Projekts bekannt.
- [ ] **MUSS** Datenschutz- und Vertraulichkeitsunterweisung der Organisation absolviert (`<TBD: Referenz auf Unterweisung>`).
- [ ] **MUSS** `devin-core-framework/onboarding/QUICKSTART.md` gelesen; Übungsrepository (`devin-core-framework/onboarding/exercises/`) eingerichtet.

### Module (Reihenfolge gemäß `devin-core-framework/onboarding/GUIDE.md`)

- [ ] **MUSS** Modul 1 – Möglichkeiten und Grenzen: Leitprinzipien P1–P10, Delegationsverbote V1–V12 erklärt bekommen und an Beispielen eingeordnet.
- [ ] **MUSS** Modul 2 – Datenschutz und Kontextauswahl: Kontextklassen K0–K3 angewendet (Übung mit gemischten Quellen); Verhalten bei K3-Fund erklärt.
- [ ] **MUSS** Modul 3 – Sichere Arbeitsweise: Standardarbeitsablauf, Betriebsmodi M1–M5, Kontrollstufen mit Maximumprinzip; Preflight-Check zweimal unter Anleitung durchgeführt.
- [ ] **MUSS** Modul 4 – Framework-Struktur: Wurzel-Anweisungsdatei, Laufzeitschicht, Overlay, Packs, Prioritätshierarchie am Repository gezeigt.
- [ ] **MUSS** Modul 5 – Skills und Prompting: mindestens `fw-repo-analyze`, `fw-code-explain`, `fw-plan`, `fw-change-small`, `fw-tests` ausgeführt; Prompting-Regeln und unzulässige Muster besprochen.
- [ ] **MUSS** Modul 6 – Übungsaufgaben: alle synthetischen Übungen aus `devin-core-framework/onboarding/exercises/` bearbeitet, einschließlich der Negativübungen (Injektion, K3-Köder, Scope-Falle).
- [ ] **MUSS** Modul 7 – Test und Review: eigene Übungsänderung mit `devin-core-framework/checklists/04-review-ai-code.md` und `05-testing.md` geprüft; Ergebnisbericht und Nutzungsvermerk erstellt.
- [ ] **SOLL** Modul 8 – Typische Fehlanwendungen: Katalog aus `devin-core-framework/onboarding/GUIDE.md` durchgesprochen; eigene Beobachtungen ergänzt.

### Abschluss

- [ ] **MUSS** Wissenstest (`devin-core-framework/onboarding/KNOWLEDGE_CHECK.md`) im Selbsttest bestanden (Kriterien in `devin-core-framework/onboarding/COMPLETION_CRITERIA.md`); der Test dient der Selbstkontrolle, nicht der Personalbeurteilung.
- [ ] **MUSS** Erfolgskriterien aus `devin-core-framework/onboarding/COMPLETION_CRITERIA.md` gemeinsam durchgegangen; offene Punkte mit Folgeplan notiert.
- [ ] **MUSS** Freigabe zur selbstständigen Nutzung durch Mentorin oder Mentor dokumentiert (Datum, Rolle); bis dahin arbeitet die oder der Neue nur begleitet mit Devin.
- [ ] **SOLL** Nachschlagewerk (`devin-core-framework/onboarding/REFERENCE.md`) und Feedbackweg (`devin-core-framework/governance/FEEDBACK_PROCESS.md`) bekannt.

## Abbruch- und Eskalationskriterien

Wiederholte Regelverstöße in Übungen (zum Beispiel Übernahme ungeprüfter Ergebnisse, K3-Weitergabe) verlängern das begleitete Arbeiten; die Mentorin oder der Mentor entscheidet über zusätzliche Module (E0/E1). Das Onboarding-Protokoll enthält Sachstände, keine Leistungsbewertungen (V7).

## Ergebnis und Nachweis

Abgehakte Module, bestandener Selbsttest und dokumentierte Freigabe im Onboarding-Protokoll; die Freigabe wird im Projekt vermerkt (Rolle, Datum).
