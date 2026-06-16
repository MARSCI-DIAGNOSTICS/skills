#!/usr/bin/env python3
"""
Report generator for social intelligence state files.

Reads JSONL data and produces markdown summary reports.

Usage:
    python generate_report.py [--since YYYY-MM-DD] [--status STATUS] [--format markdown|json] [--save]

Environment:
    CLAUDE_X_SCAN_DEV_ROOT: Override data directory (dev mode)
    CLAUDE_PROJECT_DIR: Project root for data directory resolution
"""
import sys
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


def _get_data_dir() -> Path:
    """Resolve the data directory for social intelligence state files."""
    dev_root = os.environ.get("CLAUDE_X_SCAN_DEV_ROOT")
    if dev_root:
        return Path(dev_root) / ".claude" / "social-intelligence" / "data"
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    return Path(project_dir) / ".claude" / "social-intelligence" / "data"


def _get_reports_dir() -> Path:
    """Resolve the reports directory."""
    dev_root = os.environ.get("CLAUDE_X_SCAN_DEV_ROOT")
    if dev_root:
        return Path(dev_root) / ".claude" / "social-intelligence" / "reports"
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    return Path(project_dir) / ".claude" / "social-intelligence" / "reports"


def _read_jsonl(file_path: Path) -> List[Dict[str, Any]]:
    """Read all entries from a JSONL file."""
    entries: List[Dict[str, Any]] = []
    if not file_path.exists():
        return entries
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries


def _filter_by_date(entries: List[Dict[str, Any]], since: Optional[str]) -> List[Dict[str, Any]]:
    """Filter entries by timestamp >= since date. Checks both timestamp and posted_at."""
    if not since:
        return entries
    return [
        e for e in entries
        if max(e.get("timestamp", ""), e.get("posted_at", "")) >= since
    ]


def _filter_by_status(entries: List[Dict[str, Any]], status: Optional[str]) -> List[Dict[str, Any]]:
    """Filter entries by status field."""
    if not status or status == "all":
        return entries
    return [e for e in entries if e.get("status", "") == status]


def _post_text(post: Dict[str, Any]) -> str:
    """Get post text content with fallback for schema variants."""
    return post.get("text", post.get("content_text", ""))


def _post_category(post: Dict[str, Any]) -> str:
    """Get post category with fallback for schema variants."""
    return post.get("category", post.get("relevance_category", "general"))


def _insight_areas(insight: Dict[str, Any]) -> List[str]:
    """Get insight areas with fallback for schema variants."""
    return insight.get("areas", insight.get("affected_areas", []))


def _insight_action(insight: Dict[str, Any]) -> str:
    """Get suggested action as a string, handling both v1 and v2 formats."""
    # v2: action_suggested is a string
    action = insight.get("action_suggested")
    if action:
        action_type = insight.get("action_type", "")
        if action_type:
            return f"[{action_type}] {action}"
        return action
    # v1: suggested_actions is an array of objects
    suggested = insight.get("suggested_actions", [])
    if isinstance(suggested, list) and suggested:
        first = suggested[0]
        if isinstance(first, dict):
            return f"[{first.get('type', 'unknown')}] {first.get('description', '')}"
        if isinstance(first, str):
            return first
    return ""


def generate_markdown_report(
    scans: List[Dict[str, Any]],
    posts: List[Dict[str, Any]],
    insights: List[Dict[str, Any]],
    actions: List[Dict[str, Any]],
    since: Optional[str] = None,
) -> str:
    """Generate a markdown summary report."""
    lines: List[str] = []
    lines.append("# Social Intelligence Report")
    lines.append("")

    if since:
        lines.append(f"**Since:** {since}")
    lines.append(f"**Scans:** {len(scans)} | **Posts:** {len(posts)} | **Insights:** {len(insights)} | **Actions:** {len(actions)}")
    lines.append("")

    # Scan summary
    if scans:
        lines.append("## Recent Scans")
        lines.append("")
        for scan in scans[-5:]:
            scan_id = scan.get("scan_id", "unknown")
            ts = scan.get("timestamp", "unknown")
            new = scan.get("new_posts", 0)
            relevant = scan.get("relevant_posts", 0)
            total = scan.get("posts_found", 0)
            lines.append(f"- **{scan_id}** ({ts}): {total} found, {new} new, {relevant} relevant")
        lines.append("")

    # High-relevance posts
    relevant_posts = sorted(
        [p for p in posts if p.get("relevance_score", 0) >= 0.4],
        key=lambda p: p.get("relevance_score", 0),
        reverse=True,
    )
    if relevant_posts:
        lines.append("## Relevant Posts")
        lines.append("")
        for post in relevant_posts[:25]:
            author = post.get("author_handle", "unknown")
            score = post.get("relevance_score", 0)
            category = _post_category(post)
            content = _post_text(post)[:120]
            post_id = post.get("post_id", "")
            url = post.get("url", "")
            status = post.get("status", "new")
            lines.append(f"### {author} ({category}, score: {score:.2f}) [{status}]")
            lines.append(f"> {content}...")
            if url:
                lines.append(f"[View on X]({url})")
            elif post_id:
                lines.append(f"Post ID: {post_id}")
            lines.append("")

    # Pending insights
    pending_insights = [i for i in insights if i.get("status") == "pending_review"]
    if pending_insights:
        lines.append("## Pending Insights")
        lines.append("")
        for insight in pending_insights:
            iid = insight.get("insight_id", "unknown")
            summary = insight.get("summary", "")
            confidence = insight.get("confidence", 0)
            areas = ", ".join(_insight_areas(insight))
            lines.append(f"### {iid} (confidence: {confidence:.2f})")
            lines.append(f"**Summary:** {summary}")
            if areas:
                lines.append(f"**Areas:** {areas}")
            action = _insight_action(insight)
            if action:
                lines.append(f"**Suggested action:** {action}")
            lines.append("")

    # Pending actions
    pending_actions = [a for a in actions if a.get("status") == "proposed"]
    if pending_actions:
        lines.append("## Proposed Actions")
        lines.append("")
        for action in pending_actions:
            aid = action.get("action_id", "unknown")
            atype = action.get("action_type", "unknown")
            desc = action.get("description", "")
            target = action.get("target_path", "")
            lines.append(f"- **{aid}** [{atype}]: {desc}")
            if target:
                lines.append(f"  Target: `{target}`")
        lines.append("")

    # No data message
    if not scans and not posts and not insights:
        lines.append("No data found. Run `/claude-ecosystem:social-intelligence scan` to start scanning.")
        lines.append("")

    return "\n".join(lines)


def generate_json_report(
    scans: List[Dict[str, Any]],
    posts: List[Dict[str, Any]],
    insights: List[Dict[str, Any]],
    actions: List[Dict[str, Any]],
) -> str:
    """Generate a JSON summary report."""
    report = {
        "summary": {
            "total_scans": len(scans),
            "total_posts": len(posts),
            "total_insights": len(insights),
            "total_actions": len(actions),
            "pending_insights": len([i for i in insights if i.get("status") == "pending_review"]),
            "proposed_actions": len([a for a in actions if a.get("status") == "proposed"]),
        },
        "recent_scans": scans[-5:],
        "relevant_posts": sorted(
            [p for p in posts if p.get("relevance_score", 0) >= 0.4],
            key=lambda p: p.get("relevance_score", 0),
            reverse=True,
        )[:25],
        "pending_insights": [i for i in insights if i.get("status") == "pending_review"],
        "proposed_actions": [a for a in actions if a.get("status") == "proposed"],
    }
    return json.dumps(report, indent=2, ensure_ascii=False)


def main() -> None:
    since: Optional[str] = None
    status: Optional[str] = None
    fmt = "markdown"
    save = False

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--since" and i + 1 < len(sys.argv):
            since = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--status" and i + 1 < len(sys.argv):
            status = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--format" and i + 1 < len(sys.argv):
            fmt = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--save":
            save = True
            i += 1
        else:
            i += 1

    data_dir = _get_data_dir()

    scans = _filter_by_date(_read_jsonl(data_dir / "scan-log.jsonl"), since)
    posts = _filter_by_status(_filter_by_date(_read_jsonl(data_dir / "posts-index.jsonl"), since), status)
    insights = _filter_by_status(_filter_by_date(_read_jsonl(data_dir / "insights-log.jsonl"), since), status)
    actions = _filter_by_status(_filter_by_date(_read_jsonl(data_dir / "actions-log.jsonl"), since), status)

    if fmt == "json":
        output = generate_json_report(scans, posts, insights, actions)
    else:
        output = generate_markdown_report(scans, posts, insights, actions, since=since)

    print(output)

    if save:
        reports_dir = _get_reports_dir()
        reports_dir.mkdir(parents=True, exist_ok=True)
        ts = time.strftime("%Y%m%d-%H%M%S", time.gmtime())
        ext = "json" if fmt == "json" else "md"
        report_path = reports_dir / f"report-{ts}.{ext}"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\nReport saved to: {report_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
