# Eval inputs — Jira-Ticket-Writer.md

How to run an eval: open a **fresh** Claude session, load `Jira-Ticket-Writer.md` as a skill (or paste it), then paste one input below verbatim. Check the output against the determinism invariants listed in the skill's Eval Log, and record PASS/FAIL.

---

## Input 1 — One-line vague brain dump

Messiness: hedged wording ("or something"), no scope, no format details, no permissions, and estimate-talk that must not leak into requirements.

```
hey can you write a ticket - marketing wants users to be able to export
their dashboards as pdf or something, should be quick
```

Expected key outcomes: passes the minimum-information gate (actor: users; capability: export dashboards as PDF) → a full Story is produced, not a Clarification Request. "or something" becomes an Open Question about additional formats; "should be quick" is ignored as scope-irrelevant. No invented details (page size, layout, scheduling) appear inside stated Scenarios. Verdict: `Ready for Dev: NO`, blocked on scope/format/permission questions.

---

## Input 2 — Raw refinement-meeting transcript

Messiness: multiple speakers, an off-topic tangent, a value revised mid-meeting (10MB → 8MB), and an unconfirmed naming convention.

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

Expected key outcomes: split threshold captured as **8MB** (later overrides earlier — 10MB appears only as the bank limit in Context); the coffee machine never appears anywhere; sequential `_partN` naming captured but tagged `(assumed — confirm)` with a `[blocking]` Open Question since finance still has to confirm; "show the user how many files were generated" is a stated Scenario (it got explicit agreement). Verdict: `Ready for Dev: NO` — blocked at minimum on the naming-convention confirmation.

---

## Input 3 — Below the minimum-information gate

Messiness: no actor, no scope, no observable symptom. This input exists to prove the skill refuses to hallucinate a story.

```
make the app faster
```

Expected key outcomes: the **Clarification Request** format is emitted instead of a pseudo-story. Exactly the 5 template questions, in the fixed scope → symptom → target → impact → evidence order, none skipped (the input answers nothing). A tentative title is offered. No Gherkin, no invented performance targets.
