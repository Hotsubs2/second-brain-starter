# Projects folder

This folder holds independent Git repositories grouped in project folders. It is not a repository itself.

- Treat each repository as its own codebase, history, and branch boundary. Run `git status --short --branch` inside it before editing.
- Keep a change inside one repository unless the task clearly needs two.
- Never run `git init` here or in a project folder. Never merge repositories into one.
- Preserve existing local changes, untracked files, and branches. Do not move, rename, or re-point repositories without explicit approval.
- Read and follow the repository's own `AGENTS.md`; the closest instructions win.
- The rules, the owner's profile, and the new-repository recipe live in the owner's vault: the one repository here that contains `Profile.md` and `System/`.
