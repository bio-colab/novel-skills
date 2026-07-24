"""وضع تحليل رواية موجودة."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from novel_craft.orchestrator import Orchestrator
from novel_craft.storage.project import ProjectStore

PrintFn = Callable[[str], None]


def run_analyze_prep(
    project: ProjectStore,
    source_text: str | None = None,
    source_path: str | Path | None = None,
    *,
    emit: PrintFn | None = None,
) -> Path:
    emit = emit or print
    analysis_dir = project.root / "analysis"
    analysis_dir.mkdir(exist_ok=True)

    if source_path:
        src = Path(source_path)
        text = src.read_text(encoding="utf-8")
        dest = analysis_dir / "source.txt"
        dest.write_text(text, encoding="utf-8")
        emit(f"نُسخ النص من {src} → {dest}")
    elif source_text:
        dest = analysis_dir / "source.txt"
        dest.write_text(source_text, encoding="utf-8")
        emit(f"حُفظ النص في {dest}")
    else:
        dest = analysis_dir / "source.txt"
        if not dest.exists():
            dest.write_text(
                "# الصق هنا نص الرواية أو الفصل المراد تحليله\n",
                encoding="utf-8",
            )
            emit(f"أنشئ قالب المصدر: {dest} — الصق النص ثم أعد التشغيل أو مرّر --source")

    checklist = analysis_dir / "ANALYSIS_CHECKLIST.md"
    checklist.write_text(
        "\n".join(
            [
                "# قائمة تحليل طبقية",
                "",
                "املأ بعد تشغيل المهارات (أو اطلب من الوكيل اتباع skill-analyze-novel):",
                "",
                "## 1. المادة والحبكة (Fabula / Syuzhet)",
                "- [ ] ملخص الأحداث الزمني",
                "- [ ] ترتيب السرد والانحرافات",
                "- [ ] الحدث المحرّك / الذروة / الأثر",
                "",
                "## 2. الشخصيات",
                "- [ ] بطاقات مختصرة",
                "- [ ] رغبة / حاجة / تناقض",
                "- [ ] أقواس أو ثبات مأساوي",
                "",
                "## 3. الصوت والسرد",
                "- [ ] الراوي والمصداقية",
                "- [ ] التبئير",
                "- [ ] الأسلوب غير المباشر الحر",
                "",
                "## 4. السبتيكست والثيم",
                "- [ ] أسئلة العمل لا شعاراته",
                "- [ ] مفارقات",
                "- [ ] ما يُلمَّح ولا يُقال",
                "",
                "## 5. البيئة",
                "- [ ] المكان كفاعل",
                "- [ ] الضغط الاجتماعي–التاريخي",
                "",
                "## 6. الشعرية",
                "- [ ] موتيفات",
                "- [ ] إيقاع",
                "- [ ] تغريب / عجائبي",
                "",
                "## 7. حكم نقدي مركّب",
                "- [ ] نقاط القوة",
                "- [ ] فجوات الحرفة",
                "- [ ] مقترحات (إن طُلبت) دون إعادة كتابة قسرية",
                "",
            ]
        ),
        encoding="utf-8",
    )

    project.update_meta(mode="analyze", status="analyzing")
    orch = Orchestrator(project)
    plan = orch.build_plan(mode="analyze")
    briefs = project.root / "plans" / "briefs"
    briefs.mkdir(parents=True, exist_ok=True)
    for item in plan.items:
        if item.status == "pending":
            (briefs / f"{item.skill_id}.md").write_text(
                orch.export_agent_brief(item.skill_id), encoding="utf-8"
            )
            emit(f"  • موجز: {item.skill_id}")

    project.journal.log(
        actor="orchestrator",
        action="analyze.prep",
        mode="analyze",
        summary="تجهيز وضع التحليل + خطة المهارات",
        outputs={"source": str(dest), "plan": "plans/latest.yaml"},
    )
    emit("التجهيز جاهز. مرّر موجزات plans/briefs/ لوكيل AI مع analysis/source.txt")
    return dest
