#!/usr/bin/env python3
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    # Add the repo root to sys.path so the vendored 'picar' package is importable.
    repo_root = str(Path(__file__).resolve().parent.parent)
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "remote_control.settings")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
