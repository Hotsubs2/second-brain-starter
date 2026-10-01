---
type: index
---

# Prompts

For a first session or when you want the AI to identify useful work itself, use the [guided contribution prompts](../onboarding/FRIEND.md#the-prompts-you-can-come-back-to). They cover source access, one substantive contribution, review, and returning later. They authorize one session, not ongoing background work.

Copy a block, fill the `<angle brackets>`, paste into any AI. Action prompts follow the [actual owner's source merge policy](Source%20Merge%20Policy.md). A delegated conflict-free source change finishes through merge; a conflict or missing delegation requires a direct yes/no question with plain-language consequences. The explanation prompt stays read-only.

## New project (reusable, every time)

```text
You are my AI worker. Create a new project repository by following my recipe.

- My vault repository: `<your-handle>/<your>-second-brain`
- Project folder: `<Title Case, e.g. Garden Shop>`
- Repository: `<Project-Name-Purpose, e.g. Garden-Shop-Website>`
- One-sentence purpose: `<...>`
- Kind of work: `<software / writing / research / other>`

Read first, in my vault repository: `AGENTS.md`, `System/New Project Recipe.md`, and every file under `System/repo-template/`.

Then follow the recipe's step 4 exactly: branch `ai/bootstrap` from `main`, copy the starter files from `System/repo-template/`, fill in `<Repo-Name>`, `<one-sentence purpose>`, `<Project Folder>`, and `<owner/vault-repo>`, add the work folders for the kind of work, write the README's "What this is" and "How to use it", commit `Bootstrap <Repo-Name>`, open the pull request with the template body. Follow my documented source merge policy. Finish an authorized conflict-free merge after review and appropriate checks, or ask me a direct yes/no question explaining what merging and not merging would mean. Give me the real PR link and actual state.

Then remind me to do step 5 myself: the project note in Obsidian.

Stop and ask me if a file you would create already exists with different content, or if the recipe and these instructions disagree. If you cannot create a branch or a pull request, say so first and give me the files as a list with exact paths instead.
```

## Explain this pull request to me (whenever one is confusing)

```text
Explain pull request `<link or owner/repo#number>` to me. I decide whether to merge, and I do not read code for a living.

1. **What changes after merging**, in plain English, three to five sentences.
2. **What could go wrong**, and how I would notice.
3. **What I should check before merging**: the exact files or lines, and what "good" looks like there.
4. **Privacy check:** does anything in the change look like a password, key, token, other people's private details, or a raw document? Yes or no, and where.
5. **Your recommendation:** merge, ask for changes (say which), or close. One sentence of reasoning.

Do not merge, comment, or change anything. Just explain.
```

## Start a task (the everyday prompt)

```text
You are my AI worker. One task, by the rules in my repository.

- Repository: `<your-handle>/<Repo-Name>`
- The task, in my words: `<...>`

1. Read `AGENTS.md` and `README.md`, then the open pull requests. If one already covers this task or touches the same files, stop and tell me.
2. If this is more than an afternoon's work, write a GitHub issue first: title = the outcome, "done when" = things I can see, "out of scope". Tell me the number. Otherwise skip this step.
3. Branch `ai/<slug>` (or `ai/<issue>-<slug>`) from current `main`. Build the smallest version that proves the approach. Commit in small steps with messages that say what and why.
4. Check it. Run whatever checks `AGENTS.md` names; if it names none, say what you looked at by hand. Paste the output.
5. Open a pull request with the template: **Plain English**, **What changed**, **How I checked it**, **Not done**, **Next step**. Give me the real PR link and actual state. Follow my documented source merge policy: finish a reviewed, appropriately checked conflict-free merge when delegated; otherwise ask me a direct yes/no question with plain-language merge/no-merge consequences.

Stop and ask me if the work grows bigger than the task, if something cannot be undone, if you would need a secret or a private file, or if two instructions conflict. If you cannot create a branch or a pull request, say so first and give me the files as a list with exact paths.
```

## Weekly review (once a week, after you have written the Weekly note)

```text
You are my AI worker. Weekly refresh of my vault, by its `AGENTS.md`.

- My vault repository: `<your-handle>/<your>-second-brain`

Read: `AI Context.md`, `Profile.md`, `Projects.md`, every note with `type: project`, the last seven notes in `Daily/`, and this week's note in `Weekly/` if it exists.

Produce, on branch `ai/weekly-<YYYY-MM-DD>`:

1. **A refreshed `AI Context.md`.** Keep the frontmatter and the reading contract. Rewrite: Current focus (from the Weekly note's "one thing", otherwise unchanged), Active projects (one line each: name, priority, where it stands, open pull requests), Open loops (unticked tasks from the daily notes older than three days, open questions, waiting-on items), Last refreshed. Link every line to the note it came from. Do not invent; if a project has no "Where it stands" line, write "no status recorded".
2. **A triage list in the pull request body, not in the notes:** every Log line from the seven daily notes that starts with `- [ ]` or carries `#idea`, each with one proposal: task → which project note; new note from the Note template; drop. I decide. Do not move or delete anything.
3. **Nothing else changes.**

Open the pull request. In **Plain English**, give me my week in three sentences, from the notes. Give me the real PR link and actual state. Follow my documented source merge policy: finish a reviewed, appropriately checked conflict-free merge when delegated; otherwise ask me a direct yes/no question with plain-language merge/no-merge consequences. If a note you needed is missing or empty, say so under Not done; a missing note is a gap, not a fact.
```
