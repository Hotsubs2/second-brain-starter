# Rules for any AI working here

This repository is the owner's Obsidian vault and the home of the rules for every repository the owner keeps. Any AI may work here. Codex, Cursor, Copilot, and most tools read this file directly; Claude reads `CLAUDE.md`, which imports it; Cursor also reads `.cursor/rules/`. No tool is chosen, and two may work on the same day on different branches.

Who the owner is, and what is off limits, is in `Profile.md`. Read it first, every time.

## The seven rules (they apply in every repository)

1. **GitHub is the record.** Branches, commits, and pull requests are the truth. Chat memory is not.
2. **Read before you act.** Read this file, `README.md`, and the open pull requests. For who the owner is and what is off limits, read `Profile.md`, `Home.md`, and `AI Context.md` in the owner's vault repository (its name is in this repository's README).
3. **Work on a branch, never on `main`.** Name it `ai/<short-slug>`. Open a pull request with a **Plain English** section first. Never merge; the owner merges.
4. **Nothing secret, nothing private about other people.** No passwords, keys, tokens, other people's private details, client records, or raw documents. The owner's own list is in `Profile.md`. A private repository still copies everything to GitHub's servers.
5. **Small changes, honest reports.** Say what you checked and what you did not. Never force-push, rewrite history, delete branches, or change repository settings unless the owner says so in that session.
6. **Leave the next step in the pull request** before stopping: done, not done, what comes next, and who does it.
7. **Stop and ask** when something is unclear, cannot be undone, or two instructions conflict.

For work longer than an afternoon, write a GitHub issue first (title = the outcome; "done when" = things the owner can see) and name the branch `ai/<issue-number>-<slug>`.

## This vault

- Every note has `type:` in its frontmatter: `daily`, `weekly`, `project`, `note`, `index`, or `profile`. `Projects.md` lists every `type: project` note automatically; there is no Projects folder.
- New notes come from `Templates/`. Do not edit a template to change one note. `{{date}}`, `{{time}}`, and `{{title}}` inside templates belong to Obsidian; leave them exactly as written.
- `Daily/` and `Weekly/` hold dated notes. Do not rename them.
- Link with `[[wikilinks]]`. Append to `## Decisions` and `## Log` sections; never rewrite what is already there.
- `AI Context.md` is derived. Refresh it from the source notes (the weekly-review prompt does this). Do not edit its facts directly.
- `private/` is ignored by Git. Never move its contents into a tracked note.
- Obsidian on the owner's computer commits and pushes to `main` automatically. That is the owner writing. An AI still works on a branch. Before opening a pull request, pull `main`; if a note in the branch also changed on `main`, keep both versions and stop.
- To create a new repository, follow `System/New Project Recipe.md` and copy `System/repo-template/`.
