"""Evaluator-visible integrity checks for the candidate Hugging Face artifact."""

from __future__ import annotations

import json
import re
import hashlib
from pathlib import Path


CANDIDATE = Path("candidate-space")
PAPER_SHA256 = "ca7631580c8a96ff440892fe1ab8d8b42edc84f0dc6eaaf990d404c75f47c7c7"
FIXED_COMMAND = "uv run --locked python -m reproduction.run_all"
CLAIM_STATUSES = {
    1: "VERIFIED",
    2: "BLOCKED",
    3: "VERIFIED",
    4: "VERIFIED",
    5: "FALSIFIED",
    6: "FALSIFIED",
}
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def logbook_files(node: dict[str, object]) -> list[str]:
    files = [str(node["file"])]
    for child in node.get("children", []):
        files.extend(logbook_files(child))
    return files


def local_markdown_links(path: Path) -> list[Path]:
    links: list[Path] = []
    for target in LINK_RE.findall(path.read_text(encoding="utf-8")):
        if target.startswith(("http://", "https://", "#")):
            continue
        clean = target.split("#", maxsplit=1)[0]
        if not clean:
            continue
        links.append((path.parent / clean).resolve())
    return links


def audit() -> dict[str, object]:
    logbook = json.loads((CANDIDATE / "logbook.json").read_text(encoding="utf-8"))
    assert logbook["space_id"] == "DineshAI/SGTLVjx3MN"
    navigation_files = logbook_files(logbook["root"])
    missing_navigation = [
        relative for relative in navigation_files if not (CANDIDATE / relative).is_file()
    ]
    if missing_navigation:
        raise AssertionError(f"missing navigation files: {missing_navigation}")

    claim_rows: list[dict[str, object]] = []
    for claim, status in CLAIM_STATUSES.items():
        page = CANDIDATE / f"pages/current-claim-{claim}/page.md"
        text = page.read_text(encoding="utf-8")
        required = [
            PAPER_SHA256,
            FIXED_COMMAND,
            status,
            "Evidence bundle:",
            "raw results",
            "checker output",
            "control output",
            "limitations",
            "Git SHA",
        ]
        missing = [item for item in required if item not in text]
        if missing:
            raise AssertionError(f"Claim {claim} page missing {missing}")
        raw = CANDIDATE / f"evidence/claim-{claim}/raw_results.json"
        parsed = json.loads(raw.read_text(encoding="utf-8"))
        if parsed["verdict"] != status:
            raise AssertionError(f"Claim {claim} raw verdict mismatch")
        claim_rows.append(
            {
                "claim": claim,
                "status": status,
                "page": str(page),
                "raw": str(raw),
                "required_items": "PASS",
            }
        )

    historical_pages = [
        "pages/overview/page.md",
        "pages/claim-1-lp-concentration/page.md",
        "pages/claim-4-5-6/page.md",
        "pages/methods/page.md",
        "pages/conclusion/page.md",
    ]
    if not all((CANDIDATE / path).is_file() for path in historical_pages):
        raise AssertionError("a historical judged evidence page is missing")

    broken_links: list[dict[str, str]] = []
    markdown_files = sorted(CANDIDATE.rglob("*.md"))
    for markdown in markdown_files:
        for resolved in local_markdown_links(markdown):
            if not resolved.exists():
                broken_links.append(
                    {"source": str(markdown), "missing_target": str(resolved)}
                )
    if broken_links:
        raise AssertionError(f"broken local Markdown links: {broken_links[:10]}")

    allowlist_path = CANDIDATE / "evidence/release/text-upload-allowlist.txt"
    allowlist = {
        line.strip()
        for line in allowlist_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    actual_files = {
        str(path.relative_to(CANDIDATE))
        for path in CANDIDATE.rglob("*")
        if path.is_file()
    }
    if allowlist != actual_files:
        raise AssertionError(
            "upload allowlist mismatch: "
            f"missing={sorted(actual_files - allowlist)}, "
            f"extra={sorted(allowlist - actual_files)}"
        )

    manifest_path = CANDIDATE / "evidence/release/candidate-manifest.sha256"
    manifest_entries = 0
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split(maxsplit=1)
        relative = relative.lstrip("*")
        target = CANDIDATE / relative
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(f"manifest mismatch: {relative}")
        manifest_entries += 1

    secret_scan = (
        CANDIDATE / "evidence/release/secret-scan.txt"
    ).read_text(encoding="utf-8")
    if "SECRET_SCAN_STATUS=PASS" not in secret_scan:
        raise AssertionError("secret scan has not passed")

    red_team = (
        CANDIDATE / "evidence/release/red-team-review.md"
    ).read_text(encoding="utf-8")
    if "POST_FIX_REVIEW_STATUS=PASS" not in red_team:
        raise AssertionError("post-fix blind review has not passed")

    gates = json.loads(
        (CANDIDATE / "evidence/release/release-gates.json").read_text(
            encoding="utf-8"
        )
    )
    if gates["publication_status"] != "READY_FOR_CUMULATIVE_RUN":
        raise AssertionError("release gates are not ready for cumulative run")

    return {
        "status": "PASS",
        "space_id": logbook["space_id"],
        "navigation_files": len(navigation_files),
        "markdown_files_checked": len(markdown_files),
        "broken_links": 0,
        "claim_rows": claim_rows,
        "historical_judged_pages_preserved": len(historical_pages),
        "upload_allowlist_files": len(allowlist),
        "manifest_entries_verified": manifest_entries,
        "secret_scan": "PASS",
        "post_fix_blind_review": "PASS",
        "fixed_command": FIXED_COMMAND,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
