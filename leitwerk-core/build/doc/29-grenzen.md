# 29 Bekannte Grenzen und offene Entscheidungen

## 29.1 Bekannte Grenzen dieser Erstfassung

**Keine Installationsvalidierung.** Kein Mechanismus wurde bislang in einer Zielinstallation von Devin Desktop ausgeführt. Die Referenzimplementierung beruht auf der offiziellen Dokumentation (Quellen in Anhang 31.3) und ist entsprechend gekennzeichnet; die Validierung ist als frühes Arbeitspaket AP2 mit Protokollpflicht eingeplant. Bis dahin gilt insbesondere: Der Schutz-Hook läuft fail-open (dokumentierte Entscheidung im Skript), die Berechtigungsvorlage ist gegen das dokumentierte, nicht gegen das real beobachtete Schema geschrieben, und alle dynamischen Tests des Testkatalogs stehen auf `offen`.

**Produktdynamik.** Devin Desktop entwickelt sich schnell (Rebranding Juni 2026, seither mehrere Releases). Aussagen mit Belegstatus `[DOK]` sind Momentaufnahmen des recherchierten Stands; die Governance begegnet dem mit Produktbeobachtung, Aktualitätstests (Klasse AK) und Hotfix-Pfad – ersetzt aber nicht die Prüfung vor der Einführung.

**Wirksamkeitsgrenzen der Kontrollen.** Regeln in `AGENTS.md` und `.devin/rules/` wirken über das Befolgungsverhalten des Modells und sind keine harte Durchsetzung; harte Grenzen ziehen nur Berechtigungen (`deny`), Hooks und organisationsweite Einstellungen. Das Framework kombiniert deshalb immer Verhaltensregel und technische Sperre – wo eine technische Sperre fehlt (zum Beispiel „nur Testpfade" in M4 bei gleichzeitig nötigem `edit`-Werkzeug), ist das ausgewiesen und durch Hook plus Review kompensiert. Ebenso bleibt Prompt Injection ein Restrisiko, das durch Datenbehandlungsregel, Permission-Modus Normal, Verbotslisten und Tests begrenzt, aber nicht eliminiert wird.

**Bewusste Auslassungen.** Kein konkretes Technology Pack (entsteht projektbezogen, AP4); nur ein Role Pack als Referenz; Devin Cloud/CLI/Fremdagenten standardmäßig deaktiviert; keine rechtlichen Bewertungen (N3); das Übungsrepository wird je Projekt im eigenen `<TECH_STACK>` erzeugt, damit Befehle real laufen.

**Methodische Grenzen.** Die Pilotmetriken messen Signale, keine Kausalitäten; die Selbsteinschätzungsanteile sind subjektiv; Vergleichbarkeit hängt an der Etikettierungsdisziplin. Das Framework erhöht zudem anfangs den Prozessaufwand (Preflight, Berichte, Vermerke) – der Pilot prüft ausdrücklich auch, ob dieser Aufwand im Verhältnis zum Nutzen steht.

## 29.2 Offene Entscheidungen

Alle offenen Punkte sind zentral im Decision Log geführt (Klärungstabelle K-01 bis K-20, Entscheidungen D-01 bis D-10 mit Status „Vorschlag", Annahmen A-01 bis A-05); die entscheidungsreife Kurzliste steht im Abschlussteil dieses Dokuments („Offene Entscheidungen"). Das vollständige Register:

{{EMBED-RAW:leitwerk-core/governance/DECISION_LOG.md:1}}
