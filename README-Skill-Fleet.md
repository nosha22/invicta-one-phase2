# Invicta-One Skill Fleet — README

Four skills, one design system. Each skill is an independent, production-ready utility — and their inputs and outputs are contracts, so they compose into a pipeline that covers the delivery loop from stakeholder sentence to client changelog.

## The pipeline

```
 stakeholder brain dump / refinement transcript
        │
        ▼
 [jira-ticket-writer] ◄── grounded via Confluence / Google Drive when connected
        │   ticket: Gherkin ACs, tagged assumptions, Ready-for-Dev verdict
        ▼
 [ticket-tester · Mode A] ──► traceable test plan
        │
        ▼   execution (humans, CI, or agents) ──► failure evidence
        │
 [ticket-tester · Mode B] ──► bug tickets ──► filed to Jira on explicit confirmation
        
 code diff / PR ──────────► [pr-reviewer] ──► evidence-cited findings + verdict
 
 sprint end: git log + Jira export ──► [release-notes-writer] ──► client changelog
```

## Shared contracts

- **Decision manifest.** Every skill ends its output with a machine-readable summary of its decisions — always the last fenced `json` block. Prose may vary between runs; decisions may not. The manifest is both the audit trail and the interop surface.
- **Chaining.** `jira-ticket-writer`'s `Scenario` blocks and `(assumed — confirm)` tags are exactly what `ticket-tester`'s derivation rules and three-bucket classifier consume. `pr-reviewer`'s missing-tests findings point at the gap `ticket-tester` Mode A fills. `release-notes-writer` reads the same Jira keys the other skills produce and reference.
- **Facts vs. fiction discipline, everywhere.** Unknowns become explicit questions or `confirm` tags — never guesses. Retrieval (Confluence/Drive) may answer questions and enrich context, but may never add requirements. Side effects (creating Jira issues) happen only after an explicit human go-ahead, with a duplicate search first.
- **Fixed templates, fixed orderings, fixed rubrics.** Classification precedence, severity rubrics, verdict mappings, and sort orders are spelled out so the model has no stylistic freedom where it matters.

## Determinism proof (the "How to Win" requirement)

Determinism for an LLM skill is defined here as **decision-determinism**: same inputs → same decisions (classifications, verdicts, counts, gates), even if sentences differ. That definition is enforceable and provable:

1. Run a messy input from the matching `test-inputs-*.md` in a **fresh** session; save the full output as `run1.md`.
2. Repeat twice more: `run2.md`, `run3.md`.
3. Prove it: `python check_determinism.py run1.md run2.md run3.md`
4. Paste the `RESULT: PASS` output into the skill's Eval Log and tick the run columns.

If it prints `FAIL`, the diff shows exactly which decision drifted — tighten that rule in the skill and re-run. The checker was itself verified against a reworded/key-shuffled PASS case and a drifted-classification FAIL case.

## Files in this fleet

| File | Role |
|---|---|
| `Release-Notes-Writer.md` | Trial 1 — The Archivist |
| `Jira-Ticket-Writer.md` | Trial 2 — The System Scribe (v1.1: knowledge-base grounding + Jira write-back) |
| `PR-Reviewer.md` | Trial 3 — The Code Sentinel |
| `Ticket-Tester.md` | Bonus — The Inspector: test plans from tickets, bug tickets from failures |
| `test-inputs-*.md` | 3 messy, reproducible eval inputs per skill, with expected outcomes |
| `check_determinism.py` | Automated decision-determinism proof across saved runs |

## Submission checklist (per skill)

- [ ] SKILL.md committed to the Drive folder and linked via the Official Google Form
- [ ] Eval Log at the bottom lists 3 messy inputs with 3 recorded runs each
- [ ] `check_determinism.py` PASS result pasted into the Eval Log
- [ ] The matching `test-inputs-*.md` committed alongside, so any engineer can reproduce the evals
