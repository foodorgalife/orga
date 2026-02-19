#!/usr/bin/env python3
"""Toolbelt: a small but useful multi-tool CLI for day-to-day terminal work."""

from __future__ import annotations

import argparse
import hashlib
import json
import secrets
import string
import sys
from pathlib import Path
from typing import Iterable


def generate_password(length: int, include_symbols: bool = True) -> str:
    if length < 4:
        raise ValueError("Password length must be at least 4")

    alphabet = string.ascii_letters + string.digits
    if include_symbols:
        alphabet += "!@#$%^&*()-_=+[]{};:,.?/"

    return "".join(secrets.choice(alphabet) for _ in range(length))


def digest_bytes(data: bytes, algo: str) -> str:
    hasher = hashlib.new(algo)
    hasher.update(data)
    return hasher.hexdigest()


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_file():
            yield path


def cmd_pwgen(args: argparse.Namespace) -> int:
    print(generate_password(args.length, not args.no_symbols))
    return 0


def cmd_hash(args: argparse.Namespace) -> int:
    if args.text is None and args.file is None:
        print("Either --text or --file is required", file=sys.stderr)
        return 2

    if args.text is not None:
        data = args.text.encode("utf-8")
    else:
        data = Path(args.file).read_bytes()

    print(digest_bytes(data, args.algo))
    return 0


def cmd_jsonfmt(args: argparse.Namespace) -> int:
    try:
        if args.file:
            obj = json.loads(Path(args.file).read_text(encoding="utf-8"))
        else:
            obj = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(obj, indent=args.indent, sort_keys=args.sort_keys))
    return 0


def cmd_dupes(args: argparse.Namespace) -> int:
    root = Path(args.path)
    if not root.exists() or not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 2

    hashes: dict[str, list[Path]] = {}
    for file_path in iter_files(root):
        digest = digest_bytes(file_path.read_bytes(), args.algo)
        hashes.setdefault(digest, []).append(file_path)

    groups = [paths for paths in hashes.values() if len(paths) > 1]
    if not groups:
        print("No duplicates found")
        return 0

    for idx, paths in enumerate(groups, start=1):
        print(f"Duplicate group {idx}:")
        for path in paths:
            print(f"  {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="toolbelt",
        description="A compact utility belt for common terminal tasks.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    pwgen = subparsers.add_parser("pwgen", help="Generate secure passwords")
    pwgen.add_argument("length", type=int, nargs="?", default=20)
    pwgen.add_argument("--no-symbols", action="store_true", help="Exclude punctuation")
    pwgen.set_defaults(func=cmd_pwgen)

    hash_parser = subparsers.add_parser("hash", help="Hash text or files")
    hash_parser.add_argument("--algo", default="sha256", choices=hashlib.algorithms_guaranteed)
    hash_input = hash_parser.add_mutually_exclusive_group(required=True)
    hash_input.add_argument("--text", help="Raw text to hash")
    hash_input.add_argument("--file", help="Path to file to hash")
    hash_parser.set_defaults(func=cmd_hash)

    jsonfmt = subparsers.add_parser("jsonfmt", help="Validate and pretty-print JSON")
    jsonfmt.add_argument("--file", help="JSON file (defaults to STDIN)")
    jsonfmt.add_argument("--indent", type=int, default=2)
    jsonfmt.add_argument("--sort-keys", action="store_true")
    jsonfmt.set_defaults(func=cmd_jsonfmt)

    dupes = subparsers.add_parser("dupes", help="Find duplicate files in a directory")
    dupes.add_argument("path", nargs="?", default=".")
    dupes.add_argument("--algo", default="sha256", choices=hashlib.algorithms_guaranteed)
    dupes.set_defaults(func=cmd_dupes)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
