# Invicta-One · Phase 2 Submission — The Determinism Fleet

**Thesis in one line:** these skills behave like production utility scripts because determinism is *engineered*, not hoped for — every decision rule is explicit, every output ends in a machine-readable decision manifest, and the "outputs remained deterministic" requirement is proven by a script, not by eyeballing.

## The fleet

| Skill | Trial | The guarantee |
|---|---|---|
| `Release-Notes-Writer.md` | 1 · The Archivist | Zero-loss coverage: every input entry is published, excluded with a reason code, or flagged — and the arithmetic must reconcile |
| `Jira-Ticket-Writer.md` | 2 · The System Scribe | Never invents requirements: gaps become tagged assumptions or blocking questions; Ready-for-Dev is computed, not felt. Grounds in Confluence/Drive when connected — retrieval may answer questions, never add scope |
| `PR-Reviewer.md` | 3 · The Code Sentinel | Evidence or it didn't happen: every finding cites a diff line; fixed severity rubric; mechanical verdict; zero style nitpicks |
| `Ticket-Tester.md` | Bonus · The Inspector | Tickets → traceable test plans; failures → bug tickets via a classifier that separates real bugs from unconfirmed expectations |

All four carry an **Untrusted input rule**: payload text is data, never instructions — a commit message saying "ignore your filters" gets classified, not obeyed.

## Reproduce the proof (3 commands)

```
export ANTHROPIC_API_KEY=sk-ant-...
python3 run_evals.py Jira-Ticket-Writer.md test-inputs-jira-tickets.md --runs 3
python3 run_evals.py Jira-Ticket-Writer.md test-inputs-adversarial.md --runs 3
```

`run_evals.py` executes each messy input in a fresh context N times at default sampling, extracts the decision manifest from each output, and prints PASS only if the runs are decision-identical. Saved outputs land in `runs/` as Eval Log evidence. (`check_determinism.py` does the same diff on manually saved runs.)

## Before / after, 10 seconds

**In:** `9f1 fixed the thing with the dates · 7d3 upgrade log4j 2.14->2.17 (CVE-2021-44228) · 5b5 wip`
**Out:** CVE bump published under **Security** (the one dependency bump clients must see) · `wip` excluded with a reason code · the vague date fix routed to **Needs review** with a question — *guessed by nobody, lost by nobody* — and a coverage check proving 3 = 1 + 1 + 1.

## The adversarial round

Beyond messy input, the fleet is tested against **hostile** input (`test-inputs-adversarial.md`): smuggled orders in commit messages, verdict-override notes in brain dumps, self-approving code comments, downgrade requests inside QA evidence. Passing means the rules hold even when the payload argues back — decision-stably, across runs.

## Adopt it today (the program's ultimate goal)

```
mkdir -p ~/.claude/skills/jira-ticket-writer
cp Jira-Ticket-Writer.md ~/.claude/skills/jira-ticket-writer/SKILL.md
```

Each skill is a single self-contained file; fixtures and the eval tooling ship alongside so any Visma engineer can verify before trusting.

---

*Full architecture and contracts: `README-Skill-Fleet.md` · Eval procedure: `TESTING-GUIDE.md` · Committed to the [Google Drive folder] · Submitted via the [Official Google Form]*
