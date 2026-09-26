# Quickstart – try Koolie in ten minutes

*Deutsche Fassung: [QUICKSTART.md](QUICKSTART.md). The German version is authoritative; all further
documentation is in German and marked (German).*

This quickstart installs Koolie into an **empty practice repository** and shows what is created. It does not
start an AI client and does not change any existing project. The client pack `claude-code` serves as the
example; every other pack works the same way (step 3).

To adopt Koolie in an **existing** project, read the [adoption guide](.koolie/core/docs/ADOPTION_GUIDE.md)
(German) afterwards. For the first working day in a project that already uses Koolie, start with the
[onboarding quick start](.koolie/core/onboarding/QUICKSTART.md) (German).

## Prerequisites

- **Git** and **Python 3.8 or later** (no additional packages). If Python is called `python3` on your system,
  use that instead of `python` in all commands below.
- A command line with a POSIX shell – on Windows, for example, Git Bash. Step 2 can also be done with the
  starters `install.cmd` (Windows) or `install.command` (macOS) in the root of the release archive; they ask
  for the same information. The other steps need the command line.
- Koolie itself: the **unpacked release archive** or a **clone** of this repository. Steps 1 to 4 run from its
  root directory, steps 5 and 6 inside the practice repository.

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

`--target` copies only the core (`.koolie/core/`) into the practice repository and creates the files the
client needs there. At the end, the installer lists the next steps for a real project. Its messages are in
German.

⚠️ On Windows, no copied path may exceed 259 characters. If the practice repository is nested too deeply, the
installer stops before the first copy and states how many characters are too many. In that case, choose a
shorter location and replace `../koolie-uebung` with it in all commands – in Git Bash, for example,
`/c/koolie-uebung`.

## Step 3: Choose a different client (optional)

```bash
python .koolie/core/install.py --list-clients
```

shows the available client packs. What each client enforces technically is recorded in its **capability
matrix**; the [overview of the client packs](.koolie/core/clients/README.md) (German), section 6, summarises
them. The file names in step 4 apply to `claude-code`; which files another pack creates is listed in the
[runtime glossary](.koolie/core/docs/RUNTIME_GLOSSARY.md) (German). For this quickstart, `claude-code` is enough.

## Step 4: Look at what was created

| Path in the practice repository | What it is |
|---|---|
| `CLAUDE.md` | the **instruction file** the client loads at start – with the framework's rules, for example *"Never: `git push` …"* (in German) |
| `.claude/settings.json` | the **permission file**: what the client blocks technically (`deny`), asks about (`ask`) or may do without asking (`allow`), plus the hooks |
| `.claude/rules/`, `.claude/skills/`, `.claude/agents/` | short versions of the rules, the framework's skills and a read-only review profile |
| `.koolie/core/` | the **core** – identical in every project, never edit by hand |
| `.koolie/project-overlay/` | the **project overlay** – the project configuration the team fills in |

The block from the example in the [README](README.en.md#what-does-it-look-like-in-practice) is in
`.claude/settings.json`:

```bash
grep -n "git push" ../koolie-uebung/.claude/settings.json
```

The output shows `Bash(git push:*)` twice: in `permissions.deny`, where the client reads the block, and in
`_core_rules_integrity.deny_must_contain`, the list of core rules the validator checks the file against.

## Step 5: Commit and check

```bash
echo "__pycache__/" > ../koolie-uebung/.gitignore
git -C ../koolie-uebung add -A
git -C ../koolie-uebung commit -m "Koolie installed"
cd ../koolie-uebung
python .koolie/core/tests/scripts/validate-framework.py
```

**Expected:** `Ergebnis: 0 Fehler, 0 Warnungen` (result: 0 errors, 0 warnings). Among other things, the
validator checks that the core rules of the permission file are complete. The `.gitignore` entry is needed
because the core's tools create Python bytecode on every run; without it, the validator reports a warning.

## Step 6: See what is missing for real use

```bash
python .koolie/core/tests/scripts/validate-framework.py --check-overlay-ready
```

**Expected:** several lines containing `FEHLER` (error) and `enthält offene <TBD>-Werte` (contains open
`<TBD>` values) for files under `.koolie/project-overlay/` and for the overlay rule in `.claude/rules/`. That is
correct: the overlay has not been filled in yet. Until it has been filled in, reviewed and set to active, the
agent works read-only in the project. Which
values a project has to enter and who approves them is described in the
[adoption guide](.koolie/core/docs/ADOPTION_GUIDE.md) (German).

## Step 7: Run the client against it (optional)

If you have Claude Code installed, you can start a session in the practice repository and ask the assistant
to push a commit. **Expected** (this is what was measured): the assistant declines; if it tries anyway, the
client rejects the call. This has **not been re-checked** for this quickstart – it was measured on 2026-09-17
with Claude Code 2.1.274 ([protocol](.koolie/core/tests/protocols/2026-09-17-sitzungstest-schranken.md),
German). A model can behave differently – that is why the technical block exists, and why the capability
matrix names its limit.

## Clean up

The practice repository can be deleted afterwards – seen from the directory where you ran step 1, it is
`../koolie-uebung`.

## Next steps

- [README](README.en.md): what Koolie is, who it is for, which clients are supported and how far.
- [Adoption guide](.koolie/core/docs/ADOPTION_GUIDE.md) (German): taking Koolie into an existing project, updates, costs.
- [Overview of the client packs](.koolie/core/clients/README.md) (German): capability matrices and their evidence.
