from __future__ import annotations

import tempfile
import time
from pathlib import Path
from queue import Empty, Queue
from typing import Any

from .setup_wizard import load_setup_profile

SCHEMA = "subreparo.watch_plan.v1"
SNAPSHOT_SCHEMA = "subreparo.watch_snapshot.v1"
EVENT_SCHEMA = "subreparo.watch_event.v1"

DEFAULT_SKIPPED_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
}

EXECUTABLE_OR_PERSISTENCE_SUFFIXES = {
    ".app",
    ".bat",
    ".cmd",
    ".com",
    ".dll",
    ".dylib",
    ".exe",
    ".js",
    ".jse",
    ".lnk",
    ".msi",
    ".plist",
    ".ps1",
    ".scr",
    ".service",
    ".sh",
    ".so",
    ".vbs",
    ".wsf",
}


def native_watchdog_available() -> bool:
    try:
        import watchdog.observers  # type: ignore[import-not-found]  # noqa: F401
    except ImportError:
        return False
    return True


def _existing_or_planned(path: Path) -> dict[str, Any]:
    return {
        "path": str(path.expanduser()),
        "exists": path.expanduser().exists(),
        "recursive": True,
        "events": ["created", "modified", "deleted", "moved"],
    }


def default_watch_targets(root: Path) -> list[dict[str, Any]]:
    root = root.resolve()
    home = Path.home()
    temp = Path(tempfile.gettempdir())
    targets = [
        {"kind": "project", **_existing_or_planned(root)},
        {"kind": "downloads", **_existing_or_planned(home / "Downloads")},
        {"kind": "desktop", **_existing_or_planned(home / "Desktop")},
        {"kind": "documents", **_existing_or_planned(home / "Documents")},
        {"kind": "temp", **_existing_or_planned(temp)},
        {"kind": "browser_downloads", **_existing_or_planned(home / "Downloads")},
    ]
    for candidate in (Path("/Volumes"), Path("/media"), Path("/mnt")):
        targets.append({"kind": "removable", **_existing_or_planned(candidate)})
    for archive_folder in (home / "Downloads", root):
        targets.append({
            "kind": "archive_extraction",
            **_existing_or_planned(archive_folder),
            "archive_suffixes": [".zip", ".tar", ".gz", ".tgz", ".7z", ".rar"],
        })
    targets.append({
        "kind": "process",
        "path": "process-table",
        "exists": True,
        "recursive": False,
        "events": ["new_process", "changed_command_line"],
    })
    return targets


def build_watch_plan(root: Path) -> dict[str, Any]:
    root = root.resolve()
    profile = load_setup_profile(root)
    if profile:
        profile_targets = [
            {"kind": "profile", **_existing_or_planned(Path(item).expanduser())}
            for item in profile.watched_paths
        ]
        targets = profile_targets + [item for item in default_watch_targets(root) if item["kind"] != "project"]
    else:
        targets = default_watch_targets(root)
    backend = "native_watchdog" if native_watchdog_available() else "polling_fallback"
    return {
        "schema": SCHEMA,
        "backend": backend,
        "native_available": backend == "native_watchdog",
        "targets": targets,
        "safety": {
            "local_only": True,
            "non_destructive": True,
            "alert_only_by_default": True,
        },
    }


def _walk_files(
    root: Path,
    *,
    max_files: int,
    skipped_dir_names: set[str] | None = None,
) -> tuple[list[Path], bool]:
    root = root.expanduser().resolve()
    skipped = skipped_dir_names or DEFAULT_SKIPPED_DIR_NAMES
    files: list[Path] = []
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            children = sorted(current.iterdir(), key=lambda item: item.name.lower())
        except OSError:
            continue
        for child in children:
            if child.name in skipped:
                continue
            try:
                if child.is_dir():
                    stack.append(child)
                elif child.is_file():
                    files.append(child)
                    if len(files) >= max_files:
                        return files, True
            except OSError:
                continue
    return files, False


def _relative_path(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.expanduser())


def build_file_snapshot(
    root: Path,
    *,
    max_files: int = 10_000,
    skipped_dir_names: set[str] | None = None,
) -> dict[str, Any]:
    """Build a privacy-preserving local file snapshot for watcher diffing.

    The snapshot stores path, size, and mtime metadata only. It deliberately does not
    read or hash file contents, which keeps the watcher local-first and lightweight.
    """

    root = root.expanduser().resolve()
    files, truncated = _walk_files(root, max_files=max_files, skipped_dir_names=skipped_dir_names)
    entries: dict[str, dict[str, Any]] = {}
    for path in files:
        try:
            stat = path.stat()
        except OSError:
            continue
        entries[_relative_path(root, path)] = {
            "size": stat.st_size,
            "mtime_ns": stat.st_mtime_ns,
            "suffix": path.suffix.lower(),
        }
    return {
        "schema": SNAPSHOT_SCHEMA,
        "root": str(root),
        "generated_at": int(time.time()),
        "truncated": truncated,
        "max_files": max_files,
        "files": dict(sorted(entries.items())),
    }


def _event_severity(path: str) -> str:
    suffix = Path(path).suffix.lower()
    if suffix in EXECUTABLE_OR_PERSISTENCE_SUFFIXES:
        return "medium"
    return "info"


def _event_recommendation(event_type: str, path: str) -> str:
    suffix = Path(path).suffix.lower()
    if suffix in EXECUTABLE_OR_PERSISTENCE_SUFFIXES:
        return (
            "Review this executable or persistence-capable file before trusting it. "
            "Run SubReparo patrol if it was not expected."
        )
    if event_type == "deleted":
        return "Confirm the removal was expected. Run a baseline diff if this is a watched project file."
    return "Confirm this local file event was expected. No automatic repair action was taken."


def _make_file_event(
    event_type: str,
    path: str,
    *,
    before: dict[str, Any] | None = None,
    after: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "schema": EVENT_SCHEMA,
        "backend": "polling_snapshot",
        "event_type": event_type,
        "path": path,
        "severity": _event_severity(path),
        "before": before,
        "after": after,
        "message": f"Local file {event_type}: {path}",
        "recommendation": _event_recommendation(event_type, path),
    }


def diff_file_snapshots(previous: dict[str, Any], current: dict[str, Any]) -> list[dict[str, Any]]:
    """Return created, modified, and deleted file events between two snapshots."""

    previous_files = previous.get("files", {}) if isinstance(previous, dict) else {}
    current_files = current.get("files", {}) if isinstance(current, dict) else {}
    if not isinstance(previous_files, dict) or not isinstance(current_files, dict):
        return []

    events: list[dict[str, Any]] = []
    for path in sorted(set(current_files) - set(previous_files)):
        events.append(_make_file_event("created", path, after=current_files[path]))
    for path in sorted(set(previous_files) - set(current_files)):
        events.append(_make_file_event("deleted", path, before=previous_files[path]))
    for path in sorted(set(previous_files) & set(current_files)):
        before = previous_files[path]
        after = current_files[path]
        if before.get("size") != after.get("size") or before.get("mtime_ns") != after.get("mtime_ns"):
            events.append(_make_file_event("modified", path, before=before, after=after))
    return events


def poll_file_events(
    root: Path,
    previous_snapshot: dict[str, Any] | None = None,
    *,
    max_files: int = 10_000,
) -> dict[str, Any]:
    """Build a new watcher snapshot and compare it with a previous one when supplied."""

    current = build_file_snapshot(root, max_files=max_files)
    events = diff_file_snapshots(previous_snapshot, current) if previous_snapshot else []
    return {
        "schema": "subreparo.watch_poll.v1",
        "backend": "polling_snapshot",
        "native_available": native_watchdog_available(),
        "snapshot": current,
        "events": events,
        "safety": {
            "local_only": True,
            "non_destructive": True,
            "alert_only_by_default": True,
            "content_reading": False,
        },
    }


def _normalize_native_event(event: Any, roots: list[Path]) -> dict[str, Any]:
    src_path = Path(str(getattr(event, "src_path", ""))).expanduser()
    dest_path_raw = str(getattr(event, "dest_path", "")) or None
    event_type = str(getattr(event, "event_type", "unknown"))
    path = _relative_to_any_root(src_path, roots)
    payload: dict[str, Any] = {
        "schema": EVENT_SCHEMA,
        "backend": "native_watchdog",
        "event_type": event_type,
        "path": path,
        "is_directory": bool(getattr(event, "is_directory", False)),
        "severity": _event_severity(path),
        "message": f"Native file watcher observed {event_type}: {path}",
        "recommendation": _event_recommendation(event_type, path),
    }
    if dest_path_raw:
        payload["dest_path"] = _relative_to_any_root(Path(dest_path_raw).expanduser(), roots)
    return payload


def _relative_to_any_root(path: Path, roots: list[Path]) -> str:
    for root in roots:
        try:
            return str(path.resolve().relative_to(root.resolve()))
        except ValueError:
            continue
    return str(path)


def collect_native_file_events(
    paths: list[Path],
    *,
    duration: float = 10.0,
    recursive: bool = True,
    max_events: int = 500,
) -> dict[str, Any]:
    """Collect native watchdog events for existing local directories.

    This is alert-only. It never modifies, isolates, deletes, or repairs files.
    If the optional watchdog package is not installed, the function returns a
    structured fallback payload instead of failing.
    """

    roots = [
        path.expanduser().resolve()
        for path in paths
        if path.expanduser().exists() and path.expanduser().is_dir()
    ]
    if not native_watchdog_available():
        return {
            "schema": "subreparo.native_file_watch.v1",
            "backend": "polling_fallback",
            "native_available": False,
            "watched_paths": [str(path) for path in roots],
            "events": [],
            "recommendation": (
                "Install the optional native watcher dependency with "
                "subreparo-immune[native-watch] to enable watchdog events."
            ),
            "safety": {
                "local_only": True,
                "non_destructive": True,
                "alert_only_by_default": True,
            },
        }
    if not roots:
        return {
            "schema": "subreparo.native_file_watch.v1",
            "backend": "native_watchdog",
            "native_available": True,
            "watched_paths": [],
            "events": [],
            "recommendation": "No existing local directories were available to watch.",
            "safety": {
                "local_only": True,
                "non_destructive": True,
                "alert_only_by_default": True,
            },
        }

    from watchdog.events import FileSystemEventHandler  # type: ignore[import-not-found]
    from watchdog.observers import Observer  # type: ignore[import-not-found]

    event_queue: Queue[Any] = Queue()

    class Handler(FileSystemEventHandler):
        def on_any_event(self, event: Any) -> None:
            if event_queue.qsize() < max_events:
                event_queue.put(event)

    observer = Observer()
    handler = Handler()
    for root in roots:
        observer.schedule(handler, str(root), recursive=recursive)

    observer.start()
    try:
        time.sleep(max(0.1, duration))
    finally:
        observer.stop()
        observer.join(timeout=5)

    events: list[dict[str, Any]] = []
    while len(events) < max_events:
        try:
            raw_event = event_queue.get_nowait()
        except Empty:
            break
        events.append(_normalize_native_event(raw_event, roots))

    return {
        "schema": "subreparo.native_file_watch.v1",
        "backend": "native_watchdog",
        "native_available": True,
        "watched_paths": [str(path) for path in roots],
        "duration_seconds": duration,
        "recursive": recursive,
        "truncated": len(events) >= max_events,
        "events": events,
        "safety": {
            "local_only": True,
            "non_destructive": True,
            "alert_only_by_default": True,
        },
    }
