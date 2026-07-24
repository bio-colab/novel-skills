# حرفة الرواية — Novel Craft

**نظام مفتوح المصدر** لكتابة الرواية وتحليلها ونقدها، مبني على قاعدة نظرية عبر التقاليد **العربية والإنجليزية والروسية والكلاسيكية/اللاتينية**، مع:

- **مهارات ذكاء اصطناعي** متخصصة (حبكة، شخصيات، سبتيكست، شعرية…)
- **عقل مُدير (Orchestrator)** يقرر من يعمل ومتى وكيف ويوثّق كل شيء
- **واجهة اختيار** وأوضاع: مقابلة كاتب · كتابة · تحليل · نقد · حر
- **بايثون** لإدارة المشاريع والملفات والخطط والسجلات

> الرخصة: [MIT](LICENSE) — للمجتمع الأدبي ومجتمع المصدر المفتوح.

---

## تثبيت سريع

```bash
cd novel
python -m pip install -r requirements.txt
python -m pip install -e .
python -m novel_craft doctor
python -m novel_craft menu
```

أو بدون تثبيت:

```bash
python -m novel_craft menu
```

---

## الأوضاع

| وضع | ماذا يفعل |
|-----|-----------|
| **interview** | دردشة أسئلة لفهم تصوّرك → `vision/` |
| **write** | خطة بناء (عالم، شخصيات، حبكة…) ثم حلقات مشاهد وصقل |
| **analyze** | تفكيك رواية موجودة طبقيًا |
| **critique** | نقد مسودة وفق معيار الجودة الثماني |
| **free** | اختيار مهارة/مسار يدويًا |
| **status / journal** | المشاريع والسجل الموثّق |

---

## أوامر أساسية

```bash
python -m novel_craft new "عنوان الرواية" --mode write --lenses arabic,russian
python -m novel_craft interview <project-id>
python -m novel_craft write <project-id>
python -m novel_craft write <project-id> --phase draft
python -m novel_craft analyze <project-id> --source path/to/text.txt
python -m novel_craft critique <project-id> --draft path/to/draft.txt
python -m novel_craft plan <project-id>
python -m novel_craft brief <project-id> skill-scene-engine
python -m novel_craft skills
python -m novel_craft journal <project-id> --report
python -m novel_craft list
python -m novel_craft menu
```

---

## كيف يعمل العقل المُدير؟

1. يقرأ حالة المشروع (vision، شخصيات، مسودات…).
2. يختار **pipeline** من `novel_craft/data/skills_registry.yaml`.
3. يبني `plans/latest.yaml` ويرتّب المهارات.
4. يصدّر **موجزات** في `plans/briefs/*.md` لتمريرها لوكيل AI.
5. يسجّل كل حدث في `journal/events.jsonl` ويمكن تصدير `journal/REPORT.md`.

التفاصيل: [docs/ORCHESTRATOR.md](docs/ORCHESTRATOR.md)

---

## المهارات

كلها تحت `skills/*/SKILL.md` — انظر [docs/SKILLS.md](docs/SKILLS.md) والكتالوج:

```bash
python -m novel_craft skills
```

**النواة:** `novel-craft-core` · `skill-orchestrator`  
**الكتابة:** عالم، سيناريو، حبكة، شخصيات، أقواس، علاقات، بيئة، مشهد، حوار، سبتيكست، صوت، شعرية  
**القراءة النقدية:** `skill-analyze-novel` · `skill-revision-critique`  
**العدسات:** عربي · روسي–بوليفوني · أنجلوفوني · كلاسيكي  

---

## هيكل المستودع

```
00-foundation/     القاعدة النظرية (v0.1)
skills/            مهارات الوكيل (SKILL.md)
novel_craft/       بايثون: CLI، مُدير، أوضاع، تخزين
docs/              توثيق المجتمع
projects/          مشاريع المستخدمين (محلية)
templates/         قوالب
```

---

## للمجتمع الأدبي

- النظرية ليست وصفة هوليوود؛ البنى **اختيارية** والعدسات **متكافئة**.
- النقد طبقي بشواهد لا ذوق عابر.
- وثّق عملك داخل `projects/<id>/` ليصبح قابلاً للمراجعة والتعليم.

راجع: [docs/FOR_COMMUNITY.md](docs/FOR_COMMUNITY.md) · [CONTRIBUTING.md](CONTRIBUTING.md)

---

## التوثيق

| ملف | المحتوى |
|-----|---------|
| [docs/USER_GUIDE.md](docs/USER_GUIDE.md) | دليل المستخدم |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | المعمارية |
| [docs/ORCHESTRATOR.md](docs/ORCHESTRATOR.md) | العقل المُدير |
| [docs/SKILLS.md](docs/SKILLS.md) | فهرس المهارات |
| [00-foundation/README.md](00-foundation/README.md) | القاعدة الأدبية |

---

## الحالة

**v0.1.0 Alpha** — الهيكل كامل، المهارات موثّقة، الواجهة تعمل محليًا.  
تنفيذ النثر الأدبي العميق يتم عبر **وكيل AI** يقرأ الموجزات والـ `SKILL.md`؛ بايثون يرتّب ولا يستبدل الكاتب.
