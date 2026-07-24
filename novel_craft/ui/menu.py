"""واجهة اختيار تفاعلية (Rich إن توفّر)."""

from __future__ import annotations

from typing import Callable

from novel_craft.orchestrator import catalog_text, modes_help
from novel_craft.paths import PROJECTS_DIR, ensure_layout
from novel_craft.registry import list_skills, validate_skills_on_disk
from novel_craft.storage.project import ProjectStore, list_projects

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.markdown import Markdown

    HAS_RICH = True
    console = Console()
except ImportError:  # pragma: no cover
    HAS_RICH = False
    console = None  # type: ignore


def _print(msg: str = "") -> None:
    if HAS_RICH:
        console.print(msg)
    else:
        print(msg)


def _ask(prompt: str) -> str:
    if HAS_RICH:
        return console.input(f"[bold cyan]{prompt}[/] ").strip()
    return input(f"{prompt} ").strip()


def _header() -> None:
    title = "حرفة الرواية — Novel Craft v0.1"
    if HAS_RICH:
        console.print(Panel.fit(f"[bold]{title}[/]\nنظام مفتوح المصدر للكتابة والتحليل والنقد", border_style="magenta"))
    else:
        _print("=" * 60)
        _print(title)
        _print("=" * 60)


def _pick_project() -> ProjectStore | None:
    projects = list_projects()
    if not projects:
        _print("لا مشاريع بعد. أنشئ مشروعًا أولًا.")
        return None
    _print("\nالمشاريع:")
    for i, p in enumerate(projects, 1):
        _print(f"  {i}. {p.name}")
    choice = _ask("رقم المشروع:")
    try:
        idx = int(choice) - 1
        return ProjectStore.open(projects[idx])
    except (ValueError, IndexError):
        _print("اختيار غير صالح.")
        return None


def _create_project() -> ProjectStore:
    title = _ask("عنوان الرواية/المشروع:") or "رواية بلا عنوان"
    _print("الأوضاع: write | analyze | critique | interview | free")
    mode = _ask("الوضع الابتدائي [write]:") or "write"
    lang = _ask("اللغة [ar]:") or "ar"
    lenses = _ask("عدسات (مثال: arabic,russian) أو فراغ:")
    lens_list = [x.strip() for x in lenses.split(",") if x.strip()]
    store = ProjectStore.create(title, mode=mode, language=lang, lenses=lens_list)
    _print(f"أُنشئ: {store.root}")
    return store


def run_interactive_menu() -> int:
    ensure_layout()
    _header()

    actions: dict[str, Callable[[], None]] = {}

    def do_create() -> None:
        _create_project()

    def do_interview() -> None:
        from novel_craft.modes.interview import run_interview

        proj = _pick_project() or _create_project()
        run_interview(proj, ask=lambda p: _ask(p), emit=_print)

    def do_write() -> None:
        from novel_craft.modes.write_mode import run_write_bootstrap

        proj = _pick_project()
        if not proj:
            return
        vision = proj.root / "vision" / "vision.yaml"
        if not vision.exists():
            _print("لا يوجد vision — يُفضَّل بدء مقابلة أولًا.")
            if (_ask("بدء المقابلة الآن؟ [y/N]:") or "n").lower() in ("y", "yes", "ن", "نعم"):
                from novel_craft.modes.interview import run_interview

                run_interview(proj, ask=lambda p: _ask(p), emit=_print)
        run_write_bootstrap(proj, emit=_print)

    def do_analyze() -> None:
        from novel_craft.modes.analyze import run_analyze_prep

        proj = _pick_project() or _create_project()
        src = _ask("مسار ملف النص (أو فراغ لقالب):")
        run_analyze_prep(proj, source_path=src or None, emit=_print)

    def do_critique() -> None:
        from novel_craft.modes.critique import run_critique_prep

        proj = _pick_project()
        if not proj:
            return
        src = _ask("مسار المسودة (أو فراغ):")
        run_critique_prep(proj, draft_path=src or None, emit=_print)

    def do_status() -> None:
        projects = list_projects()
        if HAS_RICH:
            table = Table(title="المشاريع")
            table.add_column("المعرف")
            table.add_column("العنوان")
            table.add_column("الوضع")
            table.add_column("الحالة")
            for p in projects:
                store = ProjectStore.open(p)
                m = store.load_meta()
                table.add_row(m.get("id", ""), m.get("title", ""), m.get("mode", ""), m.get("status", ""))
            console.print(table)
        else:
            for p in projects:
                store = ProjectStore.open(p)
                m = store.load_meta()
                _print(f"- {m.get('id')}: {m.get('title')} [{m.get('mode')}/{m.get('status')}]")
        if not projects:
            _print("(لا مشاريع)")

    def do_skills() -> None:
        if HAS_RICH:
            console.print(Markdown(catalog_text()))
        else:
            _print(catalog_text())
        errs = validate_skills_on_disk()
        if errs:
            _print("تحذيرات:")
            for e in errs:
                _print(f"  ! {e}")
        else:
            _print(f"\nكل المهارات موجودة على القرص ({len(list_skills())}).")

    def do_journal() -> None:
        proj = _pick_project()
        if not proj:
            return
        for e in proj.journal.tail(25):
            _print(f"[{e.get('timestamp','')[:19]}] {e.get('actor')}: {e.get('summary')}")
        path = proj.journal.write_markdown_report()
        _print(f"تقرير: {path}")

    def do_plan() -> None:
        from novel_craft.orchestrator import Orchestrator

        proj = _pick_project()
        if not proj:
            return
        mode = _ask("وضع الخطة [من meta]:") or None
        orch = Orchestrator(proj)
        plan = orch.build_plan(mode=mode)
        _print(plan.rationale)
        for item in plan.items:
            _print(f"  [{item.status}] {item.skill_id} (p={item.priority}) — {item.notes or item.reason}")

    def do_modes() -> None:
        for mid, desc in modes_help():
            _print(f"  {mid:12} {desc}")

    def do_quit() -> None:
        raise SystemExit(0)

    menu = [
        ("1", "إنشاء مشروع جديد", do_create),
        ("2", "مقابلة الكاتب (دردشة أسئلة → vision)", do_interview),
        ("3", "وضع الكتابة (خطة bootstrap + موجزات)", do_write),
        ("4", "تحليل رواية", do_analyze),
        ("5", "نقد / مراجعة مسودة", do_critique),
        ("6", "عرض المشاريع (status)", do_status),
        ("7", "كتالوج المهارات", do_skills),
        ("8", "سجل العقل المُدير (journal)", do_journal),
        ("9", "إعادة بناء خطة المُدير", do_plan),
        ("m", "شرح الأوضاع", do_modes),
        ("0", "خروج", do_quit),
    ]

    while True:
        _print("\n— القائمة —")
        for key, label, _ in menu:
            _print(f"  [{key}] {label}")
        choice = _ask("اختيارك:")
        matched = False
        for key, _, fn in menu:
            if choice == key:
                matched = True
                try:
                    fn()
                except SystemExit:
                    _print("إلى اللقاء.")
                    return 0
                except Exception as exc:  # noqa: BLE001
                    _print(f"خطأ: {exc}")
                break
        if not matched:
            _print("اختيار غير معروف.")
