"""The real tools. DO NOT EDIT.

These do the actual work on disk. Whether they are *allowed* to run is your
harness's problem, not theirs.
"""
import hashlib
import os
import subprocess
import sys
from pathlib import Path


def read_file(repo, path):
    return (Path(repo) / path).read_text()


def edit_file(repo, path, old_text, new_text):
    p = Path(repo) / path
    src = p.read_text()
    if old_text not in src:
        raise ValueError(f"old_text not found in {path}")
    p.write_text(src.replace(old_text, new_text, 1))
    return f"edited {path}"


def run_tests(repo):
    """Run the repo's unittest suite. Returns (passed: bool, output: str)."""
    env = dict(os.environ, PYTHONPATH=str(repo), PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
        cwd=repo, capture_output=True, text=True, env=env, timeout=30,
    )
    return p.returncode == 0, (p.stdout + p.stderr).strip()


def run_bash(repo, command):
    p = subprocess.run(command, shell=True, cwd=repo, capture_output=True, text=True, timeout=30)
    return (p.stdout + p.stderr).strip()


def hash_dir(path):
    """One fingerprint for everything under `path`. Changes if any file changes."""
    h = hashlib.sha256()
    for f in sorted(Path(path).rglob("*")):
        if f.is_file() and "__pycache__" not in f.parts:
            h.update(str(f.relative_to(path)).encode())
            h.update(f.read_bytes())
    return h.hexdigest()
