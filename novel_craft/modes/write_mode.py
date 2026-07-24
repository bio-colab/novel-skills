"""وضع الكتابة — تجهيز المسار بعد/بدون مقابلة."""

from __future__ import annotations

from typing import Callable

from novel_craft.orchestrator import Orchestrator
from novel_craft.storage.project import ProjectStore

PrintFn = Callable[[str], None]


def run_write_bootstrap(project: ProjectStore, *, emit: PrintFn | None = None) -> None:
    emit = emit or print
    project.update_meta(mode="write", status="planning")
    orch = Orchestrator(project)
    plan = orch.build_plan(mode="write", phase="write_bootstrap")
    briefs = project.root / "plans" / "briefs"
    briefs.mkdir(parents=True, exist_ok=True)
    emit(f"[العقل المُدير] {plan.rationale}")
    for item in plan.items:
        if item.status != "pending":
            emit(f"  (تخطي) {item.skill_id}: {item.reason}")
            continue
        (briefs / f"{item.skill_id}.md").write_text(
            orch.export_agent_brief(item.skill_id), encoding="utf-8"
        )
        emit(f"  • {item.skill_id} — {item.notes}")
    # هياكل فارغة إرشادية
    if not (project.root / "characters" / "README.md").exists():
        project.write_text(
            "characters/README.md",
            "# الشخصيات\n\nضع بطاقة YAML لكل شخصية: `char_<id>.yaml` وفق schema character.\n",
        )
    if not (project.root / "plot" / "README.md").exists():
        project.write_text(
            "plot/README.md",
            "# الحبكة\n\n`plot.yaml` للعمود الفقري + ملفات خيوط فرعية عند الحاجة.\n",
        )
    if not (project.root / "world" / "README.md").exists():
        project.write_text(
            "world/README.md",
            "# العالم\n\nمكان، زمن، أنظمة اجتماعية، رموز.\n",
        )
    project.journal.log(
        actor="orchestrator",
        action="write.bootstrap",
        mode="write",
        summary="تجهيز مسار الكتابة الأساسي",
    )
    emit("الخطوة التالية المقترحة: مقابلة (interview) إن لم تُحفظ vision، ثم تنفيذ الموجزات مع الوكيل.")
