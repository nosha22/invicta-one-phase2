# Test plan — Split SEPA export files above the bank size limit

| ID | Title | Kind | Source |
|---|---|---|---|
| TC-1 | Export exceeding 8MB is split into multiple files | stated | Scenario 1 |
| TC-2 | User sees the number of files generated | stated | Scenario 2 |
| TC-3 | Export just under 8MB (7.9MB) handling | derived | Boundary: 8MB limit |
| TC-4 | Export at exactly 8MB behavior | derived | Boundary: 8MB limit |
| TC-5 | Export just over 8MB (8.1MB) is split | derived | Boundary: 8MB limit |
| TC-6 | Export of an empty batch shows appropriate message | exploratory | Proposed Scenario A |
| TC-7 | Multiple files use the naming convention | derived | Q1 (assumed — confirm) |

## Cases

### TC-1 — Export exceeding 8MB is split into multiple files [stated]
- Source: Scenario 1
- Preconditions: An invoice batch exists whose SEPA export would exceed 8MB when rendered
- Steps:
  1. Select the invoice batch
  2. Trigger the export function
  3. Observe the output
- Expected result: The export produces multiple files, each with a size ≤ 8MB (per Scenario 1)

### TC-2 — User sees the number of files generated [stated]
- Source: Scenario 2
- Preconditions: An export has been split into multiple files (e.g., from TC-1)
- Steps:
  1. Observe the UI after export completes
- Expected result: The UI displays the count of files generated (e.g., "Export split into 3 files")

### TC-3 — Export just under 8MB (7.9MB) handling [derived]
- Source: Boundary derived from "8MB" limit in Scenario 1
- Preconditions: An invoice batch whose SEPA export is 7.9MB
- Steps:
  1. Select the batch
  2. Trigger export
  3. Observe the output file(s)
- Expected result: (expected: single file without split — confirm)

### TC-4 — Export at exactly 8MB behavior [derived]
- Source: Boundary derived from "8MB" limit in Scenario 1
- Preconditions: An invoice batch whose SEPA export is exactly 8.0MB
- Steps:
  1. Select the batch
  2. Trigger export
  3. Observe the output file(s)
- Expected result: (expected per limit — confirm whether exactly 8MB triggers split or remains as single file)

### TC-5 — Export just over 8MB (8.1MB) is split [derived]
- Source: Boundary derived from "8MB" limit in Scenario 1
- Preconditions: An invoice batch whose SEPA export is 8.1MB (just over the 8MB limit)
- Steps:
  1. Select the batch
  2. Trigger export
  3. Count output files and verify each file size
- Expected result: Multiple files produced, each ≤ 8MB (per Scenario 1 — exceeds threshold behavior)

### TC-6 — Export of an empty batch shows appropriate message [exploratory]
- Source: Proposed Scenario A (unconfirmed requirement)
- Preconditions: An invoice batch with zero invoices
- Steps:
  1. Select the empty batch
  2. Trigger export
- Expected result: (exploratory — expected behavior not yet confirmed; proposed: user sees a message indicating there is nothing to export)

### TC-7 — Multiple files use the naming convention [derived]
- Source: Q1 (assumed — confirm) — "sequential suffixes _part1, _part2"
- Preconditions: An export split into multiple files (export exceeds 8MB)
- Steps:
  1. Export a batch that exceeds 8MB
  2. Inspect the generated file names
- Expected result: (expected: files are named with sequential suffixes such as _part1, _part2, etc. — confirm naming convention with finance)

## Traceability check
Stated scenarios covered: 2/2 ✓ · Every case carries a Source ✓

## Decision manifest (machine-readable)
```json
{"skill": "ticket-tester", "mode": "test-plan", "stated_cases": 2, "traceability": "2/2"}
```
