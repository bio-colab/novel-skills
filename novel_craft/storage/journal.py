"""سجل العقل المُدير — توثيق من عمل ومتى وكيف وماذا."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class JournalEntry:
    id: str
    timestamp: str
    actor: str  # orchestrator | skill:<id> | user | system
    action: str
    mode: str
    summary: str
    details: dict[str, Any] = field(default_factory=dict)
    inputs: dict[str, Any] = field(default_factory=dict)
    outputs: dict[str, Any] = field(default_factory=dict)
    status: str = "ok"  # ok | planned | failed | skipped


class Journal:
    """يلتزم بملف journal/events.jsonl + ملخص يومي اختياري."""

    def __init__(self, project_root: Path) -> None:
        self.root = Path(project_root)
        self.dir = self.root / "journal"
        self.events_path = self.dir / "events.jsonl"
        self.dir.mkdir(parents=True, exist_ok=True)
        if not self.events_path.exists():
            self.events_path.write_text("", encoding="utf-8")

    def log(
        self,
        *,
        actor: str,
        action: str,
        mode: str,
        summary: str,
        details: dict[str, Any] | None = None,
        inputs: dict[str, Any] | None = None,
        outputs: dict[str, Any] | None = None,
        status: str = "ok",
    ) -> JournalEntry:
        entry = JournalEntry(
            id=str(uuid4()),
            timestamp=_utc_now(),
            actor=actor,
            action=action,
            mode=mode,
            summary=summary,
            details=details or {},
            inputs=inputs or {},
            outputs=outputs or {},
            status=status,
        )
        with self.events_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")
        return entry

    def read_all(self) -> list[dict[str, Any]]:
        if not self.events_path.exists():
            return []
        rows: list[dict[str, Any]] = []
        for line in self.events_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
        return rows

    def tail(self, n: int = 20) -> list[dict[str, Any]]:
        return self.read_all()[-n:]

    def write_markdown_report(self, path: Path | None = None) -> Path:
        """تقرير مقروء للمجتمع الأدبي / الأرشيف."""
        path = path or (self.dir / "REPORT.md")
        rows = self.read_all()
        lines = [
            "# تقرير نشاط المشروع",
            "",
            f"عدد الأحداث: {len(rows)}",
            "",
            "| الوقت | الفاعل | الإجراء | الوضع | الملخص | الحالة |",
            "|-------|--------|---------|-------|--------|--------|",
        ]
        for r in rows:
            ts = r.get("timestamp", "")[:19]
            lines.append(
                f"| {ts} | {r.get('actor','')} | {r.get('action','')} | "
                f"{r.get('mode','')} | {r.get('summary','').replace('|', '/')} | {r.get('status','')} |"
            )
        lines.append("")
        path.write_text("\n".join(lines), encoding="utf-8")
        return path
