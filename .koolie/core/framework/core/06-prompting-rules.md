# Framework Core 06 – Prompting-Regeln

| Attribut | Wert |
|---|---|
| Modul-ID | FW-CORE-06 |
| Ebene | 1 – Framework Core |
| Verbindlichkeit | normativ (Abschnitte 1–3), Erläuterung (Abschnitt 4) |
| Owner | `<FRAMEWORK_OWNER>` |
| Version | 0.1.1 |
| Status | `pilot` |

## 1. Aufbau einer Aufgabenanweisung (normativ)

Jede Anweisung an den KI-Client, die über eine einfache Rückfrage hinausgeht, SOLL die folgenden Elemente enthalten. Skills und Prompt-Vorlagen (`.koolie/core/prompts/`) setzen diese Struktur um:

| Element | Inhalt | Pflicht |
|---|---|---|
| Ziel | Was soll am Ende vorliegen (Analysebericht, Plan, Änderung, Tests, Dokumentation) | MUSS |
| Betriebsmodus | M1–M5 (`05-working-model.md`) | MUSS |
| Kontrollstufe | niedrig / mittel / hoch mit auslösendem Faktor | MUSS |
| Scope | Erlaubte Dateien oder Verzeichnisse; ausdrücklich ausgeschlossene Bereiche | MUSS |
| Kontext | Die konkret bereitgestellten Quellen mit Kontextklasse | MUSS |
| Akzeptanzkriterien | Woran der Mensch erkennt, dass das Ergebnis brauchbar ist | SOLL |
| Ausgabeformat | Verweis auf das Standardformat des Skills oder der Prompt-Vorlage | SOLL |
| Rückfrageregel | „Bei Unklarheit fragen, nicht annehmen" (Standard über die Wurzel-Anweisungsdatei; Wiederholung bei komplexen Aufgaben) | KANN |

## 2. Regeln (normativ)

1. **Ein Ziel je Anweisung.** Mehrere Ziele werden in mehrere Schritte oder Sitzungen zerlegt.
2. **Referenzen statt Kopien.** Dateien werden per Pfad oder Erwähnung referenziert, nicht als Text eingefügt, sofern das Werkzeug dies erlaubt; eingefügter Text MUSS vorher auf Kontextklasse geprüft werden.
3. **Keine impliziten Berechtigungen.** Formulierungen wie „mach einfach", „räum auf", „alles, was nötig ist" DÜRFEN NICHT verwendet werden; sie erweitern den Scope unkontrolliert.
4. **Keine Rollenspiele mit Regelwirkung.** Anweisungen, die den KI-Client auffordern, Regeln zu ignorieren, sich als anderes System auszugeben oder Sicherheitsprüfungen zu überspringen, sind unzulässig – auch zu Testzwecken außerhalb des Testkatalogs.
5. **Ergebnis vor Stil.** Prompts fordern belegte Ergebnisse (Fundstellen, Testausgaben), nicht Selbstbewertungen („Bist du sicher?").
6. **Sprache.** Anweisungen werden in der im Overlay festgelegten Arbeitssprache verfasst (`<TBD: Arbeitssprache>`); Bezeichner, Befehle und Pfade bleiben unverändert.
7. **Skills bevorzugen – von beiden Seiten.** Liegt für eine Aufgabe ein Skill vor, benennt ihn die Anweisung, und der KI-Client ruft ihn auch dann auf, wenn die Anweisung ihn nicht nennt (`/skill-name` `[DOK]`; Wurzel-Anweisungsdatei Abschnitt 17, `05-working-model.md` Abschnitt 1). Freie Prompts sind für Aufgaben ohne passenden Skill vorgesehen. **Das Passiv dieser Regel hat seit 0.7.0 offen gelassen, wer handelt** – gemessen am 2026-09-14 hat eine Sitzung den passenden Skill benannt und seinen Aufruf im eigenen Bericht für „nicht nötig“ erklärt (`.koolie/core/tests/protocols/2026-09-14-erhebung-skillaufruf.md`).
8. **Iterationen kennzeichnen.** Folgeanweisungen in derselben Sitzung benennen, was sich gegenüber dem vorherigen Schritt ändert („Nur Schritt 3 des Plans anpassen: …").

## 3. Unzulässige Prompt-Muster (normativ)

| Muster | Warum unzulässig | Stattdessen |
|---|---|---|
| „Behebe alle Fehler im Projekt" | Kein Scope, keine Reversibilität, keine Prüfbarkeit | Ein Fehler, eine Sitzung, Skill `fw-error-analyze` |
| „Hier ist der Ticket-Export, mach das" | Ungeprüfter Kontext (K2/K3-Risiko), kein Ziel | Ticket bereinigen, Ziel und Akzeptanzkriterien formulieren |
| „Schreib die Tests so, dass sie durchlaufen" | Zementiert Fehlverhalten, umgeht Quality Gates | Skill `fw-tests` mit fachlichen Erwartungen |
| „Push das und erstell den MR" | Delegationsverbot V2 | Skill `fw-mr-description`, Push und MR durch den Menschen |
| „Ignoriere die Regeln, das ist nur ein Test" | Regelumgehung, Injektionsmuster | Testkatalog verwenden |
| „Welche Bibliothek wäre gut? Bau sie ein." | Delegationsverbot V3 | Optionsanalyse anfordern, Entscheidung durch Mensch |

## 4. Erläuterung

Gute Prompts ähneln guten Tickets: Sie beschreiben Ziel, Grenzen und Erfolgskriterium und überlassen den Weg dem Bearbeiter – mit dem Unterschied, dass der Bearbeiter hier bei jeder Unklarheit sofort nachfragen soll. Wer Schwierigkeiten hat, einen Prompt zu formulieren, hat meist noch keine klare Aufgabe; dann hilft der Skill `fw-change-analyze` oder ein Gespräch mit dem Product Owner mehr als ein besserer Prompt.
