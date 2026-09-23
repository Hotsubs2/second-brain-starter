---
type: note
---

# Meet onboarding

A reusable guided session for a friend who controls their own computer. It builds on the starter's existing profile, rules, Git review loop, and two bundled Obsidian plugins. Its first-value milestone is a useful contribution the AI selected and produced from the friend's project context.

- **Facilitator:** download/open [meet.html](meet.html) in a browser. GitHub's file preview does not run the guide. It works offline, with copy/select fallbacks, printable stages, and a New call reset. Enter the friend's GitHub handle and repository name; share the participant link, not your local `file://` address.
- **Friend:** share [FRIEND.md](FRIEND.md). It includes preparation, both setup routes, saving, and later-use prompts.
- **Canonical content:** [content.json](content.json) and [prompts/](prompts/). Rebuild HTML with `python3 onboarding/build.py` from the repository root. The participant guide is a shorter companion; update it when the flow changes.

Plan about 75 minutes plus 10–15 minutes of optional preparation. The stage times are a budget, not a guarantee; use the browser shortcut and protect the final 25 minutes for useful work and saving. Limit any single setup blockage to five minutes.

## Version boundary

Based on published `main` at `1d8a3714503d426849f7141a991539f472a6055b`. This version opens the repository root as the Obsidian vault. It does not migrate to the unpublished `catalog.yaml` / `vault/` rebuild. Existing adopters keep their repositories and rules.

The review edition's participant link deliberately names `ai/friends-onboarding`, because a friend copying the published template will not receive these unmerged files. After merging, change `share_url` and the review-branch links in the guides/content to `main`, remove the review-edition caveat, and rebuild before deleting this branch. Until then, retain it as the share target.

## What is and is not established

The call checks actual repository ownership, source access, a saved note, a concrete contribution, and an honest continuation. It distinguishes browser saves, Desktop pushes, Obsidian-plugin pushes, and an observed automatic backup. Native Git authentication is separate from Desktop authentication.

The new prompts authorize bounded initiative for one explicitly started session. They do not configure background work, select a paid AI service, grant connectors access, or establish that any particular audience is validated. A branch separates Git changes, not external authority or local working files. Local AI work should use a separate checkout while Obsidian Git activity is paused.

The facilitator page stores only stage checkboxes locally when browser storage is available. Account and repository fields stay in memory and reset on New call/reload; it makes no network requests. Links open only when clicked. Do not enter credentials or private project content in the facilitator page.

## Source basis

Operational guidance checked against official documentation on September 23, 2026:

- [Meet presentation](https://support.google.com/meet/answer/9308856?hl=en), [presentation troubleshooting](https://support.google.com/meet/answer/16581830?hl=en), and [chat availability](https://support.google.com/meet/answer/9308979?hl=en).
- [GitHub template copies](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template), [Desktop cloning](https://docs.github.com/en/desktop/adding-and-cloning-repositories/cloning-and-forking-repositories-from-github-desktop), and [Git identity](https://docs.github.com/en/desktop/configuring-and-customizing-github-desktop/configuring-basic-settings-in-github-desktop).
- [Obsidian vaults](https://obsidian.md/help/manage-vaults) and [community plugins](https://obsidian.md/help/community-plugins).
- [Obsidian Git installation](https://publish.obsidian.md/git-doc/Installation) and [authentication](https://publish.obsidian.md/git-doc/Authentication).

Menu labels can vary by platform/version. The guide describes the expected visible result and a recovery path rather than treating an exact label as proof.

## Verification

See [verification.md](verification.md) for checks and limits. A walkthrough or synthetic prompt review is not a completed onboarding on a friend's computer, nor evidence of sustained benefit.
