import os
import sys
from pathlib import Path

# Add the repo root to sys.path so the vendored 'picar' package is importable.
repo_root = str(Path(__file__).resolve().parent.parent.parent)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "remote_control.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
