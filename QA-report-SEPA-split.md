# QA report — Split SEPA export files above the bank size limit

## Bugs

### [Bug] Second export file is empty when batch exceeds 8MB

**Environment:**
- Staging

**Steps to reproduce:**
1. Create an invoice batch whose SEPA export exceeds 8MB (tested: 12MB)
2. Export the batch

**Expected:**
Export is split into multiple files, each at most 8MB, with valid SEPA data (Scenario 1).

**Actual:**
Two files are produced; the second file is 0 bytes.

**Evidence:**
> 12MB invoice batch -> got 2 files but the second file is 0 bytes??

**Severity:**
Blocker — the export data that should exist in the second file is missing. Data loss on the main path.

**Suspected area:**
File-splitting logic; stream/writer may be dropping buffered data on handoff between files (hypothesis — not verified).

**Ready to file:**
YES

---

## Requirement gaps (for the Product Owner)

- **File naming convention mismatch:** Observed naming `export_1.xml` / `export_2.xml`; the open question Q1 flags the assumed convention as `_part1` / `_part2` suffix "(assumed — confirm with finance)". **Question:** Does the finance team require the `_partN` format, or is the current numbering scheme acceptable?

- **Export performance:** A 12MB batch export caused a 30-second UI freeze. Scenario 1 states no performance target. **Question:** Should the export complete within a specific time window, or should the UI remain responsive during export (e.g., with a progress indicator)? Define the performance baseline before proceeding.

---

## Observations

- **Happy path validated:** A 7MB batch exported successfully to a single file and validated correctly in the bank portal, confirming the core functionality works for batches under the 8MB limit.

---

## Coverage cross-check

| Scenario | Tested? | Notes |
|---|---|---|
| Scenario 1: Export exceeding the size limit is split | YES | 12MB batch triggered the split logic; revealed the 0-byte second file defect |
| Scenario 2: User sees how many files were generated | NO | No evidence provided of UI testing for the file-count completion message |

---

### Decision manifest (machine-readable)
```json
{
  "skill": "ticket-tester",
  "mode": "bug-report",
  "classified": {
    "bugs": 1,
    "requirement_gaps": 2
  },
  "bugs": [
    {
      "id": "BUG-1",
      "severity": "Blocker",
      "ready_to_file": true
    }
  ]
}
```
