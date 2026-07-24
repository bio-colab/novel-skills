"""إدارة ملفات مشاريع الرواية."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from novel_craft.paths import PROJECTS_DIR, ensure_layout
from novel_craft.storage.journal import Journal


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _slugify(title: str) -> str:
    s = title.strip().lower()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^\w\-ء-ي]+", "", s, flags=re.UNICODE)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "project"


def list_projects() -> list[Path]:
    ensure_layout()
    if not PROJECTS_DIR.exists():
        return []
    return sorted(
        [p for p in PROJECTS_DIR.iterdir() if p.is_dir() and (p / "project.yaml").exists()],
        key=lambda p: p.name,
    )


class ProjectStore:
    SUBDIRS = (
        "characters",
        "plot",
        "scenes",
        "world",
        "drafts",
        "analysis",
        "critique",
        "journal",
        "vision",
        "plans",
        "exports",
    )

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.meta_path = self.root / "project.yaml"
        self.journal = Journal(self.root)

    @classmethod
    def create(
        cls,
        title: str,
        mode: str = "write",
        language: str = "ar",
        lenses: list[str] | None = None,
    ) -> "ProjectStore":
        ensure_layout()
        slug = _slugify(title)
        root = PROJECTS_DIR / slug
        n = 1
        while root.exists():
            root = PROJECTS_DIR / f"{slug}-{n}"
            n += 1
        root.mkdir(parents=True)
        store = cls(root)
        for sub in cls.SUBDIRS:
            (root / sub).mkdir(exist_ok=True)
        meta = {
            "schema_version": "0.1",
            "type": "project",
            "id": root.name,
            "title": title,
            "created_at": _utc_now(),
            "updated_at": _utc_now(),
            "mode": mode,
            "language": language,
            "genre_hints": [],
            "tradition_lenses": lenses or [],
            "logline": "",
            "status": "interview" if mode in ("write", "interview") else mode,
            "paths": {s: s for s in cls.SUBDIRS},
            "active_skills": [],
            "last_orchestrator_plan": "",
        }
        store.save_meta(meta)
        store.journal.log(
            actor="system",
            action="project.create",
            mode=mode,
            summary=f"إنشاء مشروع: {title}",
            outputs={"path": str(root)},
        )
        readme = root / "README.md"
        readme.write_text(
            f"# {title}\n\n"
            f"- الوضع الابتدائي: `{mode}`\n"
            f"- أُنشئ: {meta['created_at']}\n\n"
            "المجلدات: characters, plot, scenes, world, drafts, analysis, critique, journal, vision, plans\n",
            encoding="utf-8",
        )
        return store

    @classmethod
    def open(cls, name_or_path: str | Path) -> "ProjectStore":
        p = Path(name_or_path)
        if not p.is_absolute() and not p.exists():
            p = PROJECTS_DIR / name_or_path
        if not (p / "project.yaml").exists():
            raise FileNotFoundError(f"لا يوجد مشروع في: {p}")
        return cls(p)

    def load_meta(self) -> dict[str, Any]:
        with self.meta_path.open(encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def save_meta(self, meta: dict[str, Any]) -> None:
        meta["updated_at"] = _utc_now()
        with self.meta_path.open("w", encoding="utf-8") as f:
            yaml.dump(meta, f, allow_unicode=True, sort_keys=False)

    def update_meta(self, **kwargs: Any) -> dict[str, Any]:
        meta = self.load_meta()
        meta.update(kwargs)
        self.save_meta(meta)
        return meta

    def write_yaml(self, relative: str, data: dict[str, Any] | list[Any]) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)
        return path

    def write_text(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def read_text(self, relative: str) -> str:
        return (self.root / relative).read_text(encoding="utf-8")

    def list_files(self, subdir: str) -> list[Path]:
        d = self.root / subdir
        if not d.exists():
            return []
        return sorted([p for p in d.rglob("*") if p.is_file()])

    def save_vision(self, answers: dict[str, Any]) -> Path:
        payload = {
            "schema_version": "0.1",
            "type": "vision",
            "saved_at": _utc_now(),
            "answers": answers,
        }
        path = self.write_yaml("vision/vision.yaml", payload)
        # نسخة مقروءة
        lines = ["# تصوّر الرواية (Vision)", ""]
        for k, v in answers.items():
            lines.append(f"## {k}")
            lines.append("")
            lines.append(str(v) if v else "—")
            lines.append("")
        self.write_text("vision/VISION.md", "\n".join(lines))
        self.journal.log(
            actor="skill:skill-interview-author",
            action="vision.save",
            mode=self.load_meta().get("mode", "interview"),
            summary="حفظ تصوّر الكاتب من المقابلة",
            outputs={"path": str(path)},
        )
        return path

    def save_plan(self, plan: dict[str, Any], name: str = "latest") -> Path:
        path = self.write_yaml(f"plans/{name}.yaml", plan)
        self.update_meta(last_orchestrator_plan=f"plans/{name}.yaml")
        return path
