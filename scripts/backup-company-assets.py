#!/usr/bin/env python3
"""Snapshot the company assets that exist ONLY in the working tree.

`my-company/` is gitignored and boundary-protected, so its contents have no copy in git.
That is deliberate — the evidence ledger names contract numbers and customer facts — but it
means an ordinary git operation can destroy them with no undo. That is not hypothetical: on
2026-08-04 a `git checkout main && git pull` deleted `my-company/evidence-ledger.json` and
`my-company/past-performance.md` from disk, because both were tracked on main and untracked
on the branch being merged. The ledger was recoverable only from a hand-made backup, and
git's own copy of it was 80 items stale.

This script exists so that recovery is never luck. It copies each protected asset to a
timestamped file OUTSIDE the project directory, skips writes when content has not changed,
and refuses to overwrite good history with a corrupt file.

Destination: ~/.claude/backups/fpa-company-assets/<asset-stem>/<stem>-<UTC timestamp>.<ext>

Usage:
  python scripts/backup-company-assets.py              # snapshot anything that changed
  python scripts/backup-company-assets.py --list       # what is backed up, and how stale
  python scripts/backup-company-assets.py --verify     # exit 1 if any asset is unprotected
  python scripts/backup-company-assets.py --restore my-company/evidence-ledger.json
  python scripts/backup-company-assets.py --selftest

Exit codes:
  0 = success (or selftest passed)
  1 = --verify found an asset with no usable backup, or a restore failed
  2 = usage or environment error
"""

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).parent.parent
BACKUP_ROOT = Path.home() / ".claude" / "backups" / "fpa-company-assets"

# The assets with no copy in git. Add a path here the moment something else becomes
# both gitignored and irreplaceable.
ASSETS = [
    "my-company/evidence-ledger.json",
    "my-company/past-performance.md",
    "my-company/claim-envelope.md",
    "my-company/capabilities.md",
    "my-company/company-profile.md",
    "my-company/company-description.md",
    "my-company/contract-vehicles.md",
    "my-company/published-research.md",
]

# Keep this many snapshots per asset. Old ones are pruned only when the count is
# exceeded AND at least one newer snapshot exists — pruning to zero is never correct.
KEEP_PER_ASSET = 20


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_structurally_valid(path: Path) -> tuple[bool, str]:
    """Cheap sanity check so a truncated or corrupt file never becomes the newest backup.

    JSON must parse. Markdown must be non-trivial — a 0-byte file is the signature of a
    failed write, and backing it up over good history is how a bad day becomes a worse one.
    """
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return False, f"unreadable ({exc})"
    if not raw.strip():
        return False, "empty"
    if path.suffix == ".json":
        try:
            data = json.loads(raw.decode("utf-8", errors="replace"))
        except json.JSONDecodeError as exc:
            return False, f"invalid JSON ({exc.msg} at line {exc.lineno})"
        # The ledger specifically: an items list that has collapsed is the failure we care
        # about, and it is silent — the file still parses.
        if isinstance(data, dict) and "items" in data:
            n = len(data["items"])
            if n == 0:
                return False, "JSON parses but items[] is empty"
            return True, f"{n} items"
    return True, f"{len(raw)} bytes"


def asset_dir(rel_path: str) -> Path:
    return BACKUP_ROOT / Path(rel_path).stem


def snapshots(rel_path: str) -> list[Path]:
    d = asset_dir(rel_path)
    if not d.exists():
        return []
    suffix = Path(rel_path).suffix
    return sorted(d.glob(f"{Path(rel_path).stem}-*{suffix}"))


def newest_snapshot(rel_path: str) -> Path | None:
    snaps = snapshots(rel_path)
    return snaps[-1] if snaps else None


def snapshot_taken_at(path: Path) -> datetime | None:
    """When the snapshot was TAKEN, parsed from its filename.

    Not the file mtime: shutil.copy2 preserves the source's mtime, so a snapshot taken
    seconds ago inherits the timestamp of content that may be days old. Reporting that as
    the backup's age makes a fresh backup look dangerously stale, which teaches people to
    distrust the one tool that is supposed to reassure them.
    """
    m = re.search(r"-(\d{8}T\d{6}\d{6})Z", path.name)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1), "%Y%m%dT%H%M%S%f").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def prune(rel_path: str) -> list[Path]:
    snaps = snapshots(rel_path)
    if len(snaps) <= KEEP_PER_ASSET:
        return []
    doomed = snaps[: len(snaps) - KEEP_PER_ASSET]
    for p in doomed:
        p.unlink()
    return doomed


def backup_one(rel_path: str, force: bool = False) -> tuple[str, str]:
    """Return (status, detail). status is one of: saved, unchanged, missing, refused."""
    src = WORKSPACE_ROOT / rel_path
    if not src.exists():
        prior = newest_snapshot(rel_path)
        if prior:
            return "missing", f"NOT on disk — newest backup is {prior.name} (restorable)"
        return "missing", "NOT on disk and NO backup exists"

    ok, detail = is_structurally_valid(src)
    if not ok:
        return "refused", f"{detail} — refusing to snapshot over good history"

    prior = newest_snapshot(rel_path)
    if prior and not force and sha256(prior) == sha256(src):
        return "unchanged", f"identical to {prior.name}"

    dest_dir = asset_dir(rel_path)
    dest_dir.mkdir(parents=True, exist_ok=True)
    stem, suffix = Path(rel_path).stem, Path(rel_path).suffix
    # Microsecond resolution, fixed width, never reused. Ordering here is load-bearing —
    # newest_snapshot() is what --restore hands back — so the name must sort by recency
    # under a plain lexicographic sort. A per-second stamp plus a collision counter was
    # tried and is subtly wrong: pruning frees a low sequence number, the next snapshot
    # reuses it, and the NEWEST content ends up sorting oldest.
    now = datetime.now(timezone.utc)
    while True:
        dest = dest_dir / f"{stem}-{now.strftime('%Y%m%dT%H%M%S%f')}Z{suffix}"
        if not dest.exists():
            break
        now = now.replace(microsecond=min(now.microsecond + 1, 999999))
    shutil.copy2(src, dest)
    pruned = prune(rel_path)
    extra = f", pruned {len(pruned)} old" if pruned else ""
    return "saved", f"{detail} -> {dest.name}{extra}"


def cmd_backup(force: bool) -> int:
    print(f"Backing up to {BACKUP_ROOT}")
    counts: dict[str, int] = {}
    for rel in ASSETS:
        status, detail = backup_one(rel, force)
        counts[status] = counts.get(status, 0) + 1
        mark = {"saved": "SAVED ", "unchanged": "same  ", "missing": "GONE  ", "refused": "REFUSE"}[status]
        print(f"  {mark} {rel:42} {detail}")
    print("\n" + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    if counts.get("refused"):
        print("\nA refused asset means the file on disk looks corrupt. Investigate before "
              "re-running — the previous good snapshot is still intact.", file=sys.stderr)
    return 0


def cmd_list() -> int:
    now = datetime.now(timezone.utc)
    print(f"{BACKUP_ROOT}\n")
    for rel in ASSETS:
        snaps = snapshots(rel)
        src = WORKSPACE_ROOT / rel
        live = "on disk" if src.exists() else "MISSING FROM DISK"
        if not snaps:
            print(f"  {rel:42} {live:18} NO BACKUPS")
            continue
        newest = snaps[-1]
        taken = snapshot_taken_at(newest)
        age = f"{(now - taken).total_seconds() / 3600:5.1f}h" if taken else "  ?  "
        drift = ""
        if src.exists() and sha256(src) != sha256(newest):
            drift = "  <-- disk differs from newest backup"
        print(f"  {rel:42} {live:18} {len(snaps):>2} snaps, newest {age} old{drift}")
    return 0


def cmd_verify() -> int:
    problems: list[str] = []
    for rel in ASSETS:
        src = WORKSPACE_ROOT / rel
        snaps = snapshots(rel)
        if not src.exists() and not snaps:
            problems.append(f"{rel}: missing from disk AND has no backup")
        elif src.exists():
            ok, detail = is_structurally_valid(src)
            if not ok:
                problems.append(f"{rel}: on-disk file is {detail}")
            elif not snaps:
                problems.append(f"{rel}: exists but has never been backed up")
            elif sha256(src) != sha256(snaps[-1]):
                problems.append(f"{rel}: on-disk changes are not yet backed up")
    if problems:
        print("UNPROTECTED:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        print("\nRun: python scripts/backup-company-assets.py", file=sys.stderr)
        return 1
    print(f"All {len(ASSETS)} company assets are backed up and current.")
    return 0


def cmd_restore(rel_path: str) -> int:
    rel_path = rel_path.replace("\\", "/")
    if rel_path not in ASSETS:
        print(f"ERROR: {rel_path} is not a tracked company asset. Known:", file=sys.stderr)
        for a in ASSETS:
            print(f"  {a}", file=sys.stderr)
        return 2
    snaps = snapshots(rel_path)
    if not snaps:
        print(f"ERROR: no backups exist for {rel_path}", file=sys.stderr)
        return 1
    newest = snaps[-1]
    dest = WORKSPACE_ROOT / rel_path
    if dest.exists():
        ok, detail = is_structurally_valid(dest)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        # Aside files live in their own directory, NOT beside the snapshots. Kept alongside
        # them they match the snapshot glob and sort last (because "PRE-RESTORE" > a digit),
        # so the file we just set aside for being corrupt would become "the newest snapshot"
        # and the next --restore would hand it straight back.
        aside = asset_dir(rel_path) / "pre-restore" / f"{Path(rel_path).stem}-{stamp}{Path(rel_path).suffix}"
        aside.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dest, aside)
        print(f"Existing file ({detail}) set aside as pre-restore/{aside.name}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(newest, dest)
    ok, detail = is_structurally_valid(dest)
    print(f"Restored {rel_path} from {newest.name} ({detail})")
    return 0 if ok else 1


def selftest() -> int:
    import tempfile
    global WORKSPACE_ROOT, BACKUP_ROOT, ASSETS, KEEP_PER_ASSET
    orig = (WORKSPACE_ROOT, BACKUP_ROOT, list(ASSETS), KEEP_PER_ASSET)
    try:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            (root / "my-company").mkdir(parents=True)
            WORKSPACE_ROOT = root
            BACKUP_ROOT = Path(tmp) / "backups"
            ASSETS = ["my-company/evidence-ledger.json", "my-company/past-performance.md"]

            ledger = root / "my-company/evidence-ledger.json"
            pp = root / "my-company/past-performance.md"
            ledger.write_text(json.dumps({"items": [{"id": "EV-001"}, {"id": "EV-002"}]}), encoding="utf-8")
            pp.write_text("# Past Performance\n\nreal content\n", encoding="utf-8")

            assert backup_one(ASSETS[0])[0] == "saved"
            assert backup_one(ASSETS[1])[0] == "saved"
            # Idempotent: unchanged content must not create a second snapshot.
            assert backup_one(ASSETS[0])[0] == "unchanged"
            assert len(snapshots(ASSETS[0])) == 1, snapshots(ASSETS[0])

            # A real edit does snapshot.
            ledger.write_text(json.dumps({"items": [{"id": "EV-001"}, {"id": "EV-002"}, {"id": "EV-003"}]}),
                              encoding="utf-8")
            assert backup_one(ASSETS[0])[0] == "saved"
            assert len(snapshots(ASSETS[0])) == 2

            # Corruption must be REFUSED, and must not disturb existing history.
            good = sha256(snapshots(ASSETS[0])[-1])
            ledger.write_text("{ this is not json", encoding="utf-8")
            status, detail = backup_one(ASSETS[0])
            assert status == "refused" and "invalid JSON" in detail, (status, detail)
            assert len(snapshots(ASSETS[0])) == 2, "refusal must not add a snapshot"
            assert sha256(snapshots(ASSETS[0])[-1]) == good, "refusal must not alter history"

            # The silent killer: parses fine, items[] collapsed to zero.
            ledger.write_text(json.dumps({"items": []}), encoding="utf-8")
            status, detail = backup_one(ASSETS[0])
            assert status == "refused" and "items[] is empty" in detail, (status, detail)

            # verify() must fail while the on-disk file is corrupt.
            assert cmd_verify() == 1

            # Restore brings back the last good copy and sets the corrupt one aside.
            snaps_before = len(snapshots(ASSETS[0]))
            assert cmd_restore(ASSETS[0]) == 0
            restored = json.loads(ledger.read_text(encoding="utf-8"))
            assert len(restored["items"]) == 3, restored
            aside_dir = asset_dir(ASSETS[0]) / "pre-restore"
            assert aside_dir.is_dir() and list(aside_dir.iterdir()), "corrupt file must be set aside"
            # The aside copy must NOT join the snapshot set — otherwise the corrupt file it
            # holds becomes "newest" and the next restore serves it back.
            assert len(snapshots(ASSETS[0])) == snaps_before, "aside file leaked into snapshots"
            assert len(json.loads(newest_snapshot(ASSETS[0]).read_text(encoding="utf-8"))["items"]) == 3

            # Deleted file: reported as recoverable, not silently skipped.
            pp.unlink()
            status, detail = backup_one(ASSETS[1])
            assert status == "missing" and "restorable" in detail, (status, detail)
            assert cmd_restore(ASSETS[1]) == 0 and pp.exists()

            # Pruning keeps the cap, never empties the directory, and — the part that broke
            # twice — must leave the NEWEST content as the newest-sorting snapshot.
            KEEP_PER_ASSET = 3
            for n in range(6):
                pp.write_text(f"# Past Performance\n\nrevision {n}\n", encoding="utf-8")
                backup_one(ASSETS[1])
            assert len(snapshots(ASSETS[1])) == KEEP_PER_ASSET, snapshots(ASSETS[1])
            newest = newest_snapshot(ASSETS[1])
            assert "revision 5" in newest.read_text(encoding="utf-8"), \
                f"newest snapshot should hold the latest content, holds: {newest.read_text()!r}"
            assert sha256(newest) == sha256(pp), "newest snapshot must match the live file"

            assert cmd_verify() == 0, "everything should be protected at the end"
        print("SELFTEST PASS — snapshot, dedupe, corruption refusal, empty-items refusal, "
              "verify, restore, missing-file reporting, and pruning all verified")
        return 0
    finally:
        WORKSPACE_ROOT, BACKUP_ROOT, ASSETS, KEEP_PER_ASSET = orig


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--list", action="store_true", help="show what is backed up and how stale it is")
    g.add_argument("--verify", action="store_true", help="exit 1 if any asset is unprotected")
    g.add_argument("--restore", metavar="PATH", help="restore an asset from its newest good snapshot")
    g.add_argument("--selftest", action="store_true", help="deterministic offline self-test")
    parser.add_argument("--force", action="store_true", help="snapshot even when content is unchanged")
    args = parser.parse_args()

    if args.selftest:
        return selftest()
    if args.list:
        return cmd_list()
    if args.verify:
        return cmd_verify()
    if args.restore:
        return cmd_restore(args.restore)
    return cmd_backup(args.force)


if __name__ == "__main__":
    sys.exit(main())
