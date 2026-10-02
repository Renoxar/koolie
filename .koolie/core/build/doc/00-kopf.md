# Koolie – Framework für den professionellen Einsatz von KI-Codierassistenten in Softwareentwicklungsteams

**Vorgehensmodell und technische Referenzimplementierung – projektneutral, wiederverwendbar, erweiterbar**

| | |
|---|---|
| Dokumentversion | 2.0.0 (entspricht Framework-Release 2.0.0) |
| Stand | 2026-09-28 |
| Status | Kein Modulträger steht auf `entwurf`; Prüfung 46 rechnet das bei jedem Validatorlauf nach. Die technische Validierung gegen reale Installationen (Roadmap-Arbeitspaket AP2) ist abgeschlossen; die Protokolle liegen unter `.koolie/core/tests/protocols/`. Was als Nächstes kommt, steht in der Roadmap (Kap. 30) |
| Vertraulichkeit | projektneutral – enthält keine organisations-, kunden-, personen- oder infrastrukturspezifischen Inhalte; Beispiele sind synthetisch |
| Zielprodukt | Kein einzelnes. Der Kern ist werkzeugneutral; die Bindung an einen KI-Client leistet ein **Client Pack** (`.koolie/core/clients/`). Ausgeliefert werden fünf: `devin-desktop`, `claude-code`, `openai-codex`, `kiro` und `cursor` (Reifegrad `pilot`). Welches Produkt ein Pack abbildet, gegen welche Zielversion und mit welchem Stand der Produktbeobachtung, steht im Pack selbst (Kap. 7a, 15.1), weil sich diese Angaben mit dem Produkt ändern. |
| Reproduzierbarkeit | Das Dokument wird aus dem Repository assembliert und baut aus einem frischen Auscheckstand. Laufzeitdateien stammen aus einer Referenzinstallation, die beim Bau entsteht; jede trägt die Angabe, aus welchem Client Pack sie kommt. |
| Bestandteile der Lieferung | dieses Hauptdokument (Markdown und Word) und das Referenz-Repository – das Repository ist die maßgebliche, versionierte Quelle aller eingebetteten Artefakte |
| Autorenschaft | erstellt als beauftragte Ausarbeitung; Verantwortungsübernahme durch `<FRAMEWORK_OWNER>` bei Übernahme |

**Warum Koolie?** Ein Koolie ist ein australischer Hütehund. Er treibt die Herde nicht und ersetzt den Schäfer nicht; er hält sie beisammen und in Richtung, selbständig, aber auf Anweisung. Das tut dieses Framework mit einem KI-Client: Es entscheidet nichts an seiner Stelle, sondern hält ihn in der Spur, an den Grenzen und an den Stellen, an denen ein Mensch entscheidet. Und ein Koolie ist eine Gebrauchsrasse, kein Schauhund: Was hier steht, muss im Alltag eines Projekts tragen.

**Lesehinweise:** Verbindlichkeit wird durchgängig über MUSS / SOLL / KANN / DARF NICHT ausgedrückt; normative Abschnitte sind als solche gekennzeichnet, Erläuterungen tragen den Zusatz „(Erläuterung)", Beispiele sind stets „Beispiel (synthetisch)". Jede Aussage über Produktfunktionen eines KI-Clients trägt einen Belegstatus: `[DOK]` offiziell dokumentiert (Quellen in Anhang 31.4), `[EMPF]` technisch begründete, noch nicht in einer Installation ausgeführte Empfehlung, `[KONZ]` konzeptioneller Vorschlag ohne Produktbezug; offene Prüfpunkte tragen den Belegstand `BELEG OFFEN` mit Grund und Datum. Variable Inhalte erscheinen ausschließlich als Platzhalter in spitzen Klammern (Register in Anhang 31.3); offene Projektentscheidungen als `<TBD: …>`. Verweise der Form `.koolie/core/framework/core/…` bezeichnen Dateien des Referenz-Repositorys. Bestandteile der Laufzeitschicht werden im Fließtext mit **Begriffen** benannt (Wurzel-Anweisungsdatei, Regelablage, Berechtigungsdatei …); ihre Pfade je Client Pack führt Anhang 31.2.
