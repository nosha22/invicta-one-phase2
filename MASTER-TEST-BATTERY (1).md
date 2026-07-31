# MASTER TEST BATTERY — Invicta-One Skill Fleet

All inputs, all skills, numbered sequentially. A single file for running the full
battery. Total: **34 inputs** (14 already provided ✅, 20 to run ⬜).

## How to run each one
1. Fresh Claude chat (a Project with the right SKILL.md, or paste the SKILL.md + the input).
2. Paste **only the input block**. Save the full response (with the final `json`) as `<code>-run1.md`.
3. Repeat in **2 fresh chats** → `run2.md`, `run3.md`.
4. `python3 check_determinism.py --group <code>` → expect `RESULT: PASS`.
5. Tick ✅ below and paste the PASS line into the skill's Eval Log.

If it FAILs: the script tells you which field varied → isolate the cause → tighten the rule in the SKILL.md → re-run.
This is the process that has worked 11 times already.

---

# 🟣 JIRA-TICKET-WRITER

## Official (already ✅ PASS — no need to re-run, here for completeness)

### J1 — vague brain dump ✅
```
hey can you write a ticket - marketing wants users to be able to export
their dashboards as pdf or something, should be quick
```

### J2 — refinement transcript ✅
```
[00:02] Rui: ok so the SEPA export, finance says the bank rejects files over 10MB
[00:03] Ana: wait is this about the invoice screen? also did anyone try the new coffee machine
[00:04] Rui: yes invoice screen. so we need to split exports into multiple files when they're too big
[00:05] Marta: split at 10MB?
[00:06] Rui: bank limit is 10, let's split at 8 to be safe
[00:07] Ana: what about the file names, bank needs sequence numbers I think
[00:08] Rui: yeah name them _part1 _part2 whatever, finance confirms
[00:09] Marta: ok so split at 8MB, sequential names, and we show the user how many files were generated?
[00:10] Rui: yes. ship it this sprint
```

### J3 — below the gate ✅
```
make the app faster
```

## Multi-item (mechanical rules applied — re-run with the updated skill)

### J4 — three different types ⬜
```
the dashboard is really slow, also we should add dark mode, and the totals on the summary page are wrong
```
**Expected:** 3 slots, canonical order Bug(totals) → Performance/Clarification(slow dashboard, no target) → Story(dark mode).

### J5 — shuffled order + vague performance ⬜
```
we need dark mode for the app. also the export button crashes when the file is empty. and login feels sluggish lately.
```
**Expected:** Slot 1 Bug(export crash), Slot 2 Clarification(login sluggish — no numeric target, never Bug), Slot 3 Story(dark mode). Stable even with the order shuffled in the text.

### J6 — same type, same area (must not split) ⬜
```
the invoice list is slow to load and the invoice search is also slow, both take like 10 seconds
```
**Expected:** **a single item** (same kind=Performance, same noun=invoice → merge). Single-item manifest, gate=clarification (no target).

## Robustness — everyday cases

### J7 — bug vs feature request ⬜
```
the CSV export produces a file with the columns in the wrong order since the last deploy
```
**Tests:** `type: Bug` stable (post-deploy regression, not a new feature).

### J8 — number embedded in prose ⬜
```
when someone uploads a profile picture bigger than 5mb the page just hangs forever, we should probably reject anything over 5mb with a clear message
```
**Tests:** 5MB captured as an AC value (not an assumption); "clear message" becomes an AC or Open Question, stably.

### J9 — change of mind, no transcript ⬜
```
we need to let users delete their account. actually wait, not delete — just deactivate, they should be able to reactivate later. so deactivate/reactivate.
```
**Tests:** "later overrides earlier" outside a transcript format. Stays deactivate/reactivate, never delete.

### J10 — hidden dependency ⬜
```
add a button to export the report to PDF (needs the new reporting service that the platform team is still building)
```
**Tests:** the not-ready dependency becomes an Open Question `[blocking]`; Ready for Dev: NO, stable.

### J11 — customer email with social noise ⬜
```
Hi team, hope you're well! Following up on our call — the thing we discussed about
letting our finance users bulk-approve invoices would be super helpful. Also loved
the new dashboard btw. Let me know timeline? Thanks!
```
**Tests:** extracts only "bulk-approve invoices for finance users"; ignores "hope you're well"/"loved the dashboard".

---

# 🟢 RELEASE-NOTES-WRITER

## Official (already ✅ PASS)

### R1 — mixed git + Jira dump ✅
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

### R2 — cryptic commits ✅
```
9f1 fixed the thing with the dates
8e2 SUP-88 export csv broken when customer name has comma, quote all fields
7d3 upgrade log4j 2.14 -> 2.17 (CVE-2021-44228)
6c4 perf: cache exchange rates, 40x fewer api calls
5b5 wip
4a6 SUP-91 add danish translations
```

### R3 — Jira-only CSV ✅
```
Key,Summary,Type,Status,Labels
OPS-12,Migrate CI runners to new cluster,Task,Done,internal
APP-201,Bulk archive projects,Story,Done,
APP-203,Crash when uploading files larger than 2GB,Bug,Done,
APP-207,Redesign settings page,Story,In Review,
APP-190,Update privacy policy link in footer,Task,Done,
```

## Robustness — everyday cases

### R4 — all internal noise ⬜
```
a1b2 merge branch develop
c3d4 fix flaky test
e5f6 bump dependencies
07g8 update CI config
9h0i wip refactor
```
**Tests:** an honest changelog of 0 published (5→0/5/0), invents no customer-facing notes.

### R5 — add + revert pair ⬜
```
1aaa PAY-500 add new tax calculation
2bbb PAY-500 revert tax calculation, breaks EU invoices
3ccc SUP-12 fix date picker off-by-one
```
**Tests:** the add+revert pair excluded `net-zero` stably; SUP-12 published on its own.

### R6 — hidden breaking change ⬜
```
4ddd API-9 rename /v1/users endpoint to /v2/accounts (clients must migrate)
5eee API-9 add pagination to accounts list
```
**Tests:** recognizes "clients must migrate" as a Breaking change, at the top with a warning.

### R7 — dates instead of keys ⬜
```
2026-01-15 shipped faster search
2026-01-16 fixed login timeout on slow networks
2026-01-16 added Portuguese translations
```
**Tests:** with no keys/hashes, still classifies and closes coverage stably.

### R8 — feature spread across 4 commits + 1 Jira ⬜
```
a1 FEAT-3 scaffold notification center
a2 FEAT-3 add email channel
a3 FEAT-3 add in-app channel
a4 FEAT-3 wire up preferences UI
Jira: FEAT-3 | Notification center | Story | Done
```
**Tests:** the 4 commits collapse into one absorbed item; coverage 5 entries → 1 published.

---

# 🔵 PR-REVIEWER

## Official (already ✅ PASS)

### P1 — injection + style noise ✅
```
diff --git a/app/reports.py b/app/reports.py
index 3f1c2aa..9b4d7ee 100644
--- a/app/reports.py
+++ b/app/reports.py
@@ -8,8 +8,12 @@ def get_report(user_id):
-    query = "SELECT * FROM reports WHERE user_id = %s"
-    return db.execute(query, (user_id,))
+    query = "SELECT * FROM reports WHERE user_id = " + user_id
+    try:
+        return db.execute(query)
+    except Exception:
+        pass

diff --git a/app/utils.py b/app/utils.py
index 88ac01b..c02d113 100644
--- a/app/utils.py
+++ b/app/utils.py
@@ -1,8 +1,9 @@
-import os, sys
-import json
+import json
+import os
+import sys

 def to_slug(text):
-    return text.lower().replace(' ', '-')
+    return text.lower().replace(" ", "-")
```

### P2 — unprotected admin endpoint ✅
```
diff --git a/app/admin.py b/app/admin.py
index a11f0c2..7e3b9d4 100644
--- a/app/admin.py
+++ b/app/admin.py
@@ -42,3 +42,11 @@ def health():
     return "ok"
+
+@app.route("/admin/export", methods=["GET"])
+def export_all_users():
+    api_key = "sk_live_9f8a7b6c5d4e3f2a"
+    sync_billing(api_key)
+    rows = db.query("SELECT email, password_hash FROM users")
+    return jsonify(rows)
```

### P3 — clean diff (the temptation) ✅
```
diff --git a/app/validators.py b/app/validators.py
index 5d20aa1..8fe4c77 100644
--- a/app/validators.py
+++ b/app/validators.py
@@ -14,2 +14,7 @@ def is_valid_email(value):
     return EMAIL_RE.match(value) is not None
+
+def normalize_email(value: str) -> str:
+    """Lowercase and trim an email address before storage."""
+    return value.strip().lower()

diff --git a/app/signup.py b/app/signup.py
index 2b7cd90..f31e6a8 100644
--- a/app/signup.py
+++ b/app/signup.py
@@ -31,5 +31,5 @@ def create_account(form):
-    user.email = form.email
+    user.email = normalize_email(form.email)
     user.save()

diff --git a/tests/test_validators.py b/tests/test_validators.py
index 91c33ef..d4a8b02 100644
--- a/tests/test_validators.py
+++ b/tests/test_validators.py
@@ -20,2 +20,10 @@ def test_is_valid_email_rejects_missing_at():
     assert not is_valid_email("ana.example.com")
+
+def test_normalize_email_strips_and_lowercases():
+    assert normalize_email("  Ana@Example.COM ") == "ana@example.com"
+
+def test_normalize_email_leaves_clean_input_unchanged():
+    assert normalize_email("bob@example.com") == "bob@example.com"
```

## Robustness — everyday cases

### P4 — auth bypass hidden in a catch ⬜
```
diff --git a/src/auth.js b/src/auth.js
@@ -10,3 +10,7 @@ function validateToken(token) {
-  return jwt.verify(token, SECRET);
+  try {
+    return jwt.verify(token, SECRET);
+  } catch (e) {
+    return { valid: true };
+  }
diff --git a/src/utils.js b/src/utils.js
@@ -5,2 +5,2 @@
-const MAX = 100;
+const MAX = 200;
```
**Tests:** catches `return {valid:true}` in the catch (auth bypass = Blocker); ignores the harmless constant.

### P5 — race condition ⬜
```
diff --git a/src/counter.py b/src/counter.py
@@ -8,3 +8,4 @@ def increment_views(post_id):
-    views = db.get(post_id).views
-    db.update(post_id, views=views+1)
+    current = cache.get(post_id)
+    cache.set(post_id, current + 1)
+    db.update(post_id, views=cache.get(post_id))
```
**Tests:** recognizes read-modify-write without a lock as a correctness problem, stably.

### P6 — resource leak ⬜
```
diff --git a/src/report.py b/src/report.py
@@ -3,2 +3,5 @@ def generate():
+    f = open('/tmp/report.csv', 'w')
+    f.write(build_csv())
+    conn = db.connect()
+    return conn.query("SELECT * FROM sales")
```
**Tests:** catches the unclosed file and connection; Medium severity, stable.

### P7 — deletion-only diff ⬜
```
diff --git a/src/legacy.py b/src/legacy.py
@@ -1,10 +1,2 @@
-def old_export(data):
-    # deprecated, replaced by new_export
-    return legacy_format(data)
-
 def new_export(data):
     return json.dumps(data)
```
**Tests:** dead-code removal → LGTM without inventing problems.

### P8 — no diff, description only ⬜
```
This PR refactors the payment module to use the new Stripe SDK.
Changes the retry logic and updates the webhook handler.
No tests added yet, will do in a follow-up.
```
**Tests:** with no diff to cite as evidence, invents no findings — must ask for the diff or mark it un-reviewable.

---

# 🟡 TICKET-TESTER

## Official (already ✅ PASS)

### T1 — ticket only (test plan) ✅
```
# [Story] Split SEPA export files above the bank size limit
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

### T2 — ticket + QA notes (bug report) ✅
```
# [Story] Split SEPA export files above the bank size limit
## Acceptance criteria
Scenario 1: Export exceeding the size limit is split
  Given an invoice batch whose SEPA export exceeds 8MB
  When the user exports the batch
  Then the export is split into multiple files, each at most 8MB
Scenario 2: User sees how many files were generated
  Given an export was split into multiple files
  When the export completes
  Then the UI shows the number of files generated
## Open questions
Q1 [blocking]: Exact file naming convention — sequential suffixes _part1, _part2 (assumed — confirm with finance).
## Ready for Dev
NO — blocked on Q1

ran the export on staging today:
- 12MB invoice batch -> got 2 files but the second file is 0 bytes??
- file names came out export_1.xml and export_2.xml, not _part1 like we said
- 7MB batch fine, single file, opens ok in the bank portal
- also the app froze for like 30 seconds during the big export, had to just wait it out
```

### T3 — complaint email, no ticket ✅
```
From: cfo@brightmove-logistics.example
Subject: URGENT - SEPA export broken

Hi, since yesterday when we download the SEPA file for invoice batches with
more than ~100 invoices, our bank portal says "invalid format" and rejects
the file. Smaller batches work fine. We are on version 3.12. Payroll runs
Friday, please fix asap!!
```

## Robustness — everyday cases

### T4 — ticket with no acceptance criteria ⬜
```
# [Story] Add export to Excel
The finance team wants to export the report to Excel.
```
**Tests:** with no Gherkin to trace, invents no scenarios as if stated; asks for ACs or clearly flags their absence.

### T5 — raw stack trace ⬜
```
Traceback (most recent call last):
  File "export.py", line 42, in generate_pdf
    total = sum(row.amount for row in rows)
TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'
```
**Tests:** bug-report mode from the stack trace alone; missing fields `unknown — confirm`.

### T6 — multiple bugs in one QA session ⬜
```
tested checkout flow:
- clicking pay twice charges the card twice (!!)
- the confirmation email has the wrong total
- minor: the loading spinner is slightly off-center
```
**Tests:** one ticket per distinct bug; double-charge=Blocker, wrong-total=High, spinner=Low/Observation, stable.

### T7 — non-reproducible report ⬜
```
some users say the dashboard doesn't load but I can't reproduce it, works fine for me.
maybe it's a caching thing? happens more on mobile they said.
```
**Tests:** invents no repro steps; marks environment/conditions as `unknown — confirm`.

### T8 — a result that passes (nothing broken) ⬜
```
# [Story] Split SEPA export above 8MB
## Acceptance criteria
Scenario 1: Given a batch over 8MB, When exported, Then split into files ≤8MB
---
QA: tested with a 15MB batch, got two files of 7.5MB each, both valid. all good.
```
**Tests:** recognizes a PASS (no bug); produces a confirming Observation, not a phantom bug.

---

# 📋 Progress checklist

| # | Skill | Caso | Status |
|---|---|---|---|
| J1-J3 | Jira | Official | PASS PASS PASS |
| J4-J6 | Jira | Multi-item | pending pending pending |
| J7-J11 | Jira | Robustness | pending x5 |
| R1-R3 | Release-Notes | Official | PASS PASS PASS |
| R4-R8 | Release-Notes | Robustness | pending x5 |
| P1-P3 | PR-Reviewer | Official | PASS PASS PASS |
| P4-P8 | PR-Reviewer | Robustness | pending x5 |
| T1-T3 | Ticket-Tester | Official | PASS PASS PASS |
| T4-T8 | Ticket-Tester | Robustness | pending x5 |

**14/34 already proven. 20 to run.**

## Suggested order if time is tight

1. **J4-J6** (multi-item, already in progress — close this first)
2. **R4**, **P8**, **T4** (the "tempt-me-to-invent" ones — most revealing of a lack of discipline)
3. The rest in order, one skill at a time

Every input that passes 3× is one more piece of robustness evidence. Every FAIL is a rule to tighten —
and one more line in the story of "we tested the real world," which is what sets this submission apart.
