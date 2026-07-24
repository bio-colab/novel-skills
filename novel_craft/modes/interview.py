"""وضع المقابلة — دردشة أسئلة لفهم تصوّر الكاتب."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

import yaml

from novel_craft.orchestrator import Orchestrator
from novel_craft.paths import DATA_DIR
from novel_craft.storage.project import ProjectStore

PromptFn = Callable[[str], str]
PrintFn = Callable[[str], None]


def load_script() -> dict[str, Any]:
    path = DATA_DIR / "interview_script.yaml"
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def run_interview(
    project: ProjectStore,
    *,
    ask: PromptFn | None = None,
    emit: PrintFn | None = None,
) -> dict[str, Any]:
    """
    يشغّل سكربت المقابلة تفاعليًا.
    ask(prompt) -> answer
    emit(text) للطباعة
    """
    ask = ask or (lambda p: input(f"\n{p}\n> ").strip())
    emit = emit or print

    script = load_script()
    emit(script.get("intro_ar", ""))
    answers: dict[str, Any] = {}

    project.journal.log(
        actor="orchestrator",
        action="interview.start",
        mode="interview",
        summary="بدء مقابلة الكاتب",
    )

    for phase in script.get("phases", []):
        emit(f"\n—— {phase.get('title_ar', phase.get('id'))} ——")
        for q in phase.get("questions", []):
            raw = ask(q.get("prompt_ar", q["id"]))
            if raw in ("تخطَّ", "تخطى", "skip", "s", ""):
                answers[q["field"]] = ""
                project.journal.log(
                    actor="user",
                    action="interview.skip",
                    mode="interview",
                    summary=f"تخطّي: {q['id']}",
                    status="skipped",
                )
                continue
            answers[q["field"]] = raw
            project.journal.log(
                actor="user",
                action="interview.answer",
                mode="interview",
                summary=f"إجابة: {q['id']}",
                details={"field": q["field"], "length": len(raw)},
            )

    emit("\n" + script.get("outro_ar", ""))
    project.save_vision(answers)

    # تحديث meta من الإجابات الأساسية
    lenses_raw = answers.get("tradition_lenses") or ""
    lenses = [x.strip() for x in str(lenses_raw).replace("،", ",").split(",") if x.strip()]
    project.update_meta(
        mode="write",
        status="planning",
        logline=answers.get("logline") or "",
        tradition_lenses=lenses,
    )

    orch = Orchestrator(project)
    plan = orch.suggest_phase_after_interview()
    emit(f"\n[العقل المُدير] الخطة التالية: {plan.pipeline_name}")
    for item in plan.items:
        if item.status == "pending":
            emit(f"  • {item.skill_id} — {item.notes or item.reason}")

    # حفظ موجزات المهارات للوكيل
    briefs_dir = project.root / "plans" / "briefs"
    briefs_dir.mkdir(parents=True, exist_ok=True)
    for item in plan.items:
        if item.status != "pending":
            continue
        brief = orch.export_agent_brief(item.skill_id)
        Path(briefs_dir / f"{item.skill_id}.md").write_text(brief, encoding="utf-8")

    project.journal.log(
        actor="orchestrator",
        action="interview.complete",
        mode="write",
        summary="اكتملت المقابلة وحُفظت vision + خطة bootstrap",
        outputs={"vision": "vision/vision.yaml", "plan": "plans/latest.yaml"},
    )
    return answers
