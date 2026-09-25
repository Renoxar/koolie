# 29 Bekannte Grenzen und offene Entscheidungen

## 29.1 Bekannte Grenzen dieser Erstfassung

> **Dieser Abschnitt beschreibt den Stand der Erstfassung vom 2026-09-01 und wird nicht
> fortgeschrieben.** Er bleibt als Zeitdokument erhalten; mehrere Aussagen darin gelten
> **nicht mehr**. Der aktuelle Stand steht in `.koolie/core/docs/ROADMAP.md`, Abschnitt
> „Stand nach Release …", und im `CHANGELOG.md`. Die wichtigsten Änderungen, mit Release
> und Beleg:
>
> - **Die Installationsvalidierung ist erfolgt und abgeschlossen.** AP2 ist für beide
>   Client Packs gefahren (2026-09-10 und 2026-09-11) und für `devin-desktop` mit
>   Release 0.86.0 **zu Ende geführt** – 70 Sitzungsläufe an einer Installation. Neun
>   Matrixzeilen sind dort beobachtet, genau eine sagt noch `BELEG OFFEN`. Die Protokolle
>   liegen unter `.koolie/core/tests/protocols/`.
> - **Der Schutz-Hook läuft nicht mehr fail-open.** Seit 0.24.0 blockiert er eine Eingabe,
>   die er nicht lesen kann, sofern das Client Pack das Eingabeschema als bestätigt führt
>   (`hook_fail_closed`, D-31). Beide Manifeste führen es.
> - **Ein dynamischer Test steht wieder auf `offen`** (seit Release 1.11.0): `SK-002-N03`
>   hat auch im Nachlauf weder angehalten noch die Meldung an `<SECURITY_CONTACT>` empfohlen
>   (D-404, `K-153`). Die übrigen 37 Zellen des zentralen Katalogs und 86 der 87 Zellen der
>   dreizehn Testblätter tragen `bestanden`, der Nachweis je Zelle mit Protokoll und Client Pack.
> - **Kein Modulträger steht mehr auf `entwurf`** (seit Release 0.53.0), und **kein
>   Decision Record mehr auf `entschieden (Vorschlag)`** (seit Release 0.49.0).
> - **Die verbindliche Zielversion beider Packs ist festgelegt** (D-112). Sie ist der
>   *geprüfte* Geltungsbereich und nicht der aktuelle Produktstand; den Abstand zwischen
>   beiden weist das jeweilige Pack aus.
>
> Berichtigt mit `CR-2026-051` (Befund **B12** des unabhängigen Reviews vom 2026-09-12),
> fortgeschrieben mit `CR-2026-124` (Release 0.89.0).

**Keine Installationsvalidierung.** Kein Mechanismus wurde bislang in einer Zielinstallation des KI-Clients ausgeführt. Die Referenzimplementierung beruht auf der offiziellen Dokumentation (Quellen in Anhang 31.4) und ist entsprechend gekennzeichnet; die Validierung ist als frühes Arbeitspaket AP2 mit Protokollpflicht eingeplant. Bis dahin gilt insbesondere: Der Schutz-Hook läuft fail-open (dokumentierte Entscheidung im Skript), die Berechtigungsvorlage ist gegen das dokumentierte, nicht gegen das real beobachtete Schema geschrieben, und alle dynamischen Tests des Testkatalogs stehen auf `offen`.

**Produktdynamik.** Devin Desktop entwickelt sich schnell (Rebranding Juni 2026, seither mehrere Releases). Aussagen mit Belegstatus `[DOK]` sind Momentaufnahmen des recherchierten Stands; die Governance begegnet dem mit Produktbeobachtung, Aktualitätstests (Klasse AK) und Hotfix-Pfad – ersetzt aber nicht die Prüfung vor der Einführung.

**Wirksamkeitsgrenzen der Kontrollen.** Regeln in der Wurzel-Anweisungsdatei und in der Regelablage wirken über das Befolgungsverhalten des Modells und sind keine harte Durchsetzung; harte Grenzen ziehen nur Berechtigungen (`deny`), Hooks und organisationsweite Einstellungen. Das Framework kombiniert deshalb immer Verhaltensregel und technische Sperre – wo eine technische Sperre fehlt (zum Beispiel „nur Testpfade" in M4 bei gleichzeitig nötigem `edit`-Werkzeug), ist das ausgewiesen und durch Hook plus Review kompensiert. Ebenso bleibt Prompt Injection ein Restrisiko, das durch Datenbehandlungsregel, Permission-Modus Normal, Verbotslisten und Tests begrenzt, aber nicht eliminiert wird.

**Bewusste Auslassungen.** Kein konkretes Technology Pack (entsteht projektbezogen, AP4); nur ein Role Pack als Referenz; Cloud-Sitzungen, Läufe ohne beobachtende Person und Fremdagenten standardmäßig deaktiviert (D-10, D-386); keine rechtlichen Bewertungen (N3); das Übungsrepository wird je Projekt im eigenen `<TECH_STACK>` erzeugt, damit Befehle real laufen.

**Methodische Grenzen.** Die Pilotmetriken messen Signale, keine Kausalitäten; die Selbsteinschätzungsanteile sind subjektiv; Vergleichbarkeit hängt an der Etikettierungsdisziplin. Das Framework erhöht zudem anfangs den Prozessaufwand (Preflight, Berichte, Vermerke) – der Pilot prüft ausdrücklich auch, ob dieser Aufwand im Verhältnis zum Nutzen steht.

## 29.2 Offene Entscheidungen

Alle offenen Punkte sind zentral im Decision Log geführt. **Gezählt am 2026-09-22: 312 Decision Records von D-01 bis D-312, lückenlos; 102 Klärungspunkte von K-01 bis K-104 – zwei Nummern fehlen und sind keine Lücke: die eine ist `K-99`, eine belegte synthetische Kennung des Prüfapparats, die andere die **zusammengesetzte** Kennung der Sonde zu Prüfung 50 – sie steht ausdrücklich **nicht** in der belegten Menge, weil sie gemeldet werden **soll**, und sie darf deshalb nirgends im Kern ausgeschrieben stehen, auch hier nicht; dazu fünf Annahmen A-01 bis A-05.** *(Diese Zeile ist eine **datierte** Angabe und wandert nicht mit – eine datierte Zahl veraltet nicht, eine Zahl in der Gegenwartsform schon, D-318. Bis 0.89.0 stand hier „308", „101" und „K-103", und alle drei waren für ihr eigenes Datum bereits falsch.)* Kein Record steht mehr auf `entschieden (Vorschlag)` – das ist Kriterium 4 der 1.0.0-Definition, erfüllt seit Release 0.49.0. **Die Vollständigkeit beider Register ist maschinell gedeckt:** Prüfung 50 und 58 verlangen, dass jede im Kern genannte Kennung `K-NN` beziehungsweise `D-NN` hier als Zeile steht – zweimal hat gefehlt, was anderswo längst zitiert wurde. Die entscheidungsreife Kurzliste für ein aufnehmendes Projekt steht im Abschlussteil dieses Dokuments („Offene Entscheidungen"). Das vollständige Register:

{{EMBED-RAW:.koolie/core/governance/DECISION_LOG.md:1}}
