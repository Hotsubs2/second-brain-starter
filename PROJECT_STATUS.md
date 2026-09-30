---
type: note
---

# Project status — 2026-09-25

Snapshot of the public starter. It describes `main` as of this date. It does not change the notebook, the rules, or the plugins.

## Purpose

`itsadoor-llc/second-brain-starter` is a public GitHub template. It is an Obsidian vault that backs itself up to GitHub, and it carries the rules any AI follows when it works in a copy of that vault.

Someone looking at the template creates their own private repository from it. The copy is the notebook. This repository stays the blank starter: `Profile.md` still has the lines marked **you**.

## Tip

Default branch: `main`.

Tip: `1d8a3714503d426849f7141a991539f472a6055b` (short `1d8a3714`).

That commit is "Ship core-plugin settings: daily notes and templates on, Sync off (#2)", dated 2026-09-22. Fetched `origin/main` on 2026-09-25 and it still pointed at this commit. `PROJECT_STATUS.md` was not on `main`.

## Relationship to itsadoor second-brain

This starter's own files do not name `itsadoor-second-brain`.

In the same GitHub organization, `itsadoor-llc/itsadoor-second-brain` is a separate private repository. Its description is a shared company Markdown/Obsidian knowledge vault. Its README does not point at this starter. That vault was created on 2026-09-07. This starter was created on 2026-09-22. Neither repository is a fork of the other.

This snapshot did not copy notes, paths, or names out of the company vault.

## How someone uses it

1. On GitHub, click **Use this template → Create a new repository**. Name it `<yourfirstname>-second-brain` and make it **Private**.
2. Clone that copy into `~/Projects/<Your Name>/`. In Obsidian, open the cloned folder as a vault and click **Trust author and enable plugins**. Git and Dataview are already in the vault.
3. Fill the three **you** lines in `Profile.md`. Use the calendar icon to make today's note. Obsidian Git commits and pushes that copy.
4. Any AI reads `AGENTS.md`, works on a branch, and opens a pull request. The owner merges. An AI does not write to `main`.
5. A new project repository follows `System/New Project Recipe.md` and starts from `System/repo-template/`.

The first-time checklist is `System/Start Here.md`. The plain-English map is `System/How This Works.md`.

## Open pull requests

One open pull request on 2026-09-25. No other open pull request turned up in a search for `PROJECT_STATUS`.

- Draft [#3](https://github.com/itsadoor-llc/second-brain-starter/pull/3), "Add a live Meet onboarding guide and first-contribution workflow", branch `ai/friends-onboarding`, opened 2026-09-23. It is not merged. Its base is still this tip (`1d8a3714`). It adds a live Meet guide and a first-contribution workflow for a friend on their own computer. That guide is not on `main`.

## Workers

`AGENTS.md` is already at the repository root. It holds the seven rules and the vault rules. This snapshot left it as it is.

`CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, and `.cursor/rules/` point at that same file.

## Next

The owner reads draft [#3](https://github.com/itsadoor-llc/second-brain-starter/pull/3) and decides whether to try the Meet guide, ask for a change, or leave it unmerged. Who: owner.

## What this snapshot checked

- Local `HEAD` and fetched `origin/main` both at `1d8a3714503d426849f7141a991539f472a6055b`.
- `PROJECT_STATUS.md` was absent on that tip.
- `AGENTS.md` was present, so it was not replaced.
- Open pull requests on this repository: draft #3 only.
- Company-vault README, only to see whether it names this starter. It does not. No company-vault notes were copied here.
- Not checked: a fresh "Use this template" clone, Obsidian on a computer, or the Meet guide in draft #3.
