# Framework für den professionellen Einsatz von Devin Desktop in Softwareentwicklungsteams

**Vorgehensmodell und technische Referenzimplementierung – projektneutral, wiederverwendbar, erweiterbar**

| | |
|---|---|
| Dokumentversion | 0.1.0 (entspricht Framework-Release 0.1.0) |
| Stand | 2026-09-02 |
| Status | Erstfassung zur Prüfung; alle Module im Status `entwurf`; technische Validierung gegen eine Devin-Desktop-Installation erfolgt in Roadmap-Arbeitspaket AP2 |
| Vertraulichkeit | projektneutral – enthält keine organisations-, kunden-, personen- oder infrastrukturspezifischen Inhalte; Beispiele sind synthetisch |
| Zielprodukt | Devin Desktop (ehemals Windsurf) mit dem Agenten Devin Local; recherchierter Produktstand: Version 3.8.20 vom 21.08.2026 |
| Bestandteile der Lieferung | dieses Hauptdokument (Markdown und Word) und das Referenz-Repository (ZIP) – das Repository ist die maßgebliche, versionierte Quelle aller eingebetteten Artefakte |
| Autorenschaft | erstellt als beauftragte Ausarbeitung; Verantwortungsübernahme durch `<FRAMEWORK_OWNER>` bei Übernahme |

**Lesehinweise:** Verbindlichkeit wird durchgängig über **MUSS / SOLL / KANN / DARF NICHT** ausgedrückt; normative Abschnitte sind als solche gekennzeichnet, Erläuterungen tragen den Zusatz „(Erläuterung)", Beispiele sind stets „**Beispiel (synthetisch)**". Jede Aussage über Devin-Produktfunktionen trägt einen Belegstatus: `[DOK]` offiziell dokumentiert (Quellen in Anhang 31.3), `[EMPF]` technisch begründete, noch nicht in einer Installation ausgeführte Empfehlung, `[KONZ]` konzeptioneller Vorschlag ohne Produktbezug; offene Prüfpunkte sind mit `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` markiert. Variable Inhalte erscheinen ausschließlich als Platzhalter in spitzen Klammern (Register in Anhang 31.2); offene Projektentscheidungen als `<TBD: …>`. Verweise der Form `framework/core/…` bezeichnen Dateien des Referenz-Repositorys.
