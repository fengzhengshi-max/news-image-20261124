#!/usr/bin/env python3
"""Entrypoint for the news-image entry.

Copies the finished image (entry.png, sitting next to this script)
into the output directory given by MAKEFUN_OUTPUT_DIR
(default: "out"), preserving the bytes exactly.
"""

import os
import shutil
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"


def main() -> int:
    source = Path(__file__).resolve().parent / SOURCE_NAME
    if not source.is_file():
        print(f"error: {SOURCE_NAME} not found next to main.py: {source}", file=sys.stderr)
        print("Run this script from the repo directory containing entry.png.", file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    dest_dir = Path(output_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    dest = dest_dir / SOURCE_NAME
    if dest.resolve() == source.resolve():
        print("error: output directory is the repo directory; refusing to copy entry.png onto itself", file=sys.stderr)
        return 1
    shutil.copyfile(source, dest)

    size = dest.stat().st_size
    print(f"Copied {source.name} -> {dest} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
