#!/usr/bin/env python3
"""Validate sprint documents and progress state, not simulator/scientific correctness."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPRINT_DIR = ROOT / "docs" / "sprints"
PROGRESS_FILE = ROOT / "docs" / "STATE" / "PROGRESS.json"
REQUIRED = (
    "## Objective", "## Scope", "## Prerequisites", "## Execution steps",
    "## Deliverables", "## White-box tests", "## Black-box tests",
    "## Adversarial/negative tests", "## Acceptance criteria",
    "## Evidence record", "## Failure handling and rollback",
    "## Stop conditions", "## Handoff",
)
STATUSES = {"not_started", "in_progress", "blocked", "in_review", "completed"}

def main() -> int:
    errors: list[str] = []
    try:
        state = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot read progress JSON: {exc}", file=sys.stderr)
        return 1
    if state.get("total_sprints") != 88:
        errors.append("total_sprints must equal 88")
    items = state.get("sprints")
    if not isinstance(items, list) or len(items) != 88:
        errors.append("sprints must contain exactly 88 records")
        items = items if isinstance(items, list) else []
    expected = [f"S{i:03d}" for i in range(1, 89)]
    ids = [x.get("id") for x in items if isinstance(x, dict)]
    if ids != expected:
        errors.append("progress IDs must be ordered S001 through S088")
    by_id = {x.get("id"): x for x in items if isinstance(x, dict)}
    paths = sorted(SPRINT_DIR.glob("S[0-9][0-9][0-9]-*.md"))
    if len(paths) != 88:
        errors.append(f"expected 88 sprint files, found {len(paths)}")
    path_ids = [m.group(1) for p in paths if (m := re.match(r"(S\d{3})-", p.name))]
    if sorted(path_ids) != expected:
        errors.append("sprint filenames must uniquely cover S001-S088")
    for path in paths:
        text = path.read_text(encoding="utf-8")
        match = re.match(r"(S\d{3})-", path.name)
        sid = match.group(1) if match else "UNKNOWN"
        for heading in REQUIRED:
            if heading not in text:
                errors.append(f"{path}: missing {heading}")
        item = by_id.get(sid)
        if item is None:
            errors.append(f"{sid}: missing progress record")
            continue
        if item.get("file") != str(path.relative_to(ROOT)):
            errors.append(f"{sid}: progress path mismatch")
        if item.get("status") not in STATUSES:
            errors.append(f"{sid}: invalid status")
        expected_dep = [] if sid == "S001" else [f"S{int(sid[1:])-1:03d}"]
        if item.get("depends_on") != expected_dep:
            errors.append(f"{sid}: must depend on immediate predecessor")
    for required in ("AGENTS.md", "docs/SPRINT_INDEX.md", "docs/STATE/AGENT_HANDOFF.md",
                     "docs/STATE/BLOCKERS.md", "docs/STATE/DECISION_LOG.md",
                     "docs/STATE/VALIDATION_LOG.md"):
        if not (ROOT / required).is_file():
            errors.append(f"missing governance file: {required}")
    if state.get("current_sprint_id") not in by_id:
        errors.append("unknown current_sprint_id")
    if state.get("next_sprint_id") not in by_id:
        errors.append("unknown next_sprint_id")
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        print(f"Documentation validation failed: {len(errors)} issue(s).", file=sys.stderr)
        return 1
    print("PASS: 88 sprint files, sequential dependencies, progress JSON, and governance files are consistent.")
    print("NOTE: documentation consistency does not prove simulator correctness or scientific validity.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
