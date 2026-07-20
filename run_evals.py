#!/usr/bin/env python3
"""
run_evals.py — automated eval runner for the Invicta-One skill fleet.

For each fixture input, runs the skill N times against the Anthropic API
(fresh context every run, default sampling — the honest test), extracts the
decision manifest (the LAST ```json block) from each output, and verifies the
runs are decision-identical. Raw outputs are saved under runs/ so they double
as Eval Log evidence.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python3 run_evals.py Release-Notes-Writer.md test-inputs-release-notes.md
    python3 run_evals.py PR-Reviewer.md test-inputs-adversarial.md --runs 3
    python3 run_evals.py <skill> <fixtures> --dry-run     # verify plumbing, no API

Notes:
- Stdlib only; no packages to install.
- Fixture sections without their own fenced payload (e.g. "the ticket above,
  nothing else") are skipped with a warning — run those manually.
- Exit code 0 = every input decision-deterministic; 1 = drift or error.
"""

import argparse
import json
import os
import pathlib
import re
import sys
import urllib.request

API_URL = "https://api.anthropic.com/v1/messages"
FENCE_JSON = re.compile(r"```json\s*\n(.*?)```", re.DOTALL)
FENCE_ANY = re.compile(r"```[a-z]*\s*\n(.*?)```", re.DOTALL)
SECTION = re.compile(r"^## (Input \d+[^\n]*)$", re.MULTILINE)


def parse_fixtures(path: str):
    """Yield (label, payload) for each '## Input N' section's first fenced block."""
    text = pathlib.Path(path).read_text(encoding="utf-8")
    marks = list(SECTION.finditer(text))
    for i, m in enumerate(marks):
        body = text[m.end(): marks[i + 1].start() if i + 1 < len(marks) else len(text)]
        fence = FENCE_ANY.search(body)
        label = m.group(1).split("·")[0].split("—")[0].strip()
        if fence:
            yield label, fence.group(1).rstrip()
        else:
            print(f"  ! {label}: no fenced payload in its section — run this one manually")


def call_model(skill_text: str, payload: str, model: str) -> str:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("ERROR: set ANTHROPIC_API_KEY (or use --dry-run to test the plumbing)")
    body = json.dumps({
        "model": model,
        "max_tokens": 4096,
        "system": skill_text,
        "messages": [{"role": "user", "content": payload}],
    }).encode("utf-8")
    req = urllib.request.Request(API_URL, data=body, headers={
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return "\n".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")


def fake_model(skill_text: str, payload: str, model: str) -> str:
    """--dry-run responder: deterministic canned output to validate the pipeline."""
    return ("(dry run) skill and payload received.\n\n```json\n"
            + json.dumps({"skill": "dry-run", "payload_chars": len(payload)})
            + "\n```\n")


def manifest_of(output: str, where: str) -> str:
    blocks = FENCE_JSON.findall(output)
    if not blocks:
        raise ValueError(f"no ```json manifest in {where} — the skill must end with one")
    return json.dumps(json.loads(blocks[-1]), sort_keys=True, indent=2)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("skill")
    ap.add_argument("fixtures")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--model", default="claude-sonnet-4-6")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    skill_text = pathlib.Path(args.skill).read_text(encoding="utf-8")
    caller = fake_model if args.dry_run else call_model
    outdir = pathlib.Path("runs") / pathlib.Path(args.skill).stem
    outdir.mkdir(parents=True, exist_ok=True)

    failures = 0
    inputs = list(parse_fixtures(args.fixtures))
    if not inputs:
        sys.exit("ERROR: no runnable inputs found in the fixture file")

    for label, payload in inputs:
        slug = label.lower().replace(" ", "-")
        print(f"\n{label} — {args.runs} run(s):")
        manifests = []
        for n in range(1, args.runs + 1):
            output = caller(skill_text, payload, args.model)
            run_path = outdir / f"{slug}-run{n}.md"
            run_path.write_text(output, encoding="utf-8")
            try:
                manifests.append(manifest_of(output, run_path.name))
                print(f"  run {n}: saved {run_path} — manifest OK")
            except ValueError as e:
                print(f"  run {n}: FAIL — {e}")
                failures += 1
                manifests.append(None)
        good = [m for m in manifests if m]
        if good and all(m == good[0] for m in good) and len(good) == len(manifests):
            print(f"  {label}: PASS — {args.runs} runs decision-identical")
        else:
            failures += 1
            print(f"  {label}: FAIL — decisions drifted between runs "
                  f"(diff the saved files, tighten the drifting rule, re-run)")

    print("\n" + ("RESULT: PASS — paste this into the Eval Log with the runs/ paths"
                  if failures == 0 else f"RESULT: FAIL ({failures})"))
    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()
