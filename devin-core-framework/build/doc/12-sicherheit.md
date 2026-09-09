# 12 Sicherheitsmodell

Das Sicherheitsmodell benennt Schutzziele und zehn konkrete Bedrohungen des KI-gestützten Arbeitens (vom Kontextabfluss über Prompt Injection und Supply-Chain-Risiken bis zur Umgehung von Quality Gates) und stellt ihnen vier Kontrollschichten entgegen: organisationsweite Einstellungen, versionierte Repository-Konfiguration (Berechtigungspolitik mit `deny`-Vorrang, Hooks), Sitzungsdisziplin und menschliche Prüfebene. Kein Einzelmechanismus trägt allein. Das Modul FW-CORE-03 wird hier vollständig wiedergegeben; die konkrete Berechtigungsvorlage steht in Kapitel 15 (Datei `.devin/config.json`), die Prüfroutinen in den Kapiteln 22 (FW-CL-06) und 26 (Testklassen PI, DS, ZA).

{{EMBED-RAW:devin-core-framework/framework/core/03-security.md:1}}
