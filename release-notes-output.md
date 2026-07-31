# Release Notes — <Product> <version> (2026-07-28)

This release includes 1 new feature, 1 improvement, and 1 fix.

## New features
- **Bulk project archiving** — projects can now be archived in bulk instead of one at a time. (APP-201)

## Improvements
- **Updated privacy policy link** — the privacy policy link in the footer now points to the correct page. (APP-190)

## Fixes
- **Large file upload crash fixed** — uploading files larger than 2GB no longer crashes the application. (APP-203)

---

### Needs review (not published — human decision required)
(none)

### Internal changes (excluded from client-facing notes)
- OPS-12 — Migrate CI runners to new cluster — `internal`
- APP-207 — Redesign settings page — `not-shipped`

### Coverage check
Input entries: 5 → published 3 · excluded 2 · needs review 0  →  3+2+0 = 5 ✓

### Decision manifest (machine-readable)
```json
{
  "skill": "release-notes-writer",
  "coverage": {"input": 5, "published": 3, "excluded": 2, "needs_review": 0},
  "decisions": {
    "OPS-12": "excluded:internal",
    "APP-201": "published:new-features",
    "APP-203": "published:fixes",
    "APP-207": "excluded:not-shipped",
    "APP-190": "published:improvements"
  }
}
```
