---
type: note
---

# Your notebook and your first useful AI contribution

Bring one project you care about. You do not need to know what to ask AI to do. During the call, you will give it context, let it choose and make one useful contribution, and keep the result somewhere you own.

Allow about 75 minutes. You control your computer; your friend guides the steps. If local installation gets stuck, use the browser route below and finish setup another time.

## Before we meet

- Bookmark this page. The Meet chat may not be available afterward.
- Sign in to [GitHub](https://github.com) and the AI you already use. No new paid AI account is required.
- If convenient, install [GitHub Desktop](https://desktop.github.com/), [Obsidian](https://obsidian.md/download), and [system Git](https://git-scm.com/downloads). On Mac, running `git --version` in Terminal may offer the command line tools installer. Desktop's embedded Git alone is not enough for Obsidian Git.
- Think about one project: what you want to happen, where it stands, decisions already made, and what must stay off limits. Use a few non-sensitive sentences; do not gather private documents.

## During the call

1. Join Google Meet normally, then choose **Present now → A window** or **Your entire screen**. A browser tab only shows that tab. Stop sharing for passwords, MFA, or recovery codes. Resume after sign-in.
2. Open the [starter template](https://github.com/itsadoor-llc/second-brain-starter). Choose **Use this template → Create a new repository**, your own account, a name such as `second-brain`, and **Private**. If you already have a notebook, reuse it and preserve its rules and files.
3. In Desktop, **File → Clone repository**, choose your repository, and remember the local folder. In Obsidian, **Manage vaults → Open folder as vault**, choose that same folder. `Home.md` is at its root. There is no nested `vault/` folder in this version.
4. If you accept Obsidian's community-plugin trust prompt, enable the bundled **Dataview** and **Git** plugins. Fill in `Profile.md`. Click the calendar icon to create today's note and write one harmless line under Log.
5. Run the Git sync/backup command from Obsidian's command palette. Open the exact note on GitHub and confirm the line arrived. Desktop sign-in does not guarantee Obsidian Git authentication. If this fails, disable the Git plugin and use Desktop's **Commit to main → Push origin** for now. A manual push does not prove automatic backup is working.
6. Create `Current project.md` with the project starter below, replacing the brackets with your own words. Save it through the route you verified. No second repository is needed today.
7. Use **Check access**, then **Find useful work**, below. Your AI should produce something useful for your project. If it cannot read your private repository, paste the relevant non-sensitive note text; do not share tokens or make the repository public.
8. Read the actual result. Correct anything wrong. Use **Understand the contribution** for help reviewing it. Keep the useful version using the saving instructions below.

**Browser route:** skip local installation. Edit `Profile.md` on GitHub using the pencil button and commit your own context to `main`. Create `Current project.md` with **Add file → Create new file**. Paste these notes and the relevant `AGENTS.md` rules into your existing AI if repository access is unavailable. The AI can return an unsaved Markdown draft. This route does not establish Obsidian or automatic backups.

If GitHub account setup itself is blocked, keep context and the AI draft in a local text file. Record that repository saving is unfinished.

## Project starter

Use an existing project note if you have one; explicitly give the AI its name/link or paste its text before the prompt. The prompts accept that supplied note in place of `Current project.md`. Do not overwrite an existing note. This note chooses a project for today's session, not your highest life priority.

```markdown
---
type: project
status: active
repos: []
---

# Current project

## Purpose
[What I want to make happen, and why it matters.]

## Current situation
[What exists, what has happened, and what is uncertain.]

## Progress would look like
[An observable improvement; you need not specify an AI task.]

## Decisions
[Decisions already made, or none recorded yet.]

## Boundaries
[What to preserve; what must not happen; what is off limits.]

## Log
[Today's date: this is the project I chose for the onboarding session.]
```

## The prompts you can come back to

Open a prompt, copy its text, and replace `{{HANDLE}}` and `{{VAULT_REPO}}` with your GitHub account and notebook repository name. Your facilitator's runbook fills those in automatically. Replace any square-bracketed instruction with the requested link or update.

If you have no repository yet, copy the Markdown prompt directly from the link below and replace the repository sentence with “I have no repository yet; use the context I paste and return an unsaved draft.” The facilitator's personalized copy buttons require a repository name.

| When | Prompt | What it does |
| --- | --- | --- |
| First connection | [Check access](prompts/01-orient.md) | Establishes what the AI actually read and understood. |
| Ready for useful work | [Find useful work](prompts/02-contribute.md) | Lets the AI select and make one small contribution within your boundaries. |
| Before keeping a result | [Understand the contribution](prompts/04-review.md) | Explains the content, assumptions, changes, and consequences. |
| Next session | [Continue with useful initiative](prompts/03-return.md) | Uses your update and saved work to select the next contribution. |
| Stopping or interrupted | [Pause without losing the thread](prompts/05-checkpoint.md) | Produces a truthful continuation you can check and save. |

These authorize one session at a time. They do not configure an AI to run after the session ends. Future AI sessions must actually read or receive your saved context.

## Keep the result

**If the AI opens a pull request:** open its actual **Files changed**, check that it adds the expected note to your notebook and makes no unrelated changes, and verify important claims. Merge it yourself only when satisfied. An AI's explanation helps you review; it is not independent proof.

**If the result is only in chat:** on GitHub choose **Add file → Create new file**. Give it a descriptive `.md` name, paste the reviewed result, and include `type: note` between `---` lines at the top. In **Commit changes**, choose a new branch such as `me/first-contribution`, propose the change, and create a pull request. Review, then merge it yourself. A local `.md` file is a useful fallback if you run out of time; label it as not yet saved to GitHub.

If an AI works on local files, use a separate checkout/worktree and pause Obsidian Git activity while it works. Switching branches in the folder Obsidian has open changes the files Obsidian sees. Ask your facilitator for help if this is unclear; chat-only output is enough today.

After a remote merge, stop editing in Obsidian, commit and push any owner edits, then fetch/pull `main` using the verified Git route. Confirm the new note appears before continuing. If Git reports a conflict, stop, preserve both copies, and ask for help; do not force-push or discard changes.

## Before leaving

Save this short handoff in your project's Log or a linked note, then verify that save:

```text
Notebook: [GitHub link]
Project note: [link or local path]
Contribution: [link/path; saved, unmerged, or local/chat draft]
How I save today: [browser / Desktop commit + push / plugin push verified / automatic backup observed]
My AI access: [repository read/write / local files / pasted context only]
Still unfinished: [specific item, or none observed]
Next time: give the AI my project note, last contribution, and an update;
use Continue with useful initiative.
```

The useful milestone is work that helped your project and that you can find again. Software installation alone does not establish that.

Later, use [New Project Recipe](../System/New%20Project%20Recipe.md) for a separate project repository, and [Prompts](../System/Prompts.md) for the existing weekly-review workflow. Neither is required for the first contribution.

*Review edition, September 23, 2026. Built for the published root-vault template. Until this branch merges, a new template copy will not include this guide; keep this link. Operational sources and verification limits are in the [maintainer notes](README.md).*
