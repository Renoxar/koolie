# RACI-Vorlage – Betrieb des Frameworks

| Attribut | Wert |
|---|---|
| ID | `FW-GOV-RACI` |
| Version | `0.1.0` |
| Status | `entwurf` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |

> **Ausfüllhinweis:** Die Vorlage arbeitet ausschließlich mit generischen Rollen; reale Rolleninhaber werden **nicht** hier, sondern im Teamverzeichnis der Organisation zugeordnet. R = Responsible (führt aus), A = Accountable (verantwortet, genau ein A je Zeile), C = Consulted, I = Informed. Projekte KÖNNEN Spalten ergänzen (zum Beispiel Betriebsrollen), DÜRFEN aber keine A-Zuordnungen des Frameworks auf Devin oder auf „automatisch" setzen – Verantwortung liegt immer bei Menschen (P1).

| Aktivität | Framework Owner | Modul-Owner | Overlay Owner (`<APPROVAL_ROLE>`) | Entwicklerin / Entwickler | Reviewer | `<ARCHITECT_ROLE>` | `<SECURITY_CONTACT>` | `<DATA_PROTECTION_CONTACT>` | `<PRODUCT_OWNER_ROLE>` | Mentorin / Mentor | Projektleitung |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Framework-Release erstellen und freigeben | A/R | R | I | I | – | C | C | C | – | – | I |
| Framework Core ändern (Änderungsantrag) | A | R | C | C | – | C | C | C | – | – | I |
| Prioritätshierarchie ändern | A/R | C | C | I | – | C | C | C | – | – | I |
| Role Pack / Technology Pack pflegen | C | A/R | I | C | – | C | C | – | – | – | – |
| Neuen Skill freigeben (Status aktiv) | A | R | C | C | C | – | C | – | – | – | – |
| Skill deprecaten / zurückziehen | A | R | I | I | – | – | – | – | – | – | – |
| Project Overlay erstellen und pflegen | C | – | A/R | C | – | C | C | C | C | – | I |
| Overlay aktivieren (Projektübernahme, CL-10) | C | – | A/R | I | – | C | C | C | – | – | I |
| K2-Kontextfreigabe (Einzel/Kategorie) | – | – | A/R | R | – | – | C | C (bei Personenbezug A) | – | – | – |
| Devin-Aufgabe durchführen (Preflight bis Ergebnisbericht) | – | – | – | A/R | – | – | – | – | C | C (im Onboarding) | – |
| Freigabe Kontrollstufe hoch | – | – | A/R | R | – | C | C (bei R3/R10 A mitzeichnend) | C (bei R4) | – | – | I |
| Review KI-generierter Änderungen | – | – | – | R (Selbstreview) | A/R | C (Stufe hoch) | C (Stufe hoch) | – | – | – | – |
| Merge / Release der Projektsoftware | – | – | C | R | C | C | C | – | C | – | A |
| Neue Abhängigkeit einführen (CL-07) | – | – | A | R | C | C | C | – | – | – | I |
| Sicherheits-/Datenschutzvorfall mit KI-Bezug behandeln | I | – | C | R (Meldung) | – | – | A/R | A/R (bei Personenbezug) | – | – | I |
| Lessons Learned und Feedback auswerten | A/R | R | C | C | C | – | C | – | – | C | I |
| Ausnahme genehmigen (EXCEPTION_PROCESS) | A (Core) | C | A (Overlay) | R (Antrag) | – | C | C | C | – | – | I |
| Onboarding durchführen und freigeben | C | – | I | R (Lernende) | – | – | – | – | – | A/R | I |
| Pilot planen und auswerten | C | – | R | C | C | – | – | C (Befragungen) | C | – | A |
| Aktualitätsprüfung gegenüber Devin-Produktänderungen | A/R | R | I | I | – | – | C | – | – | – | – |
| Auditnachweise bereitstellen | A/R | C | R | C | – | – | C | C | – | – | I |

**Konsistenzregeln:** Je Zeile genau ein A (bei geteilten A ist die Aufteilung vermerkt: mitzeichnend). Devin taucht in keiner Spalte auf – es ist Werkzeug, nicht Rolle. Bei Personalunion mehrerer Rollen in kleinen Teams MUSS das Vier-Augen-Prinzip je Zeile erhalten bleiben (dann übernimmt eine andere benannte Rolle das C/Review).
