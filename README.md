# Invicta-One · Phase 2 — Floor Command & Skill Fleet

![evals](https://github.com/<username>/invicta-one-phase2/actions/workflows/evals.yml/badge.svg)

🎮 **Play the floor:** https://<username>.github.io/invicta-one-phase2/
Walk the real Visma Porto floor plan, equip the trial skills in the rooms, test them at the terminals, and visit the Prompt Sensei on the terraço. (Replace `<username>` above after forking/pushing.)

## The skill fleet (Phase 2 deliverables)

| Skill | Trial |
|---|---|
| [Release-Notes-Writer.md](Release-Notes-Writer.md) | 1 · The Archivist |
| [Jira-Ticket-Writer.md](Jira-Ticket-Writer.md) | 2 · The System Scribe |
| [PR-Reviewer.md](PR-Reviewer.md) | 3 · The Code Sentinel |
| [Ticket-Tester.md](Ticket-Tester.md) | Bonus · The Inspector |

Start with [SUBMISSION.md](SUBMISSION.md) (the 30-second case), then [README-Skill-Fleet.md](README-Skill-Fleet.md) (architecture) and [TESTING-GUIDE.md](TESTING-GUIDE.md) (eval procedure).

## Prove the determinism yourself

```
export ANTHROPIC_API_KEY=sk-ant-...
python3 run_evals.py Jira-Ticket-Writer.md test-inputs-jira-tickets.md --runs 3
python3 run_evals.py Jira-Ticket-Writer.md test-inputs-adversarial.md --runs 3
```

CI runs the no-API dry-run of every fixture on each push, so the plumbing is always verified.

*May the Intelligence Be With You.*
