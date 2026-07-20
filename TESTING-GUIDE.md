# Phase 2 — Verification & Submission Guide

*What's done, what's missing, and exactly how to test. Deadline: July 31.*

## Status against "How to Win"

| Requirement (from the briefing) | Status |
|---|---|
| Production-ready SKILL.md | ✅ Done — four of them (3 trials + Inspector bonus), with fixed rules, templates, worked examples, and decision manifests |
| "Eval Log at the bottom … proving you tested it with at least 3 separate, messy inputs" | ⚠️ **Half done — this is the gap.** Each log has the 3 messy inputs and a recorded Run 1, but Runs 2–3 are marked `pending`. Until those are filled in, the log doesn't yet *prove* "outputs remained deterministic". |
| Submit the link via the Official Google Form | ⬜ To do (link is in your briefing document) |
| Commit the file to the Google Drive Folder | ⬜ To do |

The game page is kickoff material, not part of the graded submission — nothing blocking there.

## How to run one eval (~3 minutes)

1. **Fresh session.** Open a new Claude chat with no history. Easiest setup: create a Claude **Project**, add the SKILL.md to its project knowledge — then every new chat inside it is a clean run with the skill loaded. (Claude Code alternative: put the file at `.claude/skills/<name>/SKILL.md`.)
2. **Paste the input.** Copy input #N from the matching `test-inputs-*.md` **verbatim** and send it.
3. **Save the output.** Copy the complete response — including the final ```json decision manifest — into a file named `run1.md`.
4. **Repeat twice** in fresh chats → `run2.md`, `run3.md`.
5. **Prove it:** `python3 check_determinism.py run1.md run2.md run3.md` → expect `RESULT: PASS — 3 runs are decision-deterministic`.
6. **Spot-check the human invariants** listed in that skill's Eval Log — the ones a script can't judge (e.g. "style hunk not flagged", "coffee-machine tangent absent from the ticket", "no invented findings on the clean diff").
7. **Record it.** In the Eval Log table, replace `pending` with `PASS` + date, and paste the checker's RESULT line under the table.

**If the checker prints FAIL:** the diff shows exactly which decision drifted between runs. Tighten that specific rule in the skill (add a tie-break, fix a precedence), then re-run. That drift-fix loop is the whole engineering discipline the challenge is grading.

## Tracking checklist

| Skill | Input 1 | Input 2 | Input 3 |
|---|---|---|---|
| Release-Notes-Writer.md | ☐ ☐ ☐ | ☐ ☐ ☐ | ☐ ☐ ☐ |
| Jira-Ticket-Writer.md | ☐ ☐ ☐ | ☐ ☐ ☐ | ☐ ☐ ☐ |
| PR-Reviewer.md | ☐ ☐ ☐ | ☐ ☐ ☐ | ☐ ☐ ☐ |
| Ticket-Tester.md (bonus) | ☐ ☐ ☐ | ☐ ☐ ☐ | ☐ ☐ ☐ |

(Each cell = runs 1–3. Run 1 is already recorded in the logs from the authoring pass — re-run it yourself if you want all three to be your own.)

Note for Jira-Ticket-Writer: run the fixture evals with connectors **off** so runs are comparable; test the Confluence/Drive grounding separately against your real docs.

## Submission (per skill)

- [ ] Eval Log complete: 3 inputs × 3 runs recorded, checker `PASS` pasted
- [ ] File committed to the Google Drive folder
- [ ] Link submitted via the Official Google Form
- [ ] Strongly recommended: commit `test-inputs-*.md` + `check_determinism.py` alongside the skill — reviewers can then reproduce your determinism proof in one command, which is exactly the "software engineering principles applied to natural language" the briefing says wins

## Time budget

Roughly 10 minutes per skill (3 inputs × 3 runs + checker). All four skills: about 40 minutes of testing, comfortably inside the July 31 deadline.
