"""اختبارات دخان أساسية."""

from pathlib import Path

from novel_craft.orchestrator import Orchestrator
from novel_craft.paths import ROOT
from novel_craft.registry import list_skills, validate_skills_on_disk
from novel_craft.storage.project import ProjectStore


def test_skills_on_disk():
    errs = validate_skills_on_disk()
    assert errs == [], errs


def test_registry_not_empty():
    assert len(list_skills()) >= 15


def test_create_project_and_plan(tmp_path, monkeypatch):
    import novel_craft.paths as paths
    import novel_craft.storage.project as project_mod

    monkeypatch.setattr(paths, "PROJECTS_DIR", tmp_path / "projects")
    monkeypatch.setattr(project_mod, "PROJECTS_DIR", tmp_path / "projects")
    paths.PROJECTS_DIR.mkdir(parents=True)

    store = ProjectStore.create("اختبار", mode="write", lenses=["arabic"])
    assert (store.root / "project.yaml").exists()
    orch = Orchestrator(store)
    plan = orch.build_plan()
    assert plan.pipeline_name == "write_bootstrap"
    assert any(i.skill_id == "skill-character-patterns" for i in plan.items)
    assert (store.root / "plans" / "latest.yaml").exists()
    assert store.journal.tail(5)


def test_foundation_exists():
    assert (ROOT / "00-foundation" / "README.md").exists()
