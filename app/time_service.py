from datetime import datetime, timezone
from typing import Any, Optional


def now_iso() -> str:
    """Current UTC time as a stable ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def parse_iso(value: Any) -> Optional[datetime]:
    """Parses a stored timestamp back into a timezone-aware datetime. Returns None if absent/invalid."""
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value))
    except (ValueError, TypeError):
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def to_epoch_ms(value: Any) -> Optional[int]:
    """Converts a stored timestamp to epoch milliseconds for the JS timeline. None if unknown."""
    dt = parse_iso(value)
    return int(dt.timestamp() * 1000) if dt else None


def format_timestamp(value: Any, fmt: str = "%Y-%m-%d %H:%M") -> str:
    """Formats a stored UTC timestamp in the viewer's local timezone."""
    dt = parse_iso(value)
    return dt.astimezone().strftime(fmt) if dt else "unknown"


def relative_time(value: Any) -> str:
    """Human-friendly age, e.g. '3h ago'."""
    dt = parse_iso(value)
    if dt is None:
        return "unknown"
    secs = int((datetime.now(timezone.utc) - dt).total_seconds())
    if secs < 60:
        return "just now"
    if secs < 3600:
        return f"{secs // 60}m ago"
    if secs < 86400:
        return f"{secs // 3600}h ago"
    if secs < 2592000:
        return f"{secs // 86400}d ago"
    return f"{secs // 2592000}mo ago"


def capture_snapshot(graph) -> dict:
    """Records which nodes/edges exist BEFORE an extraction, so new ones can be identified after."""
    return {"nodes": set(graph.nodes), "edges": set(graph.edges)}


def ensure_timestamps(graph) -> None:
    """Backfills timestamp fields on graphs created before this feature existed.

    Legacy entries get created_at=None ('unknown') rather than a fabricated date —
    inventing a timestamp would be worse than admitting we don't have one.
    """
    for _, data in graph.nodes(data=True):
        data.setdefault("created_at", None)
        data.setdefault("updated_at", data.get("created_at"))
        data.setdefault("mention_count", 0)
    for _, _, data in graph.edges(data=True):
        data.setdefault("created_at", None)
        data.setdefault("updated_at", data.get("created_at"))
        data.setdefault("mention_count", 0)


def _resolve_node_id(graph, raw_id):
    """Matches an extracted entity id to an existing graph node, tolerating case/whitespace
    normalization done by update_graph. Returns None if there's no match — never creates a node."""
    if raw_id in graph:
        return raw_id
    target = str(raw_id).strip().lower()
    for nid in graph.nodes:
        if str(nid).strip().lower() == target:
            return nid
    return None


def stamp_graph_changes(graph, snapshot: dict, extracted_kg=None, timestamp: str = None) -> str:
    """Applies creation/update timestamps after update_graph has run.

    - Nodes/edges absent from the snapshot are brand new -> created_at + updated_at.
    - Pre-existing entities named in this extraction -> updated_at bumped, mention_count += 1.

    Returns the timestamp used, so the caller can reference it.
    """
    ts = timestamp or now_iso()

    for nid, data in graph.nodes(data=True):
        if nid not in snapshot["nodes"]:
            data["created_at"] = ts
            data["updated_at"] = ts
            data["mention_count"] = 1

    for u, v, data in graph.edges(data=True):
        if (u, v) not in snapshot["edges"]:
            data["created_at"] = ts
            data["updated_at"] = ts
            data["mention_count"] = 1

    # Backfill anything still missing (legacy entries) without overwriting what we just set
    ensure_timestamps(graph)

    if extracted_kg is not None:
        for node in getattr(extracted_kg, "nodes", []) or []:
            rid = _resolve_node_id(graph, node.id)
            if rid is None or rid not in snapshot["nodes"]:
                continue
            data = graph.nodes[rid]
            data["updated_at"] = ts
            data["mention_count"] = int(data.get("mention_count") or 0) + 1

        for edge in getattr(extracted_kg, "edges", []) or []:
            src = _resolve_node_id(graph, edge.source)
            tgt = _resolve_node_id(graph, edge.target)
            if src is None or tgt is None or not graph.has_edge(src, tgt):
                continue
            if (src, tgt) not in snapshot["edges"]:
                continue
            data = graph.edges[src, tgt]
            data["updated_at"] = ts
            data["mention_count"] = int(data.get("mention_count") or 0) + 1

    return ts


def get_timeline_events(graph, limit: int = None) -> list:
    """Returns entities in reverse-chronological order of first appearance."""
    ensure_timestamps(graph)
    events = []
    for nid, data in graph.nodes(data=True):
        events.append({
            "Entity": data.get("label", nid),
            "Type": data.get("entity_type", "unknown"),
            "Status": data.get("status", "unreviewed"),
            "First seen": format_timestamp(data.get("created_at")),
            "Last mentioned": format_timestamp(data.get("updated_at")),
            "Mentions": int(data.get("mention_count") or 0),
            "_sort": data.get("created_at") or "",
        })
    events.sort(key=lambda e: e["_sort"], reverse=True)
    for e in events:
        e.pop("_sort")
    return events[:limit] if limit else events


def get_daily_counts(graph) -> dict:
    """Counts how many entities were first learned on each calendar day (local time)."""
    counts = {}
    for _, data in graph.nodes(data=True):
        dt = parse_iso(data.get("created_at"))
        if dt is None:
            continue
        day = dt.astimezone().strftime("%Y-%m-%d")
        counts[day] = counts.get(day, 0) + 1
    return dict(sorted(counts.items()))