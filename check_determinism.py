#!/usr/bin/env python3
"""
check_determinism.py — automated determinism proof for the Invicta-One skill fleet.

Every skill in this fleet ends its output with a "decision manifest": the LAST
```json fenced block in the output. Wording may vary between runs of an LLM;
decisions may not. This script extracts the manifest from two or more saved
run outputs and verifies they are identical after canonicalization (sorted
keys), which is exactly the "outputs remained deterministic" proof the Phase 2
Eval Log requires.

Usage:
    python check_determinism.py run1.md run2.md [run3.md ...]

Exit code: 0 = PASS (all manifests decision-identical), 1 = FAIL or error.
Paste the printed result into the skill's Eval Log.
"""

import difflib
import json
import re
import sys

FENCE = re.compile(r"```json\s*\n(.*?)```", re.DOTALL)


def load_manifest(path: str) -> str:
    """Return the canonical (sorted-keys) JSON of the last ```json block in the file."""
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        sys.exit(f"ERROR: cannot read {path}: {e}")

    blocks = FENCE.findall(text)
    if not blocks:
        sys.exit(
            f"ERROR: no ```json manifest block found in {path} — "
            "did the skill emit its decision manifest?"
        )
    try:
        data = json.loads(blocks[-1])
    except json.JSONDecodeError as e:
        sys.exit(f"ERROR: last json block in {path} is not valid JSON: {e}")

    return json.dumps(data, sort_keys=True, indent=2)


def main(argv: list[str]) -> None:
    if len(argv) < 3:
        sys.exit(__doc__)

    paths = argv[1:]
    manifests = {p: load_manifest(p) for p in paths}
    ref_path, ref = paths[0], manifests[paths[0]]

    print(f"Reference manifest: {ref_path}")
    ok = True
    for p in paths[1:]:
        if manifests[p] == ref:
            print(f"  {p}: OK — decisions identical")
        else:
            ok = False
            print(f"  {p}: DIFF — decisions changed between runs:")
            diff = difflib.unified_diff(
                ref.splitlines(), manifests[p].splitlines(),
                fromfile=ref_path, tofile=p, lineterm="",
            )
            for line in diff:
                print(f"    {line}")

    print()
    if ok:
        print(f"RESULT: PASS — {len(paths)} runs are decision-deterministic")
    else:
        print("RESULT: FAIL — tighten the skill's decision rules and re-run")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main(sys.argv)
