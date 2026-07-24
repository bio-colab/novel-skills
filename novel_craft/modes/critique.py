"""وضع النقد الطبقي."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from novel_craft.orchestrator import Orchestrator
from novel_craft.storage.project import ProjectStore

PrintFn = Callable[[str], None]


def run_critique_prep(
    project: ProjectStore,
    draft_path: str | Path | None = None,
    *,
    emit: PrintFn | None = None,
) -> Path:
    emit = emit or print
    cdir = project.root / "critique"
    cdir.mkdir(exist_ok=True)

    if draft_path:
        src = Path(draft_path)
        text = src.read_text(encoding="utf-8")
        target = cdir / "draft_under_review.txt"
        target.write_text(text, encoding="utf-8")
    else:
        target = cdir / "draft_under_review.txt"
        if not target.exists():
            # حاول drafts/
            drafts = list((project.root / "drafts").glob("**/*"))
            drafts = [d for d in drafts if d.is_file()]
            if drafts:
                target.write_text(drafts[0].read_text(encoding="utf-8"), encoding="utf-8")
                emit(f"استُخدمت المسودة: {drafts[0]}")
            else:
                target.write_text("# الصق المسودة هنا للمراجعة\n", encoding="utf-8")

    rubric = cdir / "RUBRIC.md"
    rubric.write_text(
        "\n".join(
            [
                "# معيار النقد الطبقي (Definition of Done)",
                "",
                "لكل مشهد/فصل راجع:",
                "",
                "1. رغبة شخصية واضحة في الوحدة النصية",
                "2. عائق حقيقي (داخلي أو خارجي)",
                "3. تحوّل في قيمة أو علاقة أو معلومة",
                "4. سبتيكست أو توتر ظاهر/باطن",
                "5. البيئة تفعل شيئًا (لا ديكور فقط)",
                "6. صوت متسق مع بطاقة الشخصية",
                "7. الثيم يُختبر بالفعل لا بالخطبة",
                "8. ارتباط سببي بما سبق وما يلي",
                "",
                "صيغة التقرير: نقاط قوة → فجوات → أمثلة نصية → مقترحات اختيارية",
                "",
            ]
        ),
        encoding="utf-8",
    )

    project.update_meta(mode="critique", status="revising")
    orch = Orchestrator(project)
    plan = orch.build_plan(mode="critique")
    briefs = project.root / "plans" / "briefs"
    briefs.mkdir(parents=True, exist_ok=True)
    for item in plan.items:
        if item.status == "pending":
            (briefs / f"{item.skill_id}.md").write_text(
                orch.export_agent_brief(item.skill_id), encoding="utf-8"
            )

    project.journal.log(
        actor="orchestrator",
        action="critique.prep",
        mode="critique",
        summary="تجهيز النقد الطبقي",
        outputs={"draft": str(target)},
    )
    emit(f"المسودة قيد النقد: {target}")
    emit("استخدم skill-revision-critique مع RUBRIC.md")
    return target
