#!/usr/bin/env python3
"""Entrypoint: place the front-page image at the output path.

Standard library only. The image (entry.png, 1024x1024) is drawn by
draw_news.py and shipped in this repository; this program copies it
byte for byte to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    sys.exit(main())
