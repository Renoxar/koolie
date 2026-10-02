# Quickstart – try Koolie in ten minutes

*Deutsche Fassung: [QUICKSTART.md](QUICKSTART.md). The German version is authoritative; all further
documentation is in German and marked (German).*

This quickstart installs Koolie into an **empty practice repository** and shows what is created. It does not
start an AI client and does not change any existing project. The client pack `claude-code` serves as the
example; the other packs work the same way.

For an **existing** project, read the [adoption guide](.koolie/core/docs/ADOPTION_GUIDE.md) (German)
afterwards. If you are new to a project that already uses Koolie, start with the
[onboarding quick start](.koolie/core/onboarding/QUICKSTART.md) (German).

## Prerequisites

- **Git** and **Python 3.8 or later**, no additional packages. If Python is called `python3` on your system,
  use that instead of `python` in all commands.
- A command line with a POSIX shell, on Windows for example Git Bash.
- Koolie itself, in one of two ways:
  - **from a package source:** `uvx koolie` (or `pipx run koolie`, `npx @renoxar/koolie`). It replaces
    `python .koolie/core/install.py` in steps 2 and 3, and you can start from any directory. If you used
    `pip install koolie` and `koolie` is not found, run `python -m koolie`.
  - **from the unpacked release archive or a clone:** steps 1 to 4 then run from its root directory. Instead
    of step 2 you can also use the starters `install.cmd` (Windows) and `install.command` (macOS); they ask
    for the same information.

All output of the installer and the validator is in German; this guide quotes the lines you need.

## Step 1: Create a practice repository

```bash
mkdir ../koolie-uebung
git -C ../koolie-uebung init
echo "# Practice project" > ../koolie-uebung/README.md
git -C ../koolie-uebung add README.md
git -C ../koolie-uebung commit -m "Start"
```

## Step 2: Install Koolie

```bash
python .koolie/core/install.py --target ../koolie-uebung --client claude-code
```

From a package source: `uvx koolie --target ../koolie-uebung --client claude-code`. Without arguments,
`uvx koolie` opens a dialog with the current directory as the default.

The installer copies the core (`.koolie/core/`) into the practice repository, creates the files the client
needs and lists the next steps for a real project at the end.

⚠️ On Windows, no path may exceed 259 characters. If the practice repository is nested too deeply, the
installer stops before the first copy. Choose a shorter location, in Git Bash for example `/c/koolie-uebung`,
and use it instead of `../koolie-uebung` in all commands.

## Step 3: Choose a different client (optional)

```bash
python .koolie/core/install.py --list-clients
```

shows the available client packs. What each client enforces technically is summarised in the
[overview of the client packs](.koolie/core/clients/README.md) (German), section 6; which files a pack creates
is listed in the [runtime glossary](.koolie/core/docs/RUNTIME_GLOSSARY.md) (German). For this quickstart,
`claude-code` is enough.

## Step 4: Look at what was created

| Path in the practice repository | What it is |
|---|---|
| `CLAUDE.md` | the **instruction file** the client loads at start – with Koolie's rules, for example *"Never: `git push` …"* (in German) |
| `.claude/settings.json` | the **permission file**: what the client blocks (`deny`), asks about (`ask`) or may do without asking (`allow`), plus the hooks |
| `.claude/rules/`, `.claude/skills/`, `.claude/agents/` | short versions of the rules, the skills (`/koolie-plan` and others) and a read-only review profile |
| `.koolie/core/` | the **core** – identical in every project, never edit by hand |
| `.koolie/project-overlay/` | the **project overlay** – the project configuration the team fills in |

The block on `git push` from the [README](README.en.md#what-is-enforced--and-what-is-not) is in the
permission file:

```bash
grep -n "git push" ../koolie-uebung/.claude/settings.json
```

`Bash(git push:*)` appears twice: in `permissions.deny`, where the client reads the block, and in
`_core_rules_integrity.deny_must_contain`, which the validator checks the file against.

## Step 5: Commit and check

```bash
echo "__pycache__/" > ../koolie-uebung/.gitignore
git -C ../koolie-uebung add -A
git -C ../koolie-uebung commit -m "Koolie installed"
cd ../koolie-uebung
python .koolie/core/tests/scripts/validate-framework.py
```

**Expected:** `Ergebnis: 0 Fehler, 0 Warnungen` (result: 0 errors, 0 warnings). Among other things, the
validator checks that the core rules of the permission file are complete. The `.gitignore` keeps the tools'
Python bytecode out of the repository; without it you get a warning.

## Step 6: See what is missing for real use

```bash
python .koolie/core/tests/scripts/validate-framework.py --check-overlay-ready
```

**Expected:** several `FEHLER` (error) lines with `enthält offene <TBD>-Werte` (contains open `<TBD>` values)
for files under `.koolie/project-overlay/` and for the overlay rule in `.claude/rules/`. That is correct: the
overlay is still empty. Until it is filled in, reviewed and active, the agent works read-only in the project.
Which values a project enters and who approves them is described in the
[adoption guide](.koolie/core/docs/ADOPTION_GUIDE.md) (German).

## Step 7: Run the client against it (optional)

With Claude Code installed, you can start a session in the practice repository and ask the assistant to push
a commit. **Expected:** it declines; if it tries anyway, the client rejects the call. This was measured with
Claude Code 2.1.274 ([protocol](.koolie/core/tests/protocols/2026-09-17-sitzungstest-schranken.md), German)
and has not been re-checked for this quickstart. A model can behave differently – that is exactly what the
technical block is for.

## Clean up

The practice repository `../koolie-uebung` can be deleted afterwards.

## Next steps

- [README](README.en.md): what Koolie is, who it is for and which clients it supports.
- [Adoption guide](.koolie/core/docs/ADOPTION_GUIDE.md) (German): taking Koolie into an existing project, updates, costs, deployment architecture and coexistence with another agent framework.
- [Overview of the client packs](.koolie/core/clients/README.md) (German): capability matrices and their evidence.
