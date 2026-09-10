# Leitwerk – Framework für den professionellen Einsatz von KI-Codierassistenten in Softwareentwicklungsteams

**Vorgehensmodell und technische Referenzimplementierung – projektneutral, wiederverwendbar, erweiterbar**

| | |
|---|---|
| Dokumentversion | 0.9.0 (entspricht Framework-Release 0.9.0) |
| Stand | 2026-09-10 |
| Status | Alle Module im Status `entwurf`; die technische Validierung gegen eine reale Installation erfolgt in Roadmap-Arbeitspaket AP2 und ist der einzige verbliebene P1 |
| Vertraulichkeit | projektneutral – enthält keine organisations-, kunden-, personen- oder infrastrukturspezifischen Inhalte; Beispiele sind synthetisch |
| Zielprodukt | Kein einzelnes. Der Kern ist werkzeugneutral; die Bindung an einen KI-Client leistet ein **Client Pack** (`leitwerk-core/clients/`). Verfügbar: `devin-desktop` – Devin Desktop (ehemals Windsurf) mit dem Agenten Devin Local, recherchierter Produktstand 3.8.20 vom 21.08.2026 – und `claude-code`. |
| **Reproduzierbarkeit** | Das Dokument wird aus dem Repository assembliert und baut aus einem frischen Auscheckstand. Laufzeitdateien stammen aus einer Referenzinstallation, die beim Bau entsteht; jede trägt die Angabe, aus welchem Client Pack sie kommt. |
| Bestandteile der Lieferung | dieses Hauptdokument (Markdown und Word) und das Referenz-Repository – das Repository ist die maßgebliche, versionierte Quelle aller eingebetteten Artefakte |
| Autorenschaft | erstellt als beauftragte Ausarbeitung; Verantwortungsübernahme durch `<FRAMEWORK_OWNER>` bei Übernahme |

**Lesehinweise:** Verbindlichkeit wird durchgängig über **MUSS / SOLL / KANN / DARF NICHT** ausgedrückt; normative Abschnitte sind als solche gekennzeichnet, Erläuterungen tragen den Zusatz „(Erläuterung)", Beispiele sind stets „**Beispiel (synthetisch)**". Jede Aussage über Produktfunktionen eines KI-Clients trägt einen Belegstatus: `[DOK]` offiziell dokumentiert (Quellen in Anhang 31.3), `[EMPF]` technisch begründete, noch nicht in einer Installation ausgeführte Empfehlung, `[KONZ]` konzeptioneller Vorschlag ohne Produktbezug; offene Prüfpunkte sind mit `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>` markiert. Variable Inhalte erscheinen ausschließlich als Platzhalter in spitzen Klammern (Register in Anhang 31.2); offene Projektentscheidungen als `<TBD: …>`. Verweise der Form `leitwerk-core/framework/core/…` bezeichnen Dateien des Referenz-Repositorys. Bestandteile der Laufzeitschicht werden im Fließtext mit **Begriffen** benannt (Wurzel-Anweisungsdatei, Regelablage, Berechtigungsdatei …); ihre Pfade je Client Pack führt Anhang 31.2.
