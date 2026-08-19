#!/usr/bin/env python3
"""Install Shipwright skill and Codex agent profiles at user or project scope."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILL = "shipwright"
SKILL_SRC = ROOT / "skills" / SKILL
PROFILE_SRC = ROOT / "agent-profiles" / SKILL
VERSION = (SKILL_SRC / "VERSION").read_text(encoding="utf-8").strip()


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).expanduser().resolve()


def targets(scope: str, repo: str | None):
    if scope == "user":
        return (
            Path.home() / ".agents" / "skills" / SKILL,
            codex_home() / "agents",
            codex_home() / SKILL,
        )
    if not repo:
        raise ValueError("--repo is required with --scope project")
    root = Path(repo).expanduser().resolve()
    return (
        root / ".agents" / "skills" / SKILL,
        root / ".codex" / "agents",
        root / ".codex" / SKILL,
    )


def profiles():
    return sorted(PROFILE_SRC.glob("shipwright-*.toml"))


def remove(path: Path):
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def copy_atomic(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{dst.name}.install-", dir=str(dst.parent)))
    try:
        staged = staging / dst.name
        if src.is_dir():
            shutil.copytree(src, staged, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
        else:
            shutil.copy2(src, staged)
        staged.replace(dst)
    finally:
        shutil.rmtree(staging, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser(description="Install Shipwright for Codex.")
    ap.add_argument("skill", choices=[SKILL])
    ap.add_argument("--scope", choices=["user", "project"], required=True)
    ap.add_argument("--repo", help="Target repository for --scope project")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--replace", action="store_true", help="Replace an existing Shipwright installation.")
    args = ap.parse_args()

    try:
        skill_dst, agents_dst, state_dst = targets(args.scope, args.repo)
    except ValueError as exc:
        ap.error(str(exc))

    profile_srcs = profiles()
    if not SKILL_SRC.exists() or not profile_srcs:
        print("ERROR: incomplete Shipwright package.", file=sys.stderr)
        return 2

    plan = [("skill", SKILL_SRC, skill_dst)] + [
        ("profile", src, agents_dst / src.name) for src in profile_srcs
    ]
    conflicts = [dst for _, _, dst in plan if dst.exists()]

    print(f"Shipwright {VERSION}")
    print(f"Scope: {args.scope}")
    for kind, _, dst in plan:
        print(f"{'REPLACE' if dst.exists() else 'INSTALL':7} {kind:7} {dst}")

    if conflicts and not args.replace:
        print("\nREFUSED: destination already exists.", file=sys.stderr)
        for path in conflicts:
            print(f"  - {path}", file=sys.stderr)
        print("Re-run with --replace only after reviewing the destinations.", file=sys.stderr)
        return 3

    if args.dry_run:
        print("\nDRY RUN: no changes made.")
        return 0

    for _, src, dst in plan:
        if dst.exists():
            remove(dst)
        copy_atomic(src, dst)

    state_dst.mkdir(parents=True, exist_ok=True)
    manifest = {
        "skill": SKILL,
        "version": VERSION,
        "scope": args.scope,
        "source": str(ROOT),
        "skill_path": str(skill_dst),
        "profiles": [str(dst) for kind, _, dst in plan if kind == "profile"],
    }
    (state_dst / "install.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(f"\nPASS: installed Shipwright {VERSION}.")
    print(f"Manifest: {state_dst / 'install.json'}")
    print("Restart Codex so skill and custom-agent discovery is rebuilt.")
    print("Recommended parent route: gpt-5.6-luna / xhigh.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
