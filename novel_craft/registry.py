"""تحميل سجل المهارات والـ pipelines."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from novel_craft.paths import DATA_DIR, ROOT, SKILLS_DIR


@lru_cache(maxsize=1)
def load_registry() -> dict[str, Any]:
    path = DATA_DIR / "skills_registry.yaml"
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def list_skills() -> list[dict[str, Any]]:
    return list(load_registry().get("skills", []))


def get_skill(skill_id: str) -> dict[str, Any] | None:
    for s in list_skills():
        if s["id"] == skill_id:
            return s
    return None


def skills_for_mode(mode: str) -> list[dict[str, Any]]:
    return [s for s in list_skills() if mode in s.get("modes", [])]


def get_pipeline(name: str) -> list[str]:
    pipes = load_registry().get("pipelines", {})
    return list(pipes.get(name, []))


def skill_md_path(skill_id: str) -> Path | None:
    s = get_skill(skill_id)
    if not s:
        return None
    p = ROOT / s["path"] / "SKILL.md"
    return p if p.exists() else None


def read_skill_body(skill_id: str) -> str:
    p = skill_md_path(skill_id)
    if not p:
        return f"# مهارة مفقودة: {skill_id}\n"
    return p.read_text(encoding="utf-8")


def validate_skills_on_disk() -> list[str]:
    """يعيد قائمة أخطاء (فارغة = سليم)."""
    errors: list[str] = []
    if not SKILLS_DIR.exists():
        return ["مجلد skills غير موجود"]
    for s in list_skills():
        p = ROOT / s["path"] / "SKILL.md"
        if not p.exists():
            errors.append(f"مفقود: {p}")
    return errors
