# Änderungsantrag `CR-2026-003`

| Feld | Inhalt |
|---|---|
| Titel | Wurzelartefakte je Client Pack; Schalter `--client` in `install.py` |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | verschoben: `devin-core-framework/root-template/` → `devin-core-framework/clients/devin-desktop/root-template/`; verschoben: `devin-core-framework/framework/client-packs/` → `devin-core-framework/clients/`; geändert: `devin-core-framework/install.py`, `README.md`, `devin-core-framework/docs/ADOPTION_GUIDE.md`, `devin-core-framework/OWNERS.md` |
| Ebene laut Entscheidungsbaum 6 | Core (Struktur) |
| Art | Änderung |
| Dringlichkeit | regulär (Review-Zyklus) |

## 1. Anlass und Problem

`CR-2026-002` hat die Client Packs als Abbildungsschicht eingeführt, die Wurzelartefakte aber dort belassen, wo sie lagen: in `devin-core-framework/root-template/`. Damit blieb die Schicht Dokumentation ohne Wirkung – `install.py` kannte weiterhin genau eine, fest verdrahtete Vorlage. Ein zweites Client Pack hätte seine Artefakte nirgends unterbringen können.

## 2. Vorgeschlagene Änderung

1. **`root-template/` wandert unter das Client Pack**, dem es gehört: `devin-core-framework/clients/devin-desktop/root-template/`. Ein Client Pack besteht damit aus `CLIENT_PACK.md` (was der Client durchsetzt) und `root-template/` (was installiert wird).

2. **`install.py` erhält `--client`** (Standard `devin-desktop`) und `--list-clients`. Die Vorlage wird nicht mehr aus einer Konstanten abgeleitet, sondern aus dem gewählten Pack; `core_relpaths`, `seed_relpaths` und `run` nehmen sie als Parameter entgegen. Ein unbekannter Client bricht mit Exit-Code 1 ab und nennt die verfügbaren. Als installierbar gilt nur ein Pack mit vorhandenem `root-template/`.

3. **Die Schicht wandert von `framework/client-packs/` nach `clients/`.** Zwei Gründe, siehe Abschnitt 2a.

### 2a. Warum `clients/` und nicht `framework/client-packs/`

**Inhaltlich:** Unter `framework/` liegen die Regelebenen – `core/` (Ebene 3), `tech-packs/` (5), `role-packs/` (6), `org-policies/` (2). `CR-2026-002` hat aber normativ festgehalten, dass ein Client Pack **keine** Regelebene ist. Es dort einzuordnen war eine Analogie zu den anderen Packs und widersprach der eigenen Festlegung.

**Technisch, und hier lag ein realer Fehlschlag:** Die erste Testinstallation nach der Verschiebung brach unter Windows mit `FileNotFoundError` ab. Ursache war nicht die Logik, sondern die Pfadlänge. `MAX_PATH` beträgt 260 Zeichen; der längste relative Pfad des Frameworks wuchs durch die Verschiebung von 89 auf 126 Zeichen:

| Ablage | Längster relativer Pfad |
|---|---|
| vorher (`root-template/`) | 89 Zeichen |
| `framework/client-packs/<client>/root-template/` | 126 Zeichen |
| `clients/<client>/root-template/` | 111 Zeichen |

Bei einem Projektbasispfad von 135 Zeichen ergab die mittlere Variante 261 Zeichen und damit den Abbruch. Die Kürzung um 15 Zeichen löst den konkreten Fall; sie beseitigt das Problem nicht grundsätzlich. Ein Client Pack bleibt eine Verschachtelungsebene mehr als zuvor.

## 3. Prüffragen (durch Owner auszufüllen)

- [x] Richtige Ebene nach Entscheidungsbaum 6? — Ja, Struktur des Kerns.
- [x] Verschärfungsprinzip eingehalten? — Ja. Kein Regeltext geändert; die installierten Artefakte sind byteweise dieselben.
- [x] Widerspruchsfreiheit geprüft? — `clients/README.md` Abschnitt 2 hält fest, dass ein Client Pack keine Regelebene ist; die Ablage außerhalb von `framework/` zieht das nun nach.
- [x] Laufzeitfassungen betroffen? — Inhaltlich nein, nur ihr Quellort. Nachgewiesen durch eine Erstinstallation mit unveränderter Dateizahl (80).
- [x] Belegstatus korrekt? — Keine produktbezogene Aussage betroffen.
- [x] Test- und Validierungsbedarf? — Siehe Abschnitt 5. `FW-KO-04` hat die beiden gebrochenen Querverweise unmittelbar nach der Verschiebung gemeldet, ohne die historischen Nennungen in `CHANGELOG.md` fälschlich mitzumelden.
- [x] Auswirkungen auf Overlays und laufende Onboardings? — Für aufnehmende Projekte keine: `install.py` wird ohne Schalter aufgerufen und verhält sich unverändert. Betroffen ist nur, wer den Kern selbst bearbeitet.
- [x] Dokumentation? — `README.md` (Verzeichnisbaum, Abschnitt „Arbeiten an diesem Repository"), `ADOPTION_GUIDE.md` (Abschnitt „Werkzeugwechsel" von Zukunftsplan auf Ist-Zustand umgeschrieben), CHANGELOG, Decision Log.

## 4. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | angenommen |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Ohne diesen Schritt bliebe `CR-2026-002` folgenlos. Die Ablage unter `clients/` ist zugleich inhaltlich konsistenter und technisch robuster als die zunächst gewählte unter `framework/`. |
| Ziel-Release | 0.5.0 |
| Decision-Log-Eintrag | D-13 |

## 5. Umsetzung (nach Annahme)

- [x] Verschiebung beider Verzeichnisse; alle Verweise nachgezogen
- [x] `install.py`: `--client`, `--list-clients`, parametrisierte Vorlage
- [x] Validator ohne Fehler und Warnungen
- [x] Erstinstallation in leerem Verzeichnis: **80 Dateien**, kein Pack aktiv, `.devin/skills/` nur `fw-*` – identisch zum Stand vor der Verschiebung
- [x] `--check` gegen die frische Installation: keine Abweichung
- [x] Drift-Erkennung: manipulierte Core-Datei → Exit 1 mit Nennung des Client-Pack-Pfades; `--update` stellt her → Exit 0
- [x] Unbekannter Client: Exit 1, verfügbare Packs genannt
- [x] CHANGELOG und Decision Log ergänzt
- [ ] Folgearbeit: zweites Client Pack; Umbenennung der devin-spezifischen Verzeichnis- und Markernamen
