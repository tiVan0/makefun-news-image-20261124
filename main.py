#!/usr/bin/env python3
"""Entrypoint: copy entry.png into the make.fun output directory.

Stdlib only. The image is shipped in the repo (drawn by render.py); this
program only copies it, so two runs write byte-identical output.
"""
import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")

if not os.path.isfile(SRC):
    raise SystemExit("entry.png missing from repo: " + SRC)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copyfile(SRC, OUT)
os.chmod(OUT, 0o644)
print("wrote", OUT)
