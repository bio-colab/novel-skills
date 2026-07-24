"""واجهة سطر الأوامر — novel-craft / python -m novel_craft"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from novel_craft import __version__
from novel_craft.paths import PROJECTS_DIR, ensure_layout


def _cmd_menu(_: argparse.Namespace) -> int:
    from novel_craft.ui.menu import run_interactive_menu

    return run_interactive_menu()


def _cmd_new(args: argparse.Namespace) -> int:
    from novel_craft.storage.project import ProjectStore

    lenses = [x.strip() for x in (args.lenses or "").split(",") if x.strip()]
    store = ProjectStore.create(
        args.title,
        mode=args.mode,
        language=args.language,
        lenses=lenses,
    )
    print(f"أُنشئ المشروع: {store.root}")
    return 0


def _cmd_interview(args: argparse.Namespace) -> int:
    from novel_craft.modes.interview import run_interview
    from novel_craft.storage.project import ProjectStore

    store = ProjectStore.open(args.project)
    run_interview(store)
    return 0


def _cmd_write(args: argparse.Namespace) -> int:
    from novel_craft.modes.write_mode import run_write_bootstrap
    from novel_craft.orchestrator import Orchestrator
    from novel_craft.storage.project import ProjectStore

    store = ProjectStore.open(args.project)
    if args.phase == "draft":
        orch = Orchestrator(store)
        plan = orch.suggest_draft_loop()
        print(plan.rationale)
        for i in plan.items:
            if i.status == "pending":
                print(f"  • {i.skill_id}")
        return 0
    if args.phase == "polish":
        orch = Orchestrator(store)
        plan = orch.suggest_polish()
        print(plan.rationale)
        return 0
    run_write_bootstrap(store)
    return 0


def _cmd_analyze(args: argparse.Namespace) -> int:
    from novel_craft.modes.analyze import run_analyze_prep
    from novel_craft.storage.project import ProjectStore

    store = ProjectStore.open(args.project)
    run_analyze_prep(store, source_path=args.source)
    return 0


def _cmd_critique(args: argparse.Namespace) -> int:
    from novel_craft.modes.critique import run_critique_prep
    from novel_craft.storage.project import ProjectStore

    store = ProjectStore.open(args.project)
    run_critique_prep(store, draft_path=args.draft)
    return 0


def _cmd_plan(args: argparse.Namespace) -> int:
    from novel_craft.orchestrator import Orchestrator
    from novel_craft.storage.project import ProjectStore

    store = ProjectStore.open(args.project)
    orch = Orchestrator(store)
    plan = orch.build_plan(mode=args.mode, phase=args.pipeline)
    print(f"pipeline: {plan.pipeline_name}")
    print(plan.rationale)
    print("state:", plan.state_summary)
    for item in plan.items:
        print(f"  [{item.status}] p={item.priority:3} {item.skill_id} — {item.notes or item.reason}")
    return 0


def _cmd_brief(args: argparse.Namespace) -> int:
    from novel_craft.orchestrator import Orchestrator
    from novel_craft.storage.project import ProjectStore

    store = ProjectStore.open(args.project)
    orch = Orchestrator(store)
    text = orch.export_agent_brief(args.skill)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"كُتب: {args.out}")
    else:
        print(text)
    return 0


def _cmd_skills(_: argparse.Namespace) -> int:
    from novel_craft.orchestrator import catalog_text
    from novel_craft.registry import list_skills, validate_skills_on_disk

    print(catalog_text())
    errs = validate_skills_on_disk()
    print(f"\nالمسجّلة: {len(list_skills())}")
    if errs:
        print("نواقص:")
        for e in errs:
            print(" -", e)
        return 1
    print("كل ملفات SKILL.md موجودة.")
    return 0


def _cmd_list(_: argparse.Namespace) -> int:
    from novel_craft.storage.project import ProjectStore, list_projects

    ensure_layout()
    projects = list_projects()
    if not projects:
        print(f"لا مشاريع في {PROJECTS_DIR}")
        return 0
    for p in projects:
        m = ProjectStore.open(p).load_meta()
        print(f"{m.get('id')}\t{m.get('title')}\t{m.get('mode')}/{m.get('status')}")
    return 0


def _cmd_journal(args: argparse.Namespace) -> int:
    from novel_craft.storage.project import ProjectStore

    store = ProjectStore.open(args.project)
    for e in store.journal.tail(args.n):
        print(f"[{e.get('timestamp','')[:19]}] {e.get('actor')}: {e.get('summary')} ({e.get('status')})")
    if args.report:
        path = store.journal.write_markdown_report()
        print(f"REPORT → {path}")
    return 0


def _cmd_doctor(_: argparse.Namespace) -> int:
    from novel_craft.registry import list_skills, validate_skills_on_disk

    ensure_layout()
    print(f"novel-craft {__version__}")
    print(f"projects: {PROJECTS_DIR}")
    errs = validate_skills_on_disk()
    print(f"skills registered: {len(list_skills())}")
    if errs:
        for e in errs:
            print("MISSING:", e)
        return 1
    print("OK — skills on disk match registry")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="novel-craft",
        description="حرفة الرواية — مهارات AI + عقل مُدير + أوضاع كتابة/تحليل/نقد",
    )
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="command")

    m = sub.add_parser("menu", help="واجهة اختيار تفاعلية")
    m.set_defaults(func=_cmd_menu)

    n = sub.add_parser("new", help="إنشاء مشروع")
    n.add_argument("title")
    n.add_argument("--mode", default="write")
    n.add_argument("--language", default="ar")
    n.add_argument("--lenses", default="", help="مثال: arabic,russian")
    n.set_defaults(func=_cmd_new)

    i = sub.add_parser("interview", help="مقابلة الكاتب")
    i.add_argument("project", help="اسم أو مسار المشروع")
    i.set_defaults(func=_cmd_interview)

    w = sub.add_parser("write", help="تجهيز/مراحل الكتابة")
    w.add_argument("project")
    w.add_argument("--phase", choices=["bootstrap", "draft", "polish"], default="bootstrap")
    w.set_defaults(func=_cmd_write)

    a = sub.add_parser("analyze", help="تجهيز تحليل رواية")
    a.add_argument("project")
    a.add_argument("--source", default=None, help="ملف النص")
    a.set_defaults(func=_cmd_analyze)

    c = sub.add_parser("critique", help="تجهيز نقد مسودة")
    c.add_argument("project")
    c.add_argument("--draft", default=None)
    c.set_defaults(func=_cmd_critique)

    pl = sub.add_parser("plan", help="بناء خطة العقل المُدير")
    pl.add_argument("project")
    pl.add_argument("--mode", default=None)
    pl.add_argument("--pipeline", default=None, help="اسم pipeline من السجل")
    pl.set_defaults(func=_cmd_plan)

    b = sub.add_parser("brief", help="موجز مهارة للوكيل")
    b.add_argument("project")
    b.add_argument("skill")
    b.add_argument("--out", default=None)
    b.set_defaults(func=_cmd_brief)

    s = sub.add_parser("skills", help="عرض المهارات")
    s.set_defaults(func=_cmd_skills)

    ls = sub.add_parser("list", help="عرض المشاريع")
    ls.set_defaults(func=_cmd_list)

    j = sub.add_parser("journal", help="سجل الأحداث")
    j.add_argument("project")
    j.add_argument("-n", type=int, default=20)
    j.add_argument("--report", action="store_true")
    j.set_defaults(func=_cmd_journal)

    d = sub.add_parser("doctor", help="فحص صحة التثبيت")
    d.set_defaults(func=_cmd_doctor)

    return p


def main(argv: list[str] | None = None) -> int:
    ensure_layout()
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        # افتراضي: القائمة
        return _cmd_menu(args)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
