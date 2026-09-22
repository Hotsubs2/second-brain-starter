---
type: index
---

# Start Here

The first-time checklist. Twenty minutes. Every step has something to see.

## On your computer

- [ ] Install **Git** itself. Mac: open Terminal, type `git --version`, accept the prompt to install the command line tools. Windows: git-scm.com, all defaults. Obsidian Git needs it; GitHub Desktop's built-in copy is not enough.
- [ ] Install **GitHub Desktop** and **Obsidian**. Sign in to GitHub Desktop: it stores the GitHub login Obsidian Git uses and sets your name and email for commits.
- [ ] GitHub Desktop → **Clone repository** → this repository → into a new folder `~/Projects/<Your Name>/`.
- [ ] Obsidian → **Open folder as vault** → the cloned folder itself. When asked, click **Trust author and enable plugins**. The two plugins this vault uses, Git and Dataview, come with it already set up; that one click turns them on.

## Make it yours

- [ ] Obsidian Git shows in the status bar. If it says Git is not installed, install Git (first step above) and restart Obsidian. If it says "Please tell me who you are", set your name and email in GitHub Desktop → Settings → Git.
- [ ] Open [[Profile]]. Fill the three lines marked **you**: your name, your GitHub handle, your off-limits list in your own words. Put today's date on the "Set up" line.
- [ ] Click the **calendar icon** on the left ribbon. Today's note appears from the template. Type one line under **Log**.
- [ ] Open [[Projects]]. The tables render (empty is fine). Raw `TABLE ...` text means the plugins are off: Settings → Community plugins → turn off Restricted mode → enable Dataview and Git.

## Watch it back itself up

- [ ] Wait up to ten minutes, or run the command **Obsidian Git: Commit-and-sync**. The status bar shows it.
- [ ] Refresh your repository on GitHub. `Profile.md` has your name; `Daily/` has today. That is the whole backup story.

## Let an AI read it

- [ ] Ask any AI: "Read `Profile.md` and `AI Context.md` in `<handle>/<name>-second-brain` and tell me, in three sentences, who I am and what you are not allowed to do." If it cannot see GitHub, paste the two notes in. A correct answer closes the loop.

## Optional, only if an AI works on your computer

- [ ] "Copy the three files in `System/projects-folder/` to `~/Projects`." They tell an AI that starts in that folder how it works.

## If an AI can only read: the by-hand loop

Some AIs can read GitHub but cannot write to it. The system does not care. When an AI hands you files instead of a pull request:

1. GitHub Desktop → **New branch** → name it `me/<slug>`.
2. Create the files at the paths the AI gave, inside the cloned folder.
3. GitHub Desktop shows the changes. One-line summary → **Commit** → **Publish branch**.
4. **Create Pull Request**. Paste the AI's plain-English summary into the body.
5. Read it, merge it, delete the branch. Same loop, same rules.

## Next

[[System/Prompts|Prompts]] has the four things you paste into any AI. Start with **New project**.
