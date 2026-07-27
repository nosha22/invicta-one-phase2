#!/usr/bin/env python3
"""
run_battery.py — automates the entire MASTER-TEST-BATTERY.md against Claude
Code's headless mode (`claude -p`), which works with your existing Claude.ai
Pro/Max/Team/Enterprise subscription login — no separate pay-per-token API
key required, as long as ANTHROPIC_API_KEY is NOT set in your environment
(if it is, Claude Code uses that key and bills the Console account instead
of your subscription — `unset ANTHROPIC_API_KEY` first if unsure).

Each `claude -p "..."` call is a fresh, independent, tool-less turn (no
memory of prior calls) — the same "brand new chat" isolation the manual
workflow relies on for a fair determinism test.

Setup (once):
    1. Install Claude Code: npm install -g @anthropic-ai/claude-code
    2. Run `claude` once and sign in with your Claude.ai account (not an API key).
    3. unset ANTHROPIC_API_KEY   (only if you have one set — most people don't)

Usage:
    python3 run_battery.py                      # everything in the battery
    python3 run_battery.py --skill jira          # only Jira-Ticket-Writer inputs
    python3 run_battery.py --only J4 J5 J6       # only specific input codes
    python3 run_battery.py --runs 3              # runs per input (default 3)
    python3 run_battery.py --dry-run             # verify parsing, no Claude calls

Output: saves every run under runs/<code>-run<N>.md (also usable as your
Eval Log evidence), then prints one PASS/FAIL line per input and a summary.

Note: I can't execute-test this script myself (no Claude Code / your
subscription in this sandbox) — everything here is built from Anthropic's
current documented CLI behavior, but please try --dry-run first, then try
ONE input for real, before trusting a full 34-input run.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

BATTERY_FILE = "MASTER-TEST-BATTERY.md"
SKILL_FILES = {
    "J": "Jira-Ticket-Writer.md",
    "R": "Release-Notes-Writer.md",
    "P": "PR-Reviewer.md",
    "T": "Ticket-Tester.md",
}
SKILL_ALIASES = {
    "jira": "J", "release-notes": "R", "releasenotes": "R", "pr": "P",
    "pr-reviewer": "P", "ticket-tester": "T", "tickettester": "T",
}
FENCE = re.compile(r"```(?:[a-z]*)\n(.*?)```", re.DOTALL)
JSON_FENCE = re.compile(r"```json\s*\n(.*?)```", re.DOTALL)
HEADING = re.compile(r"^### ([A-Z]\d+) — [^\n]*$", re.MULTILINE)


def parse_battery(path: str):
    """Yield (code, skill_file, payload) for every '### <code> — ...' section."""
    text = Path(path).read_text(encoding="utf-8")
    marks = list(HEADING.finditer(text))
    for i, m in enumerate(marks):
        code = m.group(1)
        body = text[m.end(): marks[i + 1].start() if i + 1 < len(marks) else len(text)]
        fence = FENCE.search(body)
        if not fence:
            print(f"  ! {code}: no fenced payload found in its section — skipping")
            continue
        skill_file = SKILL_FILES.get(code[0])
        if not skill_file:
            print(f"  ! {code}: unrecognized prefix — skipping")
            continue
        yield code, skill_file, fence.group(1).rstrip()


def call_claude_code(prompt: str) -> str:
    """One fresh, isolated `claude -p` turn. Raises on failure."""
    result = subprocess.run(
        ["claude", "-p", prompt, "--output-format", "json"],
        capture_output=True, text=True, timeout=300,
    )
    if result.returncode != 0:
        raise RuntimeError(f"claude exited {result.returncode}: {result.stderr[:300]}")
    try:
        data = json.loads(result.stdout)
        return data.get("result", result.stdout)
    except json.JSONDecodeError:
        return result.stdout  # fall back to raw text if JSON parsing fails


def canon_manifest(output: str):
    blocks = JSON_FENCE.findall(output)
    if not blocks:
        return None, "no ```json manifest in output"
    try:
        return json.dumps(json.loads(blocks[-1]), sort_keys=True, indent=2), None
    except json.JSONDecodeError as e:
        return None, f"manifest not valid JSON: {e}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skill", choices=sorted(SKILL_ALIASES), help="only this skill's inputs")
    ap.add_argument("--only", nargs="+", help="only these input codes, e.g. J4 J5")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--battery", default=BATTERY_FILE)
    ap.add_argument("--dry-run", action="store_true", help="parse + print plan, no claude calls")
    args = ap.parse_args()

    if not args.dry_run and not shutil.which("claude"):
        sys.exit("ERROR: 'claude' not found on PATH. Install with:\n"
                  "  npm install -g @anthropic-ai/claude-code\n"
                  "then run `claude` once to sign in, then re-run this script.")

    prefix_filter = SKILL_ALIASES.get(args.skill) if args.skill else None
    inputs = list(parse_battery(args.battery))
    if prefix_filter:
        inputs = [i for i in inputs if i[0][0] == prefix_filter]
    if args.only:
        wanted = {c.upper() for c in args.only}
        inputs = [i for i in inputs if i[0] in wanted]
    if not inputs:
        sys.exit("No matching inputs found — check --skill/--only against " + args.battery)

    print(f"Plan: {len(inputs)} input(s) × {args.runs} run(s) = {len(inputs) * args.runs} Claude Code calls\n")
    if args.dry_run:
        for code, skill_file, payload in inputs:
            print(f"  {code:4s} -> {skill_file}  ({len(payload)} chars payload)")
        print("\n--dry-run: no calls made.")
        return

    outdir = Path("runs")
    outdir.mkdir(exist_ok=True)
    results = []

    for code, skill_file, payload in inputs:
        skill_path = Path(skill_file)
        if not skill_path.exists():
            print(f"{code}: ERROR — {skill_file} not found in this folder, skipping")
            results.append((code, skill_file, "ERROR", "skill file missing"))
            continue
        skill_text = skill_path.read_text(encoding="utf-8")
        print(f"{code} ({skill_file}):")
        manifests, errors = [], []
        for n in range(1, args.runs + 1):
            prompt = skill_text + "\n\n---\n\n" + payload
            try:
                output = call_claude_code(prompt)
            except Exception as e:
                print(f"  run {n}: CALL FAILED — {e}")
                errors.append(str(e)); manifests.append(None)
                continue
            run_path = outdir / f"{code}-run{n}.md"
            run_path.write_text(output, encoding="utf-8")
            canon, err = canon_manifest(output)
            manifests.append(canon)
            print(f"  run {n}: saved {run_path}" + (f" — {err}" if err else " — manifest OK"))
            if err:
                errors.append(err)

        good = [m for m in manifests if m]
        if good and all(m == good[0] for m in good) and len(good) == len(manifests):
            print(f"  {code}: PASS — {args.runs} runs decision-identical\n")
            results.append((code, skill_file, "PASS", ""))
        else:
            note = "; ".join(dict.fromkeys(errors)) if errors else "decisions drifted between runs"
            print(f"  {code}: FAIL — {note}\n")
            results.append((code, skill_file, "FAIL", note))

    print("=" * 60)
    print(f"{'CODE':6}{'SKILL':24}{'RESULT':8}NOTE")
    for code, skill_file, status, note in results:
        print(f"{code:6}{skill_file:24}{status:8}{note}")
    passed = sum(1 for r in results if r[2] == "PASS")
    print(f"\n{passed}/{len(results)} PASS. Saved outputs are in ./runs/ — use them as Eval Log evidence.")


if __name__ == "__main__":
    main()
