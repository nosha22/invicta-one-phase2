# Eval inputs — PR-Reviewer.md

How to run an eval: open a **fresh** Claude session, load `PR-Reviewer.md` as a skill (or paste it), then paste one diff below verbatim. Check the output against the determinism invariants listed in the skill's Eval Log, and record PASS/FAIL.

---

## Input 1 — Real defects buried next to style noise

Messiness: a SQL injection and a swallowed exception sit in one hunk, while a second, larger hunk is pure style churn (import order, quote style) designed to bait nitpicking. No test files touched.

```diff
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

Expected key outcomes: Blocker — SQL injection via concatenation (parameterized query was *removed*, visible on the `-` lines); High — swallowed `except Exception: pass` returning `None` silently; Medium — new logic with no test changes. The `utils.py` hunk produces **zero** findings. Header: `Hunks reviewed: 2/2 across 2 file(s)`. `VERDICT: BLOCK`.

---

## Input 2 — Unprotected admin endpoint

Messiness: a hardcoded live secret, a new admin route with no authentication/authorization, and sensitive data (password hashes) returned in the response. No tests.

```diff
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

Expected key outcomes: three Blockers — hardcoded live API key; new `/admin/export` route with no authn/authz check; emails + password hashes exposed in the response — plus Medium for missing tests. `VERDICT: BLOCK`. Findings sorted and numbered after sorting.

---

## Input 3 — Clean change (the temptation test)

Messiness: none — that's the trap. A small, well-scoped change **with tests included**. The skill must not invent findings to appear thorough.

```diff
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

Expected key outcomes: `No findings.` under Findings; all four categories listed under *Checked, no findings*; at most one Question (e.g. whether other persistence paths for emails exist outside this diff); `VERDICT: LGTM`. Any invented finding = FAIL.
