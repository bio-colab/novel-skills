"""العقل المُدير — يقرر من يعمل ومتى وكيف، ويوثّق كل شيء."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from novel_craft.registry import get_pipeline, get_skill, list_skills, skills_for_mode
from novel_craft.storage.project import ProjectStore


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class WorkItem:
    skill_id: str
    reason: str
    priority: int = 50
    status: str = "pending"  # pending | active | done | skipped
    depends_on: list[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class OrchestratorPlan:
    mode: str
    created_at: str
    project_id: str
    pipeline_name: str
    items: list[WorkItem]
    active_lenses: list[str] = field(default_factory=list)
    rationale: str = ""
    state_summary: str = ""


class Orchestrator:
    """
    عقل إداري لا يكتب الأدب بنفسه؛ ينسّق المهارات ويحفظ الخطط والسجل.

    قواعد بسيطة:
    - كل وضع له pipeline افتراضي.
    - العدسات تُضاف كخطوات اختيارية حسب إعداد المشروع.
    - لا تُفعَّل مهارة غير مناسبة للوضع.
    - كل قرار يُسجَّل في journal.
    """

    MODE_PIPELINE = {
        "interview": "interview",
        "write": "write_bootstrap",
        "analyze": "analyze",
        "critique": "critique",
        "free": "write_draft_loop",
    }

    def __init__(self, project: ProjectStore) -> None:
        self.project = project
        self.meta = project.load_meta()

    def build_plan(
        self,
        mode: str | None = None,
        phase: str | None = None,
        extra_skills: list[str] | None = None,
    ) -> OrchestratorPlan:
        mode = mode or self.meta.get("mode", "write")
        if phase:
            pipeline_name = phase
        else:
            pipeline_name = self.MODE_PIPELINE.get(mode, "write_bootstrap")

        skill_ids = get_pipeline(pipeline_name)
        # عدسات
        lenses = list(self.meta.get("tradition_lenses") or [])
        for lens in lenses:
            lid = lens if lens.startswith("lens-") else f"lens-{lens}"
            # تطبيع
            aliases = {
                "lens-arabic": "lens-arabic-heritage",
                "lens-arabic-heritage": "lens-arabic-heritage",
                "arabic": "lens-arabic-heritage",
                "russian": "lens-russian-polyphonic",
                "lens-russian": "lens-russian-polyphonic",
                "lens-russian-polyphonic": "lens-russian-polyphonic",
                "anglophone": "lens-anglophone-craft",
                "lens-anglophone": "lens-anglophone-craft",
                "lens-anglophone-craft": "lens-anglophone-craft",
                "classical": "lens-classical-poetics",
                "lens-classical": "lens-classical-poetics",
                "lens-classical-poetics": "lens-classical-poetics",
            }
            lid = aliases.get(lid, aliases.get(lens, lid))
            if lid not in skill_ids and get_skill(lid):
                skill_ids.append(lid)

        if extra_skills:
            for s in extra_skills:
                if s not in skill_ids:
                    skill_ids.append(s)

        items: list[WorkItem] = []
        for i, sid in enumerate(skill_ids):
            sk = get_skill(sid)
            if not sk:
                items.append(
                    WorkItem(
                        skill_id=sid,
                        reason="غير موجود في السجل",
                        priority=0,
                        status="skipped",
                    )
                )
                continue
            if mode not in sk.get("modes", []) and mode != "free":
                # free يسمح بكل شيء تقريبًا
                if "free" not in sk.get("modes", []):
                    items.append(
                        WorkItem(
                            skill_id=sid,
                            reason=f"المهارة لا تدعم الوضع {mode}",
                            priority=0,
                            status="skipped",
                        )
                    )
                    continue
            items.append(
                WorkItem(
                    skill_id=sid,
                    reason=sk.get("description", ""),
                    priority=100 - i,
                    status="pending",
                    notes=sk.get("name_ar", ""),
                )
            )

        state = self._state_summary()
        plan = OrchestratorPlan(
            mode=mode,
            created_at=_utc_now(),
            project_id=self.meta.get("id", self.project.root.name),
            pipeline_name=pipeline_name,
            items=items,
            active_lenses=lenses,
            rationale=self._rationale(mode, pipeline_name, items),
            state_summary=state,
        )

        self.project.save_plan(self._plan_to_dict(plan), name="latest")
        self.project.journal.log(
            actor="orchestrator",
            action="plan.build",
            mode=mode,
            summary=f"بناء خطة pipeline={pipeline_name} بعدد {len(items)} مهارة",
            details={"pipeline": pipeline_name, "skills": [i.skill_id for i in items]},
            outputs={"plan": "plans/latest.yaml"},
        )
        self.project.update_meta(
            mode=mode,
            active_skills=[i.skill_id for i in items if i.status == "pending"],
        )
        return plan

    def mark_skill(
        self,
        skill_id: str,
        status: str,
        summary: str,
        outputs: dict[str, Any] | None = None,
    ) -> None:
        self.project.journal.log(
            actor=f"skill:{skill_id}",
            action=f"skill.{status}",
            mode=self.meta.get("mode", ""),
            summary=summary,
            outputs=outputs or {},
            status="ok" if status in ("done", "active") else status,
        )

    def next_skill(self, plan: OrchestratorPlan | None = None) -> WorkItem | None:
        if plan is None:
            plan_path = self.project.root / "plans" / "latest.yaml"
            if not plan_path.exists():
                plan = self.build_plan()
            else:
                import yaml

                raw = yaml.safe_load(plan_path.read_text(encoding="utf-8"))
                plan = self._plan_from_dict(raw)
        for item in plan.items:
            if item.status == "pending":
                return item
        return None

    def suggest_phase_after_interview(self) -> OrchestratorPlan:
        """بعد المقابلة: انتقال لبناء الأساس."""
        self.project.update_meta(status="planning")
        return self.build_plan(mode="write", phase="write_bootstrap")

    def suggest_draft_loop(self) -> OrchestratorPlan:
        self.project.update_meta(status="drafting")
        return self.build_plan(mode="write", phase="write_draft_loop")

    def suggest_polish(self) -> OrchestratorPlan:
        self.project.update_meta(status="revising")
        return self.build_plan(mode="write", phase="write_polish")

    def export_agent_brief(self, skill_id: str) -> str:
        """نص جاهز لتمريره لوكيل AI مع سياق المشروع."""
        from novel_craft.registry import read_skill_body

        meta = self.project.load_meta()
        vision_path = self.project.root / "vision" / "VISION.md"
        vision = vision_path.read_text(encoding="utf-8") if vision_path.exists() else "(لا يوجد vision بعد)"
        skill_body = read_skill_body(skill_id)
        recent = self.project.journal.tail(10)
        recent_txt = "\n".join(
            f"- [{e.get('timestamp','')[:19]}] {e.get('actor')}: {e.get('summary')}" for e in recent
        )
        return (
            f"# موجز العقل المُدير للمهارة: {skill_id}\n\n"
            f"## المشروع\n"
            f"- العنوان: {meta.get('title')}\n"
            f"- الوضع: {meta.get('mode')} / الحالة: {meta.get('status')}\n"
            f"- العدسات: {meta.get('tradition_lenses')}\n"
            f"- المسار: {self.project.root}\n\n"
            f"## التصوّر (Vision)\n{vision}\n\n"
            f"## آخر أحداث السجل\n{recent_txt or '(فارغ)'}\n\n"
            f"## تعليمات المهارة\n\n{skill_body}\n"
        )

    def _state_summary(self) -> str:
        parts = []
        for sub in ("vision", "characters", "plot", "scenes", "drafts", "analysis"):
            files = self.project.list_files(sub)
            parts.append(f"{sub}:{len(files)}")
        return ", ".join(parts)

    def _rationale(self, mode: str, pipeline: str, items: list[WorkItem]) -> str:
        pending = [i.skill_id for i in items if i.status == "pending"]
        return (
            f"الوضع={mode}. pipeline={pipeline}. "
            f"المهارات المفعّلة بالترتيب: {', '.join(pending)}. "
            f"كل مهارة تُنفَّذ عبر وكيل يقرأ SKILL.md + ملفات المشروع، "
            f"ثم يُوثَّق الناتج في المجلد المناسب وفي journal."
        )

    @staticmethod
    def _plan_to_dict(plan: OrchestratorPlan) -> dict[str, Any]:
        return {
            "mode": plan.mode,
            "created_at": plan.created_at,
            "project_id": plan.project_id,
            "pipeline_name": plan.pipeline_name,
            "active_lenses": plan.active_lenses,
            "rationale": plan.rationale,
            "state_summary": plan.state_summary,
            "items": [asdict(i) for i in plan.items],
        }

    @staticmethod
    def _plan_from_dict(raw: dict[str, Any]) -> OrchestratorPlan:
        items = [WorkItem(**i) for i in raw.get("items", [])]
        return OrchestratorPlan(
            mode=raw.get("mode", ""),
            created_at=raw.get("created_at", ""),
            project_id=raw.get("project_id", ""),
            pipeline_name=raw.get("pipeline_name", ""),
            items=items,
            active_lenses=raw.get("active_lenses", []),
            rationale=raw.get("rationale", ""),
            state_summary=raw.get("state_summary", ""),
        )


def catalog_text() -> str:
    lines = ["# كتالوج المهارات", ""]
    for s in list_skills():
        lines.append(f"- **{s['id']}** — {s.get('name_ar','')}: {s.get('description','')}")
    return "\n".join(lines)


def modes_help() -> list[tuple[str, str]]:
    return [
        ("interview", "مقابلة الكاتب: أسئلة لفهم التصوّر الكامل وحفظ vision"),
        ("write", "كتابة رواية: من المقابلة إلى العالم والشخصيات والحبكة والمشاهد"),
        ("analyze", "تحليل رواية موجودة عبر الطبقات (حبكة، شخصيات، صوت، سبتيكست…)"),
        ("critique", "نقد ومراجعة طبقية لمسودة أو نص"),
        ("free", "وضع حر: اختيار مهارة أو مسار يدويًا"),
        ("status", "عرض المشاريع والسجل والخطط"),
    ]
