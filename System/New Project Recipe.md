---
type: index
---

# New Project Recipe

How a new repository is made, every time, so they all look the same. An AI follows this; you do the steps marked **you**.

## 1. Names

| Name | Rule | Example |
| --- | --- | --- |
| Project folder | Title Case with spaces. One folder per project. | `Garden Shop` |
| Repository | `Project-Name-Purpose`, Title-Case-With-Hyphens. | `Garden-Shop-Website` |

## 2. Create the repository on GitHub (**you**)

New repository → your account → **Private** → **Add a README** → Create. Nothing else. Creating, deleting, or making a repository public is always your own separate step, never part of another task.

## 3. Clone it (**you**, or the AI if it has a local checkout)

Into `~/Projects/<Project Folder>/<Repo-Name>/`.

## 4. Bootstrap pull request (the AI)

On a branch `ai/bootstrap` from `main`:

1. Copy every file from this vault's `System/repo-template/` into the new repository at the same relative path. Replace the placeholder README.
2. Fill in `<Repo-Name>`, `<one-sentence purpose>`, `<Project Folder>`, and `<owner/vault-repo>` (this vault's GitHub name, from `Profile.md`). Leave no angle-bracket placeholder behind.
3. Add the folders the work needs, each with an empty `.gitkeep`: `src/` and `tests/` for software; `content/` and `drafts/` for writing; `sources/` and `notes/` for research. `sources/` holds a list with titles and links, never copyrighted text or private documents.
4. Write the README's "What this is" and "How to use it" from the purpose. "Nothing runs yet." is a fine answer.
5. Commit `Bootstrap <Repo-Name>`. Open a pull request to `main`, body from the template. Do not merge.

The starter tree:

```text
<Repo-Name>/
  README.md                          what, why, how to use, where things live, where the owner's vault is
  AGENTS.md                          the seven rules plus anything specific to this repository
  CLAUDE.md                          @AGENTS.md
  .cursor/rules/rules.mdc            the same rules, for Cursor
  .github/pull_request_template.md   Plain English first
  .gitignore
  docs/
```

## 5. Give it a note in the vault (**you**, thirty seconds)

New note, name it after the project folder, then Cmd+P (Ctrl+P on Windows) → **Templates: Insert template** → **Project**. Set `repos:` to the repository's GitHub name, write one line under "What this is". It appears on [[Projects]] by itself.

## Branches, in every repository

- `main`: the real thing. Merges only. Nobody types on it.
- `ai/<slug>`: an AI's working branch. One per task. Deleted after merge.
- `me/<slug>`: your own working branch, if you ever want one.

## Done when

- [ ] The bootstrap pull request is open, with no placeholder left in any file.
- [ ] The project note exists and shows on [[Projects]].
- [ ] Nothing was merged by the AI.
