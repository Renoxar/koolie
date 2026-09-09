# Overlay-Dokumentenverzeichnis

Ablage für projektspezifische Dokumente oder bereinigte Auszüge, die Devin als Kontext erhalten darf. Jedes Dokument MUSS in `../overlay-manifest.yaml` registriert sein; nicht registrierte Dokumente gelten als K3 und werden nicht verwendet.

## Verzeichnisstruktur (ein Unterverzeichnis je Dokumenttyp)

```text
documents/
├── ai-governance/
├── ai-process-model/
├── roadmap/
├── architecture/
├── coding-guidelines/
├── definition-of-ready/
├── definition-of-done/
├── branching-strategy/
├── deployment/
├── security/
├── quality/
├── roles/
└── glossary/
```

## Regeln

1. Vor der Ablage prüft die Overlay-Ownerin oder der Overlay-Owner das Dokument anhand `devin-core-framework/checklists/02-privacy-context.md`. Bereinigungen werden im Manifest dokumentiert.
2. Bleibt das Original außerhalb des Repositorys, wird ein Verweisblatt `REFERENCE.md` abgelegt (Titel, Zweck, Ablageort als Platzhalter `<DOCUMENTATION_PLATFORM>`, Kontextklasse, Freigabe). Devin kann Verweisblätter lesen, das Original nicht.
3. Dokumente enthalten keine Personen, Kunden, Behörden, internen Adressen, Umgebungskennungen oder Secrets.
4. Änderungen erhöhen die Overlay-Version (Abschnitt 20 des Overlays).

## Vorlage Verweisblatt

```markdown
# Verweisblatt – <Dokumenttitel>

- Typ: <Manifest-Typ>
- Zweck: <ein Satz>
- Ablageort: <DOCUMENTATION_PLATFORM>, Bereich <TBD>
- Kontextklasse des Originals: <K1 | K2 | K3>
- Für Devin nutzbarer Auszug: <Pfad im Dokumentenverzeichnis oder „keiner">
- Freigabe: <Rolle>, <Datum>
```
