# العقل المُدير — Orchestrator

## المهمة

الإجابة عن أربعة أسئلة في كل لحظة عمل:

1. **من** يعمل؟ (أي `skill_id`)  
2. **متى**؟ (ترتيب الأولوية / المرحلة)  
3. **كيف**؟ (pipeline، موجز، قيود)  
4. **ماذا عمل؟** (journal + ملفات مخرجات)

## الملفات

| ملف | دور |
|-----|-----|
| `novel_craft/orchestrator.py` | المنطق |
| `novel_craft/data/skills_registry.yaml` | السجل والـ pipelines |
| `projects/<id>/plans/latest.yaml` | آخر خطة |
| `projects/<id>/plans/briefs/*.md` | موجزات للوكيل |
| `projects/<id>/journal/events.jsonl` | السجل الخام |
| `projects/<id>/journal/REPORT.md` | تقرير مقروء |

## Pipelines الافتراضية

- `interview`  
- `write_bootstrap`  
- `write_draft_loop`  
- `write_polish`  
- `analyze`  
- `critique`  

## أوامر

```bash
python -m novel_craft plan my-novel
python -m novel_craft plan my-novel --pipeline write_draft_loop
python -m novel_craft brief my-novel skill-scene-engine --out brief.md
python -m novel_craft journal my-novel --report
```

## قواعد القرار (مختصر)

- لا مشاهد قبل vision (يُفضّل).  
- التحليل لا يكتب فصولًا جديدة.  
- العدسات من `tradition_lenses` في `project.yaml`.  
- مهارة غير معروفة في السجل → `skipped` مع توثيق.

## للمساهمين

عند إضافة مهارة: سجّلها في `skills_registry.yaml` وأضفها لـ pipeline مناسب واكتب `SKILL.md`.  
