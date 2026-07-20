# Eval inputs — Release-Notes-Writer.md

How to run an eval: open a **fresh** Claude session, load `Release-Notes-Writer.md` as a skill (or paste it), then paste one input below verbatim. Check the output against the determinism invariants listed in the skill's Eval Log, and record PASS/FAIL.

---

## Input 1 — "Sprint 14 mixed dump" (git + Jira, 17 entries)

Messiness: merge commits, typo/lint/format noise, a revert pair, a version bump, a tests-only commit, commits duplicating Jira tickets, one Reopened and one In Progress ticket.

```
git log --oneline:
a1f9c2b Merge branch 'main' into develop
b7e3d21 PAY-341: add SEPA export button to invoices screen
c9d0a11 fix typo in readme
d4e8f02 PAY-341 hook SEPA export to backend endpoint
e5a7b93 bump version to 3.12.0
f6c1d84 PAY-355: add retry logic for webhook delivery
07a2e45 Revert "PAY-350: enable beta dashboard"
18b3f56 PAY-350: enable beta dashboard
29c4a67 chore: update eslint config
3ad5b78 PAY-362 fix rounding error in VAT totals on credit notes
4be6c89 add tests for vat rounding
5cf7d9a style: reformat payment module with prettier

Jira export:
PAY-341 | SEPA payment file export           | Story | Done
PAY-355 | Improve webhook reliability         | Story | Done
PAY-350 | Beta dashboard rollout              | Story | Reopened
PAY-362 | VAT rounding incorrect on credit notes | Bug | Done
PAY-370 | Dark mode                           | Story | In Progress
```

Expected key outcomes: PAY-341 published as New feature (absorbing 2 commits); PAY-355 Improvement; PAY-362 Fix; PAY-350 excluded `net-zero` (revert pair) despite the ticket; PAY-370 excluded `not-shipped`; all noise commits excluded with reason codes; coverage 17 → 7 published · 10 excluded · 0 review.

---

## Input 2 — "Cryptic commit dump" (git only, 6 entries)

Messiness: missing ticket keys, a `wip` commit, a security CVE dependency bump, and one message too vague to classify safely.

```
9f1 fixed the thing with the dates
8e2 SUP-88 export csv broken when customer name has comma, quote all fields
7d3 upgrade log4j 2.14 -> 2.17 (CVE-2021-44228)
6c4 perf: cache exchange rates, 40x fewer api calls
5b5 wip
4a6 SUP-91 add danish translations
```

Expected key outcomes: `7d3` published under **Security** (CVE exception overrides the dependency-bump exclusion); `8e2` → Fixes; `6c4` → Improvements (translated to client language); `4a6` → New features (Danish language support); `5b5` excluded `wip`; `9f1` → **Needs review** with a question — never guessed, never silently dropped. Coverage 6 → 4 · 1 · 1.

---

## Input 3 — "Jira-only CSV export" (5 rows)

Messiness: extra columns, an internal-labelled infra ticket, a not-yet-done row, and a cosmetic Task that tests the classification rules.

```
Key,Summary,Type,Status,Labels
OPS-12,Migrate CI runners to new cluster,Task,Done,internal
APP-201,Bulk archive projects,Story,Done,
APP-203,Crash when uploading files larger than 2GB,Bug,Done,
APP-207,Redesign settings page,Story,In Review,
APP-190,Update privacy policy link in footer,Task,Done,
```

Expected key outcomes: OPS-12 excluded `internal`; APP-207 excluded `not-shipped`; APP-201 → New features; APP-203 → Fixes; APP-190 → Improvements (user-visible Task, no defect). Coverage 5 → 3 · 2 · 0.
