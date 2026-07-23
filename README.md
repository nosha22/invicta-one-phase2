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

## Run the skills in Claude

**Claude Code — zero install.** The repo ships them as project skills in `.claude/skills/`, so cloning *is* installing:

```
git clone https://github.com/<username>/invicta-one-phase2.git
cd invicta-one-phase2 && claude
```

**Claude Code — everywhere.** `./install.sh` copies the four skills into `~/.claude/skills/` so they load in every project. Restart the session after.

**claude.ai (web/desktop).** Settings → Capabilities → Skills → *Upload skill*, then drag a per-skill zip (or zip any folder from `.claude/skills/`). Requires a paid plan with code execution enabled; uploads are per-user.

**Any plan fallback.** Create a Claude Project and paste a SKILL.md into its project knowledge — every chat in that Project runs with it.

## Optional: live-AI mode for the Prompt Sensei

GitHub Pages is static — an API key committed here would be public. Instead, deploy [sensei-worker.js](sensei-worker.js) to Cloudflare Workers (free tier; the key lives there as a secret, CORS locked to your Pages origin), then set `SENSEI_API_URL` in `index.html`. Without it, the sensei stays fully functional in deterministic rule-based mode.

## Prove the determinism yourself

```
export ANTHROPIC_API_KEY=sk-ant-...
python3 run_evals.py Jira-Ticket-Writer.md test-inputs-jira-tickets.md --runs 3
python3 run_evals.py Jira-Ticket-Writer.md test-inputs-adversarial.md --runs 3
```

CI runs the no-API dry-run of every fixture on each push, so the plumbing is always verified.

*May the Intelligence Be With You.*
