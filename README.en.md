# Koolie

**Governance for AI coding assistants – one rule source for every client, enforced technically wherever the client allows it.**

[![PyPI](https://img.shields.io/pypi/v/koolie)](https://pypi.org/project/koolie/)
[![npm](https://img.shields.io/npm/v/@renoxar/koolie)](https://www.npmjs.com/package/@renoxar/koolie)
[![License: GPL-3.0](https://img.shields.io/badge/license-GPL--3.0-blue)](LICENSE)

*Deutsch: [README.md](README.md). The German documentation is authoritative; further documents are in German.*

A team working with AI coding assistants needs more than an instruction file: shared rules for every
assistant, technical blocks wherever a rule must not be broken, and clear points where a human decides.
Koolie brings exactly that into an existing Git repository – and states openly, for each client, which rule
it really enforces and which only acts as an instruction.

## Quick start

In your project directory:

```bash
uvx koolie                  # or: pipx run koolie · npx @renoxar/koolie
```

The command fetches Koolie, offers the current directory as the project and asks for your AI client.
Afterwards the project holds the instruction file, the permissions and a guard hook for that client. Without
a package registry, use the release archive and the starters `install.cmd` / `install.command`.

**Want to try it first?** The [quickstart](QUICKSTART.en.md) installs Koolie into an empty practice repository
– in ten minutes, without starting an AI client.

## How it works

```text
  Core  .koolie/core/            Project overlay  .koolie/project-overlay/
  rules, skills, checklists,     paths, approval routes, project documents
  guard hook, validator          – owned by the project
            │                               │
            └───────────────┬───────────────┘
                            ▼
                Client pack per AI client
       instruction file · permissions · hooks · skills
       (e.g. CLAUDE.md and .claude/ for Claude Code)
```

- **One core for all clients.** Rules and skills are written once, tool-neutral; a team with mixed tools shares
  the same rules.
- **The project stays in charge.** Project values live in the overlay. A new release updates a project with the
  same command: it detects the existing core and offers to update it; the overlay is never touched.
- **Control levels instead of trust.** The assistant handles small tasks on its own; from "medium" it needs a
  confirmed plan, at "high" an explicit approval.

## What is enforced – and what is not

| Kind of rule | What it means | Example |
|---|---|---|
| **Technical** | The client enforces it, whatever the model does | `git push` is blocked; secret files cannot be read |
| **Instruction** | The rule is in the model's context; it can follow it | "Do not change files outside the approved scope" |
| **Human** | Approvals, reviews, decisions | A person approves a release |

Each client pack keeps a **capability matrix** that assigns every promise to one of these kinds – backed by a
measurement on the client. Koolie complements a good standard setup (branch protection, CI, managed settings);
it does not replace it.

## Supported clients

| Client | Pack | Status |
|---|---|---|
| Claude Code | [`claude-code`](.koolie/core/clients/claude-code/CLIENT_PACK.md) | pilot |
| Cursor | [`cursor`](.koolie/core/clients/cursor/CLIENT_PACK.md) | pilot |
| Devin Desktop | [`devin-desktop`](.koolie/core/clients/devin-desktop/CLIENT_PACK.md) | pilot |
| Kiro | [`kiro`](.koolie/core/clients/kiro/CLIENT_PACK.md) | pilot |
| OpenAI Codex CLI | [`openai-codex`](.koolie/core/clients/openai-codex/CLIENT_PACK.md) | pilot, only with approval by the security officer |

*Pilot* means: fully built, measured on real installations, meant for accompanied use. The limits of each
client are listed in its pack (German).

## Who is it for?

- **Development teams** that use AI assistants every day and want shared, verifiable rules.
- **Technical leads** – team leads, architecture, security, data protection – who must show what a tool
  enforces technically.

Koolie is not meant for running an agent fully autonomously without human approvals.

## Documentation

| Topic | Where |
|---|---|
| Try it in ten minutes | [`QUICKSTART.en.md`](QUICKSTART.en.md) |
| Adopt in a project, update, costs | [Adoption guide](.koolie/core/docs/ADOPTION_GUIDE.md) (German) |
| First day in a project that uses Koolie | [Onboarding](.koolie/core/onboarding/QUICKSTART.md) (German) |
| Client packs and capability matrices | [`clients/README.md`](.koolie/core/clients/README.md) (German) |
| The rules themselves | [`framework/core/`](.koolie/core/framework/core/) (German) |
| Changes and plans | [`CHANGELOG.md`](.koolie/core/CHANGELOG.md) · [`ROADMAP.md`](.koolie/core/docs/ROADMAP.md) (German) |
| Contributing to the framework | [`CONTRIBUTING.md`](CONTRIBUTING.md) (German) |

## Why "Koolie"?

A Koolie is an Australian herding dog. It does not drive the herd and does not replace the shepherd – it keeps
the flock together, on course and within bounds. That is what this framework is meant to do with an AI
assistant.

## License

[GPL-3.0](LICENSE) with an additional permission: files created from the templates and any output of the tools
belong to the project that creates them. Merely using Koolie – also commercially – puts no obligations on you;
the details are in [`LICENSE-HINWEIS.md`](.koolie/core/LICENSE-HINWEIS.md) (German).
Copyright © 2026 `<FRAMEWORK_OWNER>`.
