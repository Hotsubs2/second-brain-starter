# Rules for any AI working in <Repo-Name>

<one-sentence purpose>

- Owner's vault (read `Profile.md` there first): `<owner/vault-repo>`
- Checks to run before opening a pull request: none yet.
- Files not to change without the owner saying so: none yet.

## The seven rules

<!-- copied from the owner's vault → AGENTS.md; change them there first -->

1. **GitHub is the record.** Branches, commits, and pull requests are the truth. Chat memory is not.
2. **Read before you act.** Read this file, `README.md`, and the open pull requests. For who the owner is and what is off limits, read `Profile.md`, `Home.md`, and `AI Context.md` in the owner's vault repository (its name is in this repository's README).
3. **Work on a branch, never on `main`.** Name it `ai/<short-slug>`. Open a pull request with a **Plain English** section first. Never merge; the owner merges.
4. **Nothing secret, nothing private about other people.** No passwords, keys, tokens, other people's private details, client records, or raw documents. The owner's own list is in `Profile.md`. A private repository still copies everything to GitHub's servers.
5. **Small changes, honest reports.** Say what you checked and what you did not. Never force-push, rewrite history, delete branches, or change repository settings unless the owner says so in that session.
6. **Leave the next step in the pull request** before stopping: done, not done, what comes next, and who does it.
7. **Stop and ask** when something is unclear, cannot be undone, or two instructions conflict.

For work longer than an afternoon, write a GitHub issue first (title = the outcome; "done when" = things the owner can see) and name the branch `ai/<issue-number>-<slug>`.
