# Änderungsantrag `CR-2026-126`

| Feld | Inhalt |
|---|---|
| Titel | Die Lizenz: GPL-3.0 mit einer Zusatzerlaubnis nach §7 für Vorlagenergebnisse und Werkzeugausgaben |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-23 |
| Betroffene Artefakte | `LICENSE` (neu); `.koolie/core/LICENSE` (neu); `.koolie/core/LICENSE-HINWEIS.md` (neu); `.koolie/core/tests/scripts/validate-framework.py` (**Prüfung 79**); `.koolie/core/tests/scripts/probe-pruefungen.py` (Sonden 79a–c, Gegenprobe 79a); `.koolie/core/tests/TEST_CATALOG.md`; `README.md`; `.koolie/core/governance/DECISION_LOG.md` (**D-316**, **D-317**); `.koolie/core/CHANGELOG.md` |
| Ebene laut Entscheidungsbaum 6 | Core, und darüber hinaus: Die Lizenz ist eine **rechtliche** Festlegung über den gesamten Bestand |
| Art | Neuaufnahme (erste Lizenzfestlegung des Projekts) |
| Dringlichkeit | hoch, **bevor** das Repositorium öffentlich wird. Ein Repositorium ohne erkannte Lizenz gilt als *alle Rechte vorbehalten*; niemand darf es dann benutzen |

---

## 1. Anlass und Problem

Der Owner beabsichtigt, das Repositorium öffentlich verfügbar zu machen, und hat zwei
Bedingungen genannt:

1. *„Ich bin dafür, daß das durchaus ein Open-Source-Projekt ist."*
2. *„Allerdings, daß das Kernprojekt nicht von anderen zum Verkauf angeboten werden
   darf."* – Nutzung **im Entwicklungsbereich** eines kommerziellen Produkts soll
   ausdrücklich erlaubt bleiben.

🔴 **Die beiden Bedingungen schließen einander aus, und das ist kein Auslegungsspielraum.**
Die Open-Source-Definition der OSI verbietet in **§1** (*Free Redistribution*) und **§6**
(*No Discrimination Against Fields of Endeavor*) genau die Einschränkung aus Bedingung 2.
**Keine OSI-anerkannte Lizenz kann leisten, was Bedingung 2 verlangt.**

➡️ *Eine Anforderung, die zwei Bedingungen stellt, von denen die eine die andere
ausschließt, ist keine Anforderung, sondern eine Entscheidung, die noch nicht getroffen
ist.* Sie ist deshalb als Entscheidungsvorlage gestellt worden.

### 1.1 Die Rückfrage, die die Entscheidung getragen hat

Der Owner hat gefragt, ob unter Apache-2.0 *„eine Firma einfach den gesamten Kern nehmen
und unter einem anderen Namen als eigene Lösung verkaufen"* könnte. **Die Antwort ist ja**,
und sie hat die Wahl entschieden: Apache-2.0 erlaubt Umbenennen, Schließen und Verkaufen;
ihr einziger Riegel ist §6, und der schützt den **Namen**, nicht die Sache.

### 1.2 Der Weg, der beides trägt

**Die GPL-3.0 löst den Widerspruch, ohne ihn zu verbieten.** Sie ist OSI-anerkannt – also
echtes Open Source –, und der Weiterverkauf bleibt **erlaubt**. Nur bekommt jeder Käufer
den Quelltext unter derselben Lizenz mit und darf ihn weitergeben. **Damit fällt das
Geschäftsmodell *umbenennen und proprietär verkaufen* weg, ohne daß die Lizenz jemandem
etwas verbietet.**

Die Nutzung bleibt unberührt: **Die GPL bindet die Weitergabe, nicht den Gebrauch.**

### 1.3 🔴 Die eine scharfe Kante, und sie wird nicht verschwiegen

Ein ausgefülltes `.koolie/project-overlay/OVERLAY.md` entsteht aus einer mitgelieferten
Vorlage und ist damit formal eine **geänderte Fassung eines GPL-Werks**. Das beabsichtigt
niemand, und eine Rechtsabteilung hält an genau dieser Stelle zu Recht an.

**§7 GPL-3.0 erlaubt ausdrücklich zusätzliche Erlaubnisse.** Eine davon nimmt die Kante
weg, ohne die Wirkung aus 1.2 zu berühren.

---

## 2. Vorschlag

1. **GPL-3.0** als Lizenz des gesamten Bestands, wörtlicher Text der Free Software
   Foundation.
2. **Zusatzerlaubnis nach §7** für Vorlagenergebnisse und Werkzeugausgaben.
3. **Zwei Ablageorte** – Wurzel und Kern – und **Prüfung 79**, die sie gegeneinander hält.
4. **`LICENSE-HINWEIS.md`** mit der Tabelle *„was das für ein übernehmendes Projekt
   bedeutet"* und den verworfenen Alternativen.

---

## 3. Auswirkungen

| Gegenstand | Wirkung |
|---|---|
| Veröffentlichung | 🟢 möglich. Ohne Lizenz wäre das Repositorium unbenutzbar |
| Übernehmende Projekte | **keine Pflicht**, solange sie nichts weitergeben. Siehe `LICENSE-HINWEIS.md` Abschnitt 3 |
| Prüfapparat | 🟢 Prüfung 79, drei Sonden und eine Gegenprobe |
| Bestehende Installationen | keine. Die Lizenz gilt ab diesem Release; frühere Stände hatten keine |

---

## 4. Vorlage zur Entscheidung

| # | Frage | Auflösung und Preis |
|---|---|---|
| **E1** | **Welche Lizenz?** | **GPL-3.0.** Sie ist OSI-anerkannt und macht den Rebrand-Verkauf unattraktiv, ohne ihn zu verbieten. **Verworfen: Apache-2.0** – erlaubt Umbenennen, Schließen und Verkaufen ausdrücklich; Bedingung 2 wäre nicht erfüllt. **Verworfen: BUSL-1.1** – trifft Bedingung 2 wörtlich, ist aber **kein OSI-Open-Source**; der Zweck dieses Frameworks ist die Übernahme in Unternehmen, und eine Lizenz, die eine Rechtsabteilung als proprietär einstuft, kostet genau dort. ⚠️ **Preis, benannt:** pauschale GPL-Verbote in manchen Organisationen |
| **E2** | **Braucht es eine Zusatzerlaubnis?** | **Ja, nach §7.** Ohne sie wäre ein ausgefülltes Overlay formal eine geänderte Fassung eines GPL-Werks. *Verworfen: es bei der Erläuterung zu belassen* – eine Erläuterung ist keine Erlaubnis, und die Frage entsteht bei jedem übernehmenden Projekt neu |
| **E3** | **Wo liegt die Lizenzdatei?** | **An zwei Stellen, und Prüfung 79 hält sie gleich.** Die Wurzel, weil die Hostingdienste dort suchen; der Kern, weil `docs/ADOPTION_GUIDE.md` Schritt 2 ihn **als Ganzes** kopiert und die Lizenz sonst nicht mitwandert (§4 GPL-3.0). *Verworfen: nur die Wurzel plus die Anweisung „beim Übernehmen mitkopieren"* – **eine Zusage ohne Mechanismus ist der wiederkehrende Befundtyp dieses Projekts** |
| **E4** | **Wer hält das Urheberrecht?** | `<FRAMEWORK_OWNER>`. ⚠️ **Nicht entschieden und ausdrücklich offen:** ob eine Wortmarke `Koolie` gesichert wird. Die GPL schützt den Namen **nicht** – anders als Apache-2.0 §6 –, und ein Fork dürfte sich heute so nennen. *Das ist eine Markenfrage, keine Lizenzfrage, und sie gehört nicht in diesen Antrag* |

---

## 5. Abnahme

`validate-framework.py --root .` ohne Fehler (**Prüfung 79** aktiv); Sondenlauf in beiden
Kodierungsumgebungen; die Lizenzdateien byteweise gleich und als GPL-3.0 erkannt.

---

## 6. Entscheidung

**Entschieden am 2026-09-23 durch `<FRAMEWORK_OWNER>`:** E1 bis E3 wie vorgeschlagen; E4
zur Urheberschaft bestätigt, die Markenfrage bleibt ausdrücklich offen. Festgehalten als
**D-316** und **D-317**. Umgesetzt mit Release `0.90.0`.

> ⚠️ **Rechtlicher Vorbehalt, und er gehört hierher:** Dieser Antrag ist die
> **Vorbereitung** einer rechtlichen Festlegung, keine Rechtsberatung. Nach `AGENTS.md`
> Abschnitt 16 ist eine rechtliche Bewertung nicht delegierbar. Die Auswahl, die Prüfung
> der Wirkung im eigenen Verwertungsumfeld und die Verantwortung für die Veröffentlichung
> liegen bei `<FRAMEWORK_OWNER>`.
