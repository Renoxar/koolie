# Koolie

**Koolie – governance for AI coding assistants.**

*This is the English introduction. The German [README.md](README.md) is authoritative, and all further
documentation is in German; links to it are marked (German).*

Koolie gives a software development team that works with AI coding assistants a shared framework:
**shared project rules** for every assistant on the team, **human approvals** where a human has to decide,
**structured reviews** of AI-generated code, a **reusable project configuration** that a team carries from
project to project, and a **documented statement per client** of which of these rules the tool enforces
technically and which only act as instructions.

**Version:** [`.koolie/core/VERSION`](.koolie/core/VERSION) · **Changes:** [`CHANGELOG.md`](.koolie/core/CHANGELOG.md) (German) · **Status:** pilot – all modules and all client packs are at `pilot` · **Licence:** GPL-3.0 with an additional permission for generated files ([`LICENSE`](LICENSE), explanation in [`LICENSE-HINWEIS.md`](.koolie/core/LICENSE-HINWEIS.md), German)

## What is Koolie?

Koolie is a **framework of rules, templates and tools** that is installed into an existing Git repository.
It has three parts:

- the **core** (`.koolie/core/`): tool-neutral rules, checklists, skills, validation tools and the installer –
  byte-identical in every project;
- the **project overlay** (`.koolie/project-overlay/`): the exchangeable project configuration – allowed and
  blocked paths, approval routes, project documents. It belongs to the project;
- one **AI client pack** per AI client. An *AI client* is the coding assistant the team works with, for
  example Claude Code or Kiro. The client pack maps the rules of the core onto the files and mechanisms of
  that client – instruction file, permissions, hooks – and its **capability matrix** states which of them the
  client actually enforces.

Koolie replaces neither the AI client nor human review. It keeps the client within limits that can be
checked, traced and reused across projects.

## What problem does Koolie solve?

As soon as several people work on a repository with AI coding assistants, three questions arise that a single
instruction file does not answer:

1. **Do the same rules apply to everyone?** Every assistant has its own file locations and mechanisms. Without
   a shared source, the rules drift apart per tool and per person.
2. **What holds when the model does not follow the instruction?** An instruction only works as long as the
   model follows it. Where a rule must not be broken, it needs a technical block – and the team has to know
   where one exists and where it does not.
3. **Who decides?** Which tasks an assistant may complete on its own, which need a confirmed plan and which
   need an explicit approval has to be defined and visible in daily work.

Koolie answers them with one core for all clients, a classification of every rule by how it is enforced, and
fixed control levels with human approval.

## Who is Koolie for?

- **Development teams** that use AI coding assistants every day and want shared, checkable rules for them –
  including teams that use different clients.
- **Technical leads** (team lead, architecture, security, data protection) who have to show which promises a
  tool keeps technically and which are covered organisationally.
- **Projects that onboard new developers**: the framework comes with an onboarding path including exercises
  and completion criteria.

Koolie is **less suitable** for individuals who only want a personal instruction file, and for fully
autonomous agent operation without human approvals – the framework explicitly rules that out.

## What does it look like in practice?

A small, synthetic example with the client pack `claude-code`:

| Step | What happens |
|---|---|
| **Starting point** | A team wants to prevent an assistant from publishing changes on its own. `git push` is a human's job. |
| **Setup** | `install.py` creates the instruction file `CLAUDE.md` and the permission file `.claude/settings.json` in the project. |
| **The rule** | The instruction file says *"Never: `git push` …"*; the permission file lists `Bash(git push:*)` under `deny`, and the `allow` list permits only five read-only `git` commands. |
| **Expected behaviour** | The assistant declines a push. If it tries anyway, the client rejects the call. |
| **Observed behaviour** | Measured on 2026-09-17 with Claude Code 2.1.274 in non-interactive mode: with the rule text present, the assistant declined the push **without attempting it** – the technical block was never reached. Without the rule text, it called `git push origin main` and was **rejected**; likewise when `git push` was in both `allow` and `deny` – `deny` wins. |
| **The measured limit** | The pattern only matches commands that start with the string `git push`. If a project widens its `allow` list to `Bash(git:*)`, `git -C <path> push origin main` **goes through** – measured, with the commit arriving at the remote. In the shipped configuration this spelling is not allowed and was rejected in non-interactive mode; the capability matrix states the limit explicitly. |
| **Verifiable result** | The entries are in `.claude/settings.json` and can be read there; the validator checks that the core rules of the permission file are complete. Evidence: [measurement protocol](.koolie/core/tests/protocols/2026-09-17-sitzungstest-schranken.md) (German), sections 3, 5 and 6, and matrix row B6 in the [client pack `claude-code`](.koolie/core/clients/claude-code/CLIENT_PACK.md) (German). |

The [quickstart](QUICKSTART.en.md) walks through the setup of this example step by step. The client's
behaviour is not measured again there; it is taken from the protocol.

## Which AI clients are supported, and how far?

All client packs have the status **pilot**: they are fully built, measured on real installations and intended
for supervised use. What each client enforces technically is listed row by row in its capability matrix; the
overview of all packs is in [`clients/README.md`](.koolie/core/clients/README.md) (German), section 6.

| Client | Client pack | Status | Most important known limit |
|---|---|---|---|
| Claude Code | [`claude-code`](.koolie/core/clients/claude-code/CLIENT_PACK.md) | pilot | Command blocks work as prefix patterns (see the example); the file blocks – secret files protected from reading, framework, CI and lock files protected from writing – only cover direct file access; for shell and subprocesses only the instruction applies |
| Devin Desktop | [`devin-desktop`](.koolie/core/clients/devin-desktop/CLIENT_PACK.md) | pilot | In the client's `dangerous` operating mode the technical classifications do not apply; there, only the framework's protection hook blocks actions |
| Kiro | [`kiro`](.koolie/core/clients/kiro/CLIENT_PACK.md) | pilot | The blocks only work with the active agent profile; hooks only run in the interactive session; the IDE is mapped from its documentation only |
| OpenAI Codex CLI | [`openai-codex`](.koolie/core/clients/openai-codex/CLIENT_PACK.md) | pilot, **with a condition** | Two core promises cannot be mapped – **use only with approval** by the security contact; the project-local layer only loads in a project registered as trusted |
| Cursor | – | **planned** (`1.16.0`) | no client pack yet |

Which client version a pack covers and which version it was measured against is stated in the profile table
at the top of each `CLIENT_PACK.md`.

## What does Koolie add to a single AGENTS.md?

An `AGENTS.md` (or `CLAUDE.md`) is an instruction to the model. It is a good start – and Koolie installs one
itself. What it adds:

| A single instruction file | Koolie |
|---|---|
| works as long as the model follows it | additionally maps rules onto the client's **permissions and hooks**, where the client supports it |
| does not say which rule is enforced | classifies every promise as `[TECHNISCH]` (technical), `[TEXTUELL]` (instruction only) or `[NICHT ABBILDBAR]` (not mappable), with evidence |
| applies to one client | one core, mapped onto several clients; a team with mixed tools shares the same rules |
| is rewritten for every project | core unchanged, project values in the exchangeable project overlay; a new release is applied to a project with `install.py --update`, and whatever has to be added by hand is listed in the migration notes of the changelog |
| does not define responsibilities | control levels low/medium/high: a task rated medium or higher needs a plan that a human has confirmed; a task rated high also needs an explicit approval |
| is not checked | a validator checks the installation; test sheets check the behaviour of the skills on the client |

## What is enforced technically – and what stays with humans?

Koolie distinguishes three kinds of rules, and every capability matrix assigns each promise to one of them:

- **Enforced technically** (`[TECHNISCH]`): the client enforces the rule regardless of how the model behaves –
  for example a blocked file or a blocked command. This has limits too, and the matrix names them.
- **Effective as an agent instruction** (`[TEXTUELL]`): the rule is in the model's context. It can follow it;
  it is not enforced.
- **Human review required**: approvals, reviews and the delegation bans – tasks that must never be handed to
  an AI client – are not enforced by any client. They remain organisational – with checklists, control levels
  and documented exceptions.

If a client has no mechanism at all for a promise, the matrix lists it as `[NICHT ABBILDBAR]` (not mappable):
it then falls back to the instruction and to people, and a pack where this affects a core promise needs an
approval by the security contact before it is used.

**Responsibility stays with humans.** The AI client proposes; people review, accept and approve. Koolie does
not make a project secure or compliant – it makes visible **where** a rule holds technically and where a human
has to hold it.

## How do I start?

1. **Try it out:** the [quickstart](QUICKSTART.en.md) installs Koolie into an empty practice repository and
   shows what is created – in about ten minutes, without starting an AI client.
2. **Adopt it:** the [adoption guide](.koolie/core/docs/ADOPTION_GUIDE.md) (German) covers taking Koolie into
   an existing project with prerequisites, approvals and activation; the binding record is the
   [adoption checklist](.koolie/core/checklists/10-project-adoption.md) (German).
3. **Onboard:** for the first working day in a project that already uses Koolie, there is the
   [onboarding quick start](.koolie/core/onboarding/QUICKSTART.md) (German).

The installation commands are in the German README under
[„Framework in ein Projekt übernehmen“](README.md#framework-in-ein-projekt-übernehmen).

## Where can I find details and limits?

All documents below are in German.

| Topic | Document |
|---|---|
| Client packs and capability matrices | [`clients/README.md`](.koolie/core/clients/README.md) |
| Adoption, updates, several repositories, costs | [`ADOPTION_GUIDE.md`](.koolie/core/docs/ADOPTION_GUIDE.md) |
| The rules themselves (normative core) | [`framework/core/`](.koolie/core/framework/core/) |
| Data protection and security | [`02-privacy.md`](.koolie/core/framework/core/02-privacy.md), [`03-security.md`](.koolie/core/framework/core/03-security.md) |
| Control levels and delegation bans | [`09-risk-model.md`](.koolie/core/framework/core/09-risk-model.md) |
| What is planned and what remains open | [`ROADMAP.md`](.koolie/core/docs/ROADMAP.md) |
| Decisions with rationale, open questions | [`DECISION_LOG.md`](.koolie/core/governance/DECISION_LOG.md) |
| Test catalogue | [`TEST_CATALOG.md`](.koolie/core/tests/TEST_CATALOG.md) |

## Why "Koolie"?

A **Koolie** is an Australian herding dog, and the image is the job description of this framework: a herding
dog does not drive the herd and does not replace the shepherd – it keeps the herd together and heading in one
direction. It works independently, but on instruction, and it holds boundaries without biting. The decision
on the name, with its rationale and the rejected alternatives, is D-125 in
[`DECISION_LOG.md`](.koolie/core/governance/DECISION_LOG.md) (German).

## Licence

Koolie is licensed under the **GNU General Public License, version 3** ([`LICENSE`](LICENSE)), with an
additional permission under §7: files created from the supplied templates and any output of the framework's
tools are **not** covered by this licence. The GPL binds redistribution, not use. Details, in German:
[`LICENSE-HINWEIS.md`](.koolie/core/LICENSE-HINWEIS.md) and the German README, section „Lizenz“.
