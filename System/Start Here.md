---
type: index
---

# Start Here

The first-time checklist. Allow extra time for installation and authentication. Every step has something to see.

For a guided Google Meet call, start with [[onboarding/FRIEND|the participant guide]]. It includes a browser route and a first useful contribution selected and produced by your AI. The facilitator can use [the call runbook](../onboarding/README.md).

## On your computer

- [ ] Install **Git** itself. Mac: open Terminal, type `git --version`, accept the prompt to install the command line tools. Windows: git-scm.com, all defaults. Obsidian Git needs it; GitHub Desktop's built-in copy is not enough.
- [ ] Install **GitHub Desktop** and **Obsidian**. Sign in to GitHub Desktop and check its Git identity settings. Obsidian Git uses system Git; Desktop sign-in does not guarantee the plugin can authenticate. Verify its push below.
- [ ] GitHub Desktop → **Clone repository** → this repository → into a new folder `~/Projects/<Your Name>/`.
- [ ] Obsidian → **Open folder as vault** → the cloned folder itself. When asked, click **Trust author and enable plugins**. The two plugins this vault uses, Git and Dataview, come with it already set up; that one click turns them on.

## Make it yours

- [ ] Obsidian Git shows in the status bar. If it says Git is not installed, install Git (first step above) and restart Obsidian. If it says "Please tell me who you are", set your name and email in GitHub Desktop → Settings → Git.
- [ ] Open [[Profile]]. Fill the three lines marked **you**: your name, your GitHub handle, your off-limits list in your own words. Put today's date on the "Set up" line.
- [ ] Click the **calendar icon** on the left ribbon. Today's note appears from the template. Type one line under **Log**.
- [ ] Open [[Projects]]. The tables render (empty is fine). Raw `TABLE ...` text means the plugins are off: Settings → Community plugins → turn off Restricted mode → enable Dataview and Git.

## Watch it back itself up

- [ ] Wait up to ten minutes, or run the command **Obsidian Git: Commit-and-sync**. The status bar shows it.
- [ ] Refresh your repository on GitHub. Verify your exact new line in today's note. A plugin push confirms that route works; observe a later automatic commit before calling the ten-minute schedule verified.
- [ ] If plugin authentication blocks you, disable the Git plugin and use Desktop to inspect changes, **Commit to main → Push origin**, then verify the line on GitHub. Record that saving is manual for now. Never paste tokens into a call or chat. On a conflict, preserve both copies and ask for help instead of forcing a push.

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

Use [[onboarding/FRIEND|the guided first contribution]] to let your AI find and do useful work from your project context. [[System/Prompts|Prompts]] also has task, new-repository, and weekly-review workflows; another repository is optional.
