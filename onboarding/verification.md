---
type: note
---

# Verification — September 23, 2026

## Scope

The review edition targets the published root-vault template at `1d8a3714503d426849f7141a991539f472a6055b`. The remote main head was rechecked and unchanged before preparing the review branch; no open PR overlapped at that check.

## Checks performed

- Built the self-contained HTML from the real JSON and five prompt files. Python and generated JavaScript syntax checks passed. Generator checks covered duplicate IDs, known prompt references, path containment, safe source/share URLs, embedded-text escaping, and full prompt inclusion.
- Inspected the guide in the Codex in-app browser on macOS. Stage navigation, missing-field notices, valid handle/repository substitution, expanded full prompt, successful Copy feedback, and completion checkbox worked. After reload, the checkbox persisted and account/repository fields were blank. New call resets the progress and fields. Visual inspection found readable cards and stage navigation.
- Checked Markdown relative-link targets, whitespace errors, and a deterministic rebuild. No new runtime package dependency or remote asset is required.
- An independent review checked remote-call usability, source access, scope boundaries, manual-save fallback, and conflicts. Its existing-note concern was addressed: an explicitly supplied project note takes precedence over `Current project.md`.

## Synthetic prompt exercise

An independent agent executed the first-contribution prompt in chat-only mode with a fictional Reading Evening project: reserved room, four tables, one hour, bring-your-own book, no registration, and no selected AI task. It chose and drafted a concrete hour-long format with optional conversation, preserved the existing decisions, and labeled the result unsaved. It did not ask the owner to choose a task or claim a PR existed. The owner would still need to judge the proposed format. The exercise exposed an omitted frontmatter requirement for chat-only delivery; the prompt now states that explicitly.

The existing Start a task prompt was compared by inspection: it requires a user-specified task and does not expressly ask the AI to discover one. That comparison was not a controlled paired execution and does not establish superiority across models.

Missing source access and malicious document instructions to email/delete were reviewed as tabletop cases. The prompt requires supplied context and excludes those side effects. This is an instruction review, not evidence that every model will reliably follow it.

## Not established

No real friend's account was created or connected. This change has not been run end to end on a friend's Mac or Windows computer, in an actual Meet call, or through live native-Git authentication. Automatic backup, PR-writing capability of arbitrary AI products, user benefit, and later return behavior must be observed in the actual session. Print styles and offline fallback are implemented; printed pagination and every browser's clipboard permissions have not been qualified. The files are review materials until the owner accepts and merges them.
