"""مسارات المشروع الجذرية."""

from __future__ import annotations

from pathlib import Path

# novel_craft/ -> repo root
PACKAGE_DIR = Path(__file__).resolve().parent
ROOT = PACKAGE_DIR.parent
SKILLS_DIR = ROOT / "skills"
FOUNDATION_DIR = ROOT / "00-foundation"
DOCS_DIR = ROOT / "docs"
PROJECTS_DIR = ROOT / "projects"
TEMPLATES_DIR = ROOT / "templates"
DATA_DIR = PACKAGE_DIR / "data"
SCHEMAS_DIR = PACKAGE_DIR / "schemas"


def ensure_layout() -> None:
    """إنشاء المجلدات الأساسية إن لم تكن موجودة."""
    for d in (PROJECTS_DIR, TEMPLATES_DIR, DOCS_DIR):
        d.mkdir(parents=True, exist_ok=True)
