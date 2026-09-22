---
type: index
---

# How This Works

## Three layers, and you

| Layer | What it is | What it holds |
| --- | --- | --- |
| GitHub | The record | Every repository, branch, and pull request. Your notes too, because this vault is a repository. |
| Obsidian | The notebook | Daily notes, projects, whatever you write. It saves to GitHub by itself. |
| Any AI | The worker | Reads the rules, works on a branch, hands back a change for you to approve. Which AI does not matter. |

You are the fourth layer: the only one who merges.

## The loop

1. You ask an AI for something, in your words.
2. It works on a **branch**: a copy of the repository where nothing it does touches the real thing.
3. It opens a **pull request**: "here is the change, here is what it means in plain English."
4. You read the plain English. If it is confusing, ask the AI to explain the pull request.
5. You click **merge**. Now `main` has it. Until you click, nothing has changed.

`main` is the real thing. An AI never writes to it. That one rule is what makes it safe to let an AI work while you sleep.

## Git in plain English

| Word | Meaning |
| --- | --- |
| Commit | A saved snapshot, with a one-line note. Obsidian makes one every ten minutes. |
| Push | Send snapshots to GitHub. Obsidian does this by itself. |
| Pull | Bring down what changed on GitHub, like a merged pull request. Obsidian does this when it opens and every ten minutes. |
| Branch | A parallel copy for work in progress. `main` is the one that counts. |
| Pull request | A branch asking to become part of `main`, with a description. You approve it by merging. |
| Merge | Accept a pull request. Squash-and-merge keeps `main` tidy: one snapshot per change. |
| Conflict | The same line changed in two places. Obsidian shows both versions. Keep both, then ask an AI to help sort it. Never pick a side blindly. |

## Where things live on your computer

```text
~/Projects/
  AGENTS.md                            rules for an AI that starts here (copy from System/projects-folder)
  <Your Name>/
    <name>-second-brain/               this vault
  Some Project/
    Some-Project-Website/              a project repository
```

One folder per project, one repository per folder inside it. `Projects` and the project folders are plain folders, never repositories.

## Privacy, in one table

| What | Where |
| --- | --- |
| A thought, a plan, a project note, a person's name and what they care about | This vault |
| Something private about another person, or about money, health, or legal matters | `private/`, which never leaves this computer, or not written |
| A password, key, token, recovery code | A password manager. Never a file. |
| A client, customer, patient, or student record | The system built for it. Never here. |
| A raw document or export | Its original home. Write a one-line pointer here. |

A private repository is not a private place. GitHub keeps copies. When unsure, keep it out.

If a secret slips in: change the password or revoke the key first. That is the fix. Then tell an AI which file. Deleting the file does not remove it from history; only you decide about rewriting history, and only after the secret is dead.

## Recovery

- Deleted a note? It is in Git history. Ask an AI: "restore `Daily/2026-09-22.md` from history, on a branch."
- Broke a template? Ask: "show me the previous version of `Templates/Daily.md`."
- Obsidian says conflict? Keep both versions, save, and ask for help sorting it.

## Growing it

Everything below is one pull request away. Ask an AI in plain words.

- A new kind of note (people, meetings, decisions): "add a People template like the Project one, and a People page like Projects."
- A second computer: clone the vault there, open it, install the two plugins. Same settings travel with it.
- The phone: a separate decision with its own trade-offs. Ask Hogan first.
- Many repositories: when the rules and the repo template outgrow this vault, they can move to their own repository. One pull request.
