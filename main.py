#!/usr/bin/env python3
"""News-image entry v2 for make.fun competition news-image-20261124:
"Sum up 24 November's world news in one image".

The entry is the PNG beside this file (entry.png, 1024x1024,
drawn locally with PIL by draw-v2.py: a newspaper front page with
six verified stories from Tuesday 24 November 2026, built from the
full day's news). This program copies it to the output directory
the grader reads, so the judge sees exactly those bytes.

Python 3.13, standard library only. Outside the grader's container,
MAKEFUN_OUTPUT_DIR stands in for /output:
  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
# An empty MAKEFUN_OUTPUT_DIR means the same as an unset one.
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
TARGET = Path(OUT_DIR) / "entry.png"

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main() -> None:
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    data = SOURCE.read_bytes()
    TARGET.write_bytes(data)
    written = TARGET.read_bytes()
    if len(written) != len(data):
        raise SystemExit(
            f"entry.png copy mismatch: wrote {len(written)} bytes, "
            f"source is {len(data)}"
        )
    # The gate reads the file by its first bytes: refuse to pass on a
    # truncated or non-PNG copy instead of letting the entry score 0.
    if written[:8] != PNG_MAGIC:
        raise SystemExit(f"{TARGET} does not start with the PNG magic bytes")
    print(f"wrote {TARGET} ({len(written)} bytes)")


if __name__ == "__main__":
    main()
