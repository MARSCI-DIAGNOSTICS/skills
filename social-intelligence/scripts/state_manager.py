#!/usr/bin/env python3
"""
State manager for social intelligence JSONL data files.

Cross-platform file locking ported from hook_dispatcher.py.
Provides read/write/dedup/migrate for scan-log, posts-index, insights-log, actions-log.

Usage:
    python state_manager.py append <file> <json_line>
    python state_manager.py read <file> [--since YYYY-MM-DD] [--status STATUS] [--limit N]
    python state_manager.py next-seq
    python state_manager.py dedup-check <post_id>
    python state_manager.py dedup-check-batch <post_id1> <post_id2> ...
    python state_manager.py migrate
    python state_manager.py update <file> <key_field> <key_value> <json_patch>
    python state_manager.py compact <file>
    python state_manager.py last-scanned <handle> [<iso_timestamp>]
    python state_manager.py stats
    python state_manager.py init

Environment:
    CLAUDE_X_SCAN_DEV_ROOT: Override data directory (dev mode)
    CLAUDE_PROJECT_DIR: Project root for data directory resolution
"""
import sys
import json
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

if sys.version_info < (3, 6):
    sys.exit(0)

# Platform-specific file locking
if sys.platform == "win32":
    try:
        import msvcrt
    except ImportError:
        msvcrt = None  # type: ignore[assignment]
    fcntl = None  # type: ignore[assignment]
else:
    try:
        import fcntl
    except ImportError:
        fcntl = None  # type: ignore[assignment]
    msvcrt = None  # type: ignore[assignment]

# Path to accounts.json (resolved relative to this script)
_SCRIPT_DIR = Path(__file__).resolve().parent
_ACCOUNTS_JSON = _SCRIPT_DIR.parent / "config" / "accounts.json"


def _get_data_dir() -> Path:
    """Resolve the data directory for social intelligence state files."""
    dev_root = os.environ.get("CLAUDE_X_SCAN_DEV_ROOT")
    if dev_root:
        data_dir = Path(dev_root) / ".claude" / "social-intelligence" / "data"
    else:
        project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
        data_dir = Path(project_dir) / ".claude" / "social-intelligence" / "data"
    return data_dir


def _ensure_data_dir(data_dir: Path) -> None:
    """Create data directory if it doesn't exist."""
    data_dir.mkdir(parents=True, exist_ok=True)


def _locked_append(file_path: Path, line: str) -> None:
    """
    Append a line to a file with cross-platform file locking.

    - Windows: msvcrt.locking on a .lock sentinel file with retry (max 2s, 5ms sleep)
    - Unix: fcntl.flock(LOCK_EX) on the target file (blocking, auto-release on close)
    - Fallback: bare write if locking unavailable or fails
    """
    try:
        if sys.platform == "win32" and msvcrt is not None:
            lock_path = str(file_path) + ".lock"
            lock_fd = os.open(lock_path, os.O_CREAT | os.O_RDWR)
            locked = False
            try:
                for _ in range(400):  # 400 * 5ms = 2s max wait
                    try:
                        msvcrt.locking(lock_fd, msvcrt.LK_NBLCK, 1)
                        locked = True
                        break
                    except (OSError, IOError):
                        time.sleep(0.005)
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write(line)
            finally:
                if locked:
                    try:
                        os.lseek(lock_fd, 0, os.SEEK_SET)
                        msvcrt.locking(lock_fd, msvcrt.LK_UNLCK, 1)
                    except (OSError, IOError):
                        pass
                os.close(lock_fd)
        elif fcntl is not None:
            with open(file_path, "a", encoding="utf-8") as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                f.write(line)
        else:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(line)
    except Exception:
        try:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(line)
        except Exception:
            pass


def _next_seq(data_dir: Path) -> int:
    """
    Get next monotonic sequence number from {data_dir}/.seq file.

    Uses file locking to ensure uniqueness across concurrent processes.
    Returns 0 if counter cannot be read/written.
    """
    seq_file = data_dir / ".seq"
    try:
        fd = os.open(str(seq_file), os.O_CREAT | os.O_RDWR)
        try:
            if sys.platform == "win32" and msvcrt is not None:
                for _ in range(400):
                    try:
                        msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
                        break
                    except (OSError, IOError):
                        time.sleep(0.005)
            elif fcntl is not None:
                fcntl.flock(fd, fcntl.LOCK_EX)

            data = os.read(fd, 20).strip()
            try:
                seq = int(data) + 1 if data else 1
            except ValueError:
                seq = 1

            os.lseek(fd, 0, os.SEEK_SET)
            os.ftruncate(fd, 0)
            os.write(fd, str(seq).encode())

            return seq
        finally:
            if sys.platform == "win32" and msvcrt is not None:
                try:
                    os.lseek(fd, 0, os.SEEK_SET)
                    msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
                except (OSError, IOError):
                    pass
            os.close(fd)
    except Exception:
        return 0


def _read_jsonl(file_path: Path) -> List[Dict[str, Any]]:
    """Read all entries from a JSONL file."""
    entries = []
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


def _write_jsonl(file_path: Path, entries: List[Dict[str, Any]]) -> None:
    """Overwrite a JSONL file with the given entries."""
    with open(file_path, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _extract_numeric_id(post_id: str) -> Optional[str]:
    """Extract the X numeric post ID from any post_id format.

    Handles:
      - "bcherny-1893456789012345678" -> "1893456789012345678"
      - "1893456789012345678" -> "1893456789012345678"
      - "@bcherny-1893456789012345678" -> "1893456789012345678"
    """
    match = re.search(r"(\d{15,25})$", post_id)
    return match.group(1) if match else None


def _normalize_post(entry: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize a post entry from any schema variant to canonical v2.

    Field renames:
      content_text -> text
      relevance_category -> category
      affected_areas -> areas

    Constructs url from author_handle + numeric post ID if missing.
    Ensures posted_at is present (falls back to timestamp).
    """
    out = dict(entry)

    # Rename content_text -> text
    if "content_text" in out and "text" not in out:
        out["text"] = out.pop("content_text")
    elif "content_text" in out and "text" in out:
        del out["content_text"]

    # Rename relevance_category -> category
    if "relevance_category" in out and "category" not in out:
        out["category"] = out.pop("relevance_category")
    elif "relevance_category" in out and "category" in out:
        del out["relevance_category"]

    # Rename affected_areas -> areas
    if "affected_areas" in out and "areas" not in out:
        out["areas"] = out.pop("affected_areas")
    elif "affected_areas" in out and "areas" in out:
        del out["affected_areas"]

    # Ensure posted_at exists
    if "posted_at" not in out and "timestamp" in out:
        out["posted_at"] = out["timestamp"]

    # Construct url if missing
    if "url" not in out:
        handle = out.get("author_handle", "")
        pid = out.get("post_id", "")
        numeric = _extract_numeric_id(pid)
        if handle and numeric:
            clean_handle = handle.lstrip("@")
            out["url"] = f"https://x.com/{clean_handle}/status/{numeric}"

    # Normalize post_id to {handle}-{numeric} format
    pid = out.get("post_id", "")
    numeric = _extract_numeric_id(pid)
    if numeric and "-" not in pid:
        handle = out.get("author_handle", "").lstrip("@")
        if handle:
            out["post_id"] = f"{handle}-{numeric}"

    # Ensure defaults
    out.setdefault("status", "new")
    out.setdefault("relevance_score", 0.0)
    out.setdefault("category", "general")
    out.setdefault("areas", [])

    return out


def _normalize_insight(entry: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize an insight entry from any schema variant to canonical v2.

    Field renames:
      affected_areas -> areas
      source_posts -> source_post_ids

    Flattens suggested_actions array to action_suggested string + action_type string.
    """
    out = dict(entry)

    # Rename affected_areas -> areas
    if "affected_areas" in out and "areas" not in out:
        out["areas"] = out.pop("affected_areas")
    elif "affected_areas" in out and "areas" in out:
        del out["affected_areas"]

    # Rename source_posts -> source_post_ids
    if "source_posts" in out and "source_post_ids" not in out:
        out["source_post_ids"] = out.pop("source_posts")
    elif "source_posts" in out and "source_post_ids" in out:
        del out["source_posts"]

    # Flatten suggested_actions array to action_suggested + action_type
    if "suggested_actions" in out and "action_suggested" not in out:
        actions = out.pop("suggested_actions")
        if isinstance(actions, list) and actions:
            first = actions[0]
            if isinstance(first, dict):
                out["action_suggested"] = first.get("description", "")
                out["action_type"] = first.get("type", "")
            elif isinstance(first, str):
                out["action_suggested"] = first
        elif isinstance(actions, str):
            out["action_suggested"] = actions
    elif "suggested_actions" in out and "action_suggested" in out:
        del out["suggested_actions"]

    # Ensure defaults
    out.setdefault("status", "pending_review")
    out.setdefault("confidence", 0.0)
    out.setdefault("areas", [])
    out.setdefault("source_post_ids", [])

    return out


def _filter_entries(
    entries: List[Dict[str, Any]],
    since: Optional[str] = None,
    status: Optional[str] = None,
    limit: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Filter JSONL entries by date, status, and limit."""
    result = entries

    if since:
        result = [
            e for e in result
            if max(e.get("timestamp", ""), e.get("posted_at", "")) >= since
        ]

    if status:
        result = [
            e for e in result
            if e.get("status", "") == status
        ]

    if limit and limit > 0:
        result = result[-limit:]

    return result


def cmd_init() -> None:
    """Initialize the data directory and empty JSONL files."""
    data_dir = _get_data_dir()
    _ensure_data_dir(data_dir)

    files = ["scan-log.jsonl", "posts-index.jsonl", "insights-log.jsonl", "actions-log.jsonl"]
    for fname in files:
        fpath = data_dir / fname
        if not fpath.exists():
            fpath.touch()

    seq_file = data_dir / ".seq"
    if not seq_file.exists():
        with open(seq_file, "w", encoding="utf-8") as f:
            f.write("0")

    # Create reports directory
    reports_dir = data_dir.parent / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    print(json.dumps({"status": "ok", "data_dir": str(data_dir), "files": files}))


def cmd_append(file_name: str, json_line: str) -> None:
    """Append a JSON line to a state file, auto-normalizing to v2 schema."""
    data_dir = _get_data_dir()
    _ensure_data_dir(data_dir)

    valid_files = ["scan-log.jsonl", "posts-index.jsonl", "insights-log.jsonl", "actions-log.jsonl"]
    if file_name not in valid_files:
        print(json.dumps({"error": f"Invalid file: {file_name}. Valid: {valid_files}"}))
        sys.exit(1)

    try:
        entry = json.loads(json_line)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}))
        sys.exit(1)

    # Auto-normalize on write
    if file_name == "posts-index.jsonl":
        entry = _normalize_post(entry)
    elif file_name == "insights-log.jsonl":
        entry = _normalize_insight(entry)

    seq = _next_seq(data_dir)
    entry["seq"] = seq

    line = json.dumps(entry, ensure_ascii=False) + "\n"
    file_path = data_dir / file_name
    _locked_append(file_path, line)

    print(json.dumps({"status": "ok", "seq": seq, "file": file_name}))


def cmd_read(file_name: str, since: Optional[str] = None, status: Optional[str] = None, limit: Optional[int] = None) -> None:
    """Read and filter entries from a state file."""
    data_dir = _get_data_dir()

    valid_files = ["scan-log.jsonl", "posts-index.jsonl", "insights-log.jsonl", "actions-log.jsonl"]
    if file_name not in valid_files:
        print(json.dumps({"error": f"Invalid file: {file_name}. Valid: {valid_files}"}))
        sys.exit(1)

    file_path = data_dir / file_name
    entries = _read_jsonl(file_path)
    filtered = _filter_entries(entries, since=since, status=status, limit=limit)

    print(json.dumps({"status": "ok", "count": len(filtered), "entries": filtered}, ensure_ascii=False))


def cmd_next_seq() -> None:
    """Get the next sequence number."""
    data_dir = _get_data_dir()
    _ensure_data_dir(data_dir)
    seq = _next_seq(data_dir)
    print(json.dumps({"status": "ok", "seq": seq}))


def cmd_dedup_check(post_id: str) -> None:
    """Check if a post_id already exists in posts-index.jsonl."""
    data_dir = _get_data_dir()
    file_path = data_dir / "posts-index.jsonl"
    entries = _read_jsonl(file_path)

    # Check both exact match and numeric ID match
    numeric = _extract_numeric_id(post_id)
    exists = any(
        e.get("post_id") == post_id or
        (numeric and _extract_numeric_id(e.get("post_id", "")) == numeric)
        for e in entries
    )
    print(json.dumps({"status": "ok", "post_id": post_id, "exists": exists}))


def cmd_dedup_check_batch(post_ids: List[str]) -> None:
    """Check multiple post_ids in one pass (loads index once)."""
    data_dir = _get_data_dir()
    file_path = data_dir / "posts-index.jsonl"
    entries = _read_jsonl(file_path)

    # Build set of known numeric IDs for fast lookup
    known_numeric: set = set()
    known_exact: set = set()
    for e in entries:
        pid = e.get("post_id", "")
        known_exact.add(pid)
        num = _extract_numeric_id(pid)
        if num:
            known_numeric.add(num)

    results: Dict[str, bool] = {}
    for pid in post_ids:
        numeric = _extract_numeric_id(pid)
        exists = pid in known_exact or (numeric is not None and numeric in known_numeric)
        results[pid] = exists

    new_ids = [pid for pid, exists in results.items() if not exists]
    existing_ids = [pid for pid, exists in results.items() if exists]

    print(json.dumps({
        "status": "ok",
        "total": len(post_ids),
        "new_count": len(new_ids),
        "existing_count": len(existing_ids),
        "new_ids": new_ids,
        "existing_ids": existing_ids,
        "results": results,
    }))


def cmd_migrate() -> None:
    """Normalize all JSONL data to v2 schema, dedup, clean up batch files."""
    data_dir = _get_data_dir()
    if not data_dir.exists():
        print(json.dumps({"error": "Data directory does not exist. Run init first."}))
        sys.exit(1)

    report: Dict[str, Any] = {}

    # Migrate posts-index.jsonl
    posts_file = data_dir / "posts-index.jsonl"
    if posts_file.exists():
        entries = _read_jsonl(posts_file)
        original_count = len(entries)
        normalized = [_normalize_post(e) for e in entries]
        # Dedup by numeric ID (keep last occurrence)
        seen: Dict[str, Dict[str, Any]] = {}
        for e in normalized:
            numeric = _extract_numeric_id(e.get("post_id", ""))
            key = numeric if numeric else e.get("post_id", str(id(e)))
            seen[key] = e
        deduped = list(seen.values())
        _write_jsonl(posts_file, deduped)
        report["posts-index.jsonl"] = {
            "original": original_count,
            "after_dedup": len(deduped),
            "removed": original_count - len(deduped),
        }

    # Migrate insights-log.jsonl
    insights_file = data_dir / "insights-log.jsonl"
    if insights_file.exists():
        entries = _read_jsonl(insights_file)
        original_count = len(entries)
        normalized = [_normalize_insight(e) for e in entries]
        # Dedup by insight_id (keep last occurrence)
        seen_insights: Dict[str, Dict[str, Any]] = {}
        for e in normalized:
            key = e.get("insight_id", str(id(e)))
            seen_insights[key] = e
        deduped = list(seen_insights.values())
        _write_jsonl(insights_file, deduped)
        report["insights-log.jsonl"] = {
            "original": original_count,
            "after_dedup": len(deduped),
            "removed": original_count - len(deduped),
        }

    # Clean up orphaned batch files
    batch_removed = 0
    lock_removed = 0
    for f in data_dir.iterdir():
        if f.name.startswith("batch-") and f.suffix == ".jsonl":
            f.unlink()
            batch_removed += 1
        elif f.suffix == ".lock":
            f.unlink()
            lock_removed += 1
    report["cleanup"] = {"batch_files_removed": batch_removed, "lock_files_removed": lock_removed}

    print(json.dumps({"status": "ok", **report}, ensure_ascii=False))


def cmd_update(file_name: str, key_field: str, key_value: str, json_patch: str) -> None:
    """Patch fields on an existing entry identified by key_field=key_value."""
    data_dir = _get_data_dir()

    valid_files = ["scan-log.jsonl", "posts-index.jsonl", "insights-log.jsonl", "actions-log.jsonl"]
    if file_name not in valid_files:
        print(json.dumps({"error": f"Invalid file: {file_name}. Valid: {valid_files}"}))
        sys.exit(1)

    try:
        patch = json.loads(json_patch)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON patch: {e}"}))
        sys.exit(1)

    file_path = data_dir / file_name
    entries = _read_jsonl(file_path)

    updated = 0
    for entry in entries:
        if entry.get(key_field) == key_value:
            entry.update(patch)
            updated += 1

    if updated > 0:
        _write_jsonl(file_path, entries)

    print(json.dumps({"status": "ok", "file": file_name, "key": f"{key_field}={key_value}", "updated": updated}))


def cmd_compact(file_name: str) -> None:
    """Remove duplicate entries by primary key (post_id or insight_id)."""
    data_dir = _get_data_dir()

    valid_files = ["posts-index.jsonl", "insights-log.jsonl"]
    if file_name not in valid_files:
        print(json.dumps({"error": f"compact only supports: {valid_files}"}))
        sys.exit(1)

    file_path = data_dir / file_name
    entries = _read_jsonl(file_path)
    original_count = len(entries)

    if file_name == "posts-index.jsonl":
        key_field = "post_id"
        # Use numeric ID for dedup
        seen: Dict[str, Dict[str, Any]] = {}
        for e in entries:
            numeric = _extract_numeric_id(e.get(key_field, ""))
            key = numeric if numeric else e.get(key_field, str(id(e)))
            seen[key] = e
        deduped = list(seen.values())
    else:
        key_field = "insight_id"
        seen_map: Dict[str, Dict[str, Any]] = {}
        for e in entries:
            key = e.get(key_field, str(id(e)))
            seen_map[key] = e
        deduped = list(seen_map.values())

    _write_jsonl(file_path, deduped)

    print(json.dumps({
        "status": "ok",
        "file": file_name,
        "original": original_count,
        "after_compact": len(deduped),
        "removed": original_count - len(deduped),
    }))


def cmd_last_scanned(handle: str, timestamp: Optional[str] = None) -> None:
    """Get or set per-account last_scanned timestamp in accounts.json."""
    if not _ACCOUNTS_JSON.exists():
        print(json.dumps({"error": f"accounts.json not found at {_ACCOUNTS_JSON}"}))
        sys.exit(1)

    with open(_ACCOUNTS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    accounts = data.get("accounts", [])
    found = False
    for acct in accounts:
        if acct.get("handle") == handle or acct.get("handle") == f"@{handle.lstrip('@')}":
            found = True
            if timestamp:
                acct["last_scanned"] = timestamp
                with open(_ACCOUNTS_JSON, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    f.write("\n")
                print(json.dumps({"status": "ok", "handle": handle, "last_scanned": timestamp, "action": "set"}))
            else:
                ls = acct.get("last_scanned")
                print(json.dumps({"status": "ok", "handle": handle, "last_scanned": ls}))
            break

    if not found:
        print(json.dumps({"error": f"Account not found: {handle}"}))
        sys.exit(1)


def cmd_stats() -> None:
    """Print statistics about all state files."""
    data_dir = _get_data_dir()
    stats: Dict[str, Any] = {"data_dir": str(data_dir), "files": {}}

    files = ["scan-log.jsonl", "posts-index.jsonl", "insights-log.jsonl", "actions-log.jsonl"]
    for fname in files:
        fpath = data_dir / fname
        if fpath.exists():
            entries = _read_jsonl(fpath)
            size_bytes = fpath.stat().st_size
            file_stats: Dict[str, Any] = {
                "entries": len(entries),
                "size_bytes": size_bytes,
            }
            if entries:
                # Check both timestamp and posted_at for newest/oldest
                def _best_ts(e: Dict[str, Any]) -> str:
                    return max(e.get("timestamp", ""), e.get("posted_at", ""))
                file_stats["newest"] = _best_ts(entries[-1]) or "unknown"
                file_stats["oldest"] = _best_ts(entries[0]) or "unknown"
            stats["files"][fname] = file_stats
        else:
            stats["files"][fname] = {"entries": 0, "size_bytes": 0}

    # Count orphaned batch/lock files
    orphaned_batch = 0
    orphaned_lock = 0
    if data_dir.exists():
        for f in data_dir.iterdir():
            if f.name.startswith("batch-") and f.suffix == ".jsonl":
                orphaned_batch += 1
            elif f.suffix == ".lock":
                orphaned_lock += 1
    stats["orphaned_batch_files"] = orphaned_batch
    stats["orphaned_lock_files"] = orphaned_lock

    seq_file = data_dir / ".seq"
    if seq_file.exists():
        try:
            with open(seq_file, "r", encoding="utf-8") as f:
                stats["current_seq"] = int(f.read().strip() or "0")
        except (ValueError, OSError):
            stats["current_seq"] = 0
    else:
        stats["current_seq"] = 0

    print(json.dumps({"status": "ok", **stats}, ensure_ascii=False))


def main() -> None:
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: state_manager.py <command> [args]"}))
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "init":
        cmd_init()
    elif cmd == "append":
        if len(sys.argv) < 4:
            print(json.dumps({"error": "Usage: state_manager.py append <file> <json_line>"}))
            sys.exit(1)
        cmd_append(sys.argv[2], sys.argv[3])
    elif cmd == "read":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: state_manager.py read <file> [--since DATE] [--status STATUS] [--limit N]"}))
            sys.exit(1)
        file_name = sys.argv[2]
        since = None
        status = None
        limit = None
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--since" and i + 1 < len(sys.argv):
                since = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--status" and i + 1 < len(sys.argv):
                status = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--limit" and i + 1 < len(sys.argv):
                try:
                    limit = int(sys.argv[i + 1])
                except ValueError:
                    pass
                i += 2
            else:
                i += 1
        cmd_read(file_name, since=since, status=status, limit=limit)
    elif cmd == "next-seq":
        cmd_next_seq()
    elif cmd == "dedup-check":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: state_manager.py dedup-check <post_id>"}))
            sys.exit(1)
        cmd_dedup_check(sys.argv[2])
    elif cmd == "dedup-check-batch":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: state_manager.py dedup-check-batch <post_id1> [post_id2 ...]"}))
            sys.exit(1)
        cmd_dedup_check_batch(sys.argv[2:])
    elif cmd == "migrate":
        cmd_migrate()
    elif cmd == "update":
        if len(sys.argv) < 6:
            print(json.dumps({"error": "Usage: state_manager.py update <file> <key_field> <key_value> <json_patch>"}))
            sys.exit(1)
        cmd_update(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif cmd == "compact":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: state_manager.py compact <file>"}))
            sys.exit(1)
        cmd_compact(sys.argv[2])
    elif cmd == "last-scanned":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: state_manager.py last-scanned <handle> [<iso_timestamp>]"}))
            sys.exit(1)
        ts = sys.argv[3] if len(sys.argv) > 3 else None
        cmd_last_scanned(sys.argv[2], ts)
    elif cmd == "stats":
        cmd_stats()
    else:
        print(json.dumps({"error": f"Unknown command: {cmd}. Valid: init, append, read, next-seq, dedup-check, dedup-check-batch, migrate, update, compact, last-scanned, stats"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
