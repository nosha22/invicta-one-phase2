# Eval inputs — Ticket-Tester.md

How to run an eval: open a **fresh** Claude session, load `Ticket-Tester.md` as a skill (or paste it), then paste one input below verbatim. Check the output against the determinism invariants in the skill's Eval Log, and record PASS/FAIL.

Inputs 1 and 2 use this ticket (it is the output shape produced by `Jira-Ticket-Writer.md` — the skills are designed to chain):

```markdown
# [Story] Split SEPA export files above the bank size limit

## Context
The bank rejects SEPA files over 10MB. Exports from the invoice screen must be split to stay safely under that limit.

## Acceptance criteria
Scenario 1: Export exceeding the size limit is split
  Given an invoice batch whose SEPA export exceeds 8MB
  When the user exports the batch
  Then the export is split into multiple files, each at most 8MB

Scenario 2: User sees how many files were generated
  Given an export was split into multiple files
  When the export completes
  Then the UI shows the number of files generated

## Proposed edge-case scenarios (not stated — confirm before implementing)
Scenario A: Export of an empty batch
  Given an invoice batch with no invoices
  When the user exports the batch
  Then the user sees a message that there is nothing to export

## Open questions
Q1 [blocking]: Exact file naming convention — sequential suffixes _part1, _part2 (assumed — confirm with finance).

## Ready for Dev
NO — blocked on Q1
```

---

## Input 1 — The ticket above, nothing else

Messiness: a concrete value (8MB) with unstated at-limit behavior, an assumed naming requirement, and a proposed (unconfirmed) edge scenario — plenty of bait to invent expectations.

Expected key outcomes: **Mode A.** TC for Scenario 1 and Scenario 2 (stated); boundary trio around 8MB with the exactly-8MB expectation tagged `(expected per limit — confirm)`; a naming test case carrying the `(assumed — confirm)` tag; the empty-batch scenario labeled `exploratory (unconfirmed requirement)`; a negative/permission case with `confirm` tag; traceability check `2/2 ✓`; manifest is the last json block.

---

## Input 2 — Same ticket + messy QA execution notes

Messiness: informal language, mixed pass/fail results, and three failures of *different natures* — the classifier's real test.

```
ran the export on staging today:
- 12MB invoice batch -> got 2 files but the second file is 0 bytes??
- file names came out export_1.xml and export_2.xml, not _part1 like we said
- 7MB batch fine, single file, opens ok in the bank portal
- also the app froze for like 30 seconds during the big export, had to just wait it out
```

Expected key outcomes: **Mode B.** Zero-byte second file → **Bug, Blocker** (payment data missing = data loss, basic correctness — a Bug even though no AC says "files must not be empty"). Naming mismatch → **Requirement gap**, not a bug (the `_partN` convention was `(assumed — confirm)` in the ticket) — routed to the PO with a question. 30-second freeze → **Requirement gap** (no stated performance target). 7MB pass → **Observation**. Coverage cross-check notes that Scenario 2 (file-count message) was never verified. Exactly one bug ticket; repro steps only from evidence.

---

## Input 3 — Raw customer complaint email, no ticket

Messiness: urgency noise, a vague threshold, missing environment details, and an implied-but-unstated workaround (a trap for the severity rubric).

```
From: cfo@brightmove-logistics.example
Subject: URGENT - SEPA export broken

Hi, since yesterday when we download the SEPA file for invoice batches with
more than ~100 invoices, our bank portal says "invalid format" and rejects
the file. Smaller batches work fine. We are on version 3.12. Payroll runs
Friday, please fix asap!!
```

Expected key outcomes: **Mode B** without a ticket. One bug: bank rejects export as invalid format for batches over ~100 invoices. Severity **High** — a main function is broken and no workaround was *stated* ("smaller batches work fine" is evidence about the boundary, not a stated workaround; splitting batches manually was never mentioned by the reporter — inferring it would quietly downgrade real pain). Steps to reproduce drawn only from the email (version 3.12, >~100 invoices, upload to bank portal); bank portal name and browser/OS `unknown — confirm`; Expected sourced to the reporter's stated expectation (bank accepts the file); urgency/deadline noise ("Payroll runs Friday", "asap!!") does not leak into severity — the rubric decides. Ready to file: YES.
