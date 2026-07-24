# دليل المستخدم

## 1) تثبيت

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
python -m novel_craft doctor
```

## 2) اكتب رواية (المسار الموصى به)

### أ. أنشئ مشروعًا

```bash
python -m novel_craft new "مدن الظل" --mode write --lenses arabic
```

### ب. أجرِ المقابلة

```bash
python -m novel_craft interview mudn-alzl
```

أجب عن الأسئلة (أو `تخطَّ`). سيُحفظ:

- `projects/.../vision/vision.yaml`
- `vision/VISION.md`
- خطة bootstrap + موجزات

### ج. جهّز الكتابة

```bash
python -m novel_craft write mudn-alzl
```

### د. نفّذ مع وكيل AI

افتح بالترتيب ملفات:

`projects/<id>/plans/briefs/*.md`

واطلب من الوكيل اتباع التعليمات وحفظ المخرجات في مجلدات المشروع (`characters/`, `plot/`, `scenes/`…).

### هـ. حلقة المسودات ثم الصقل

```bash
python -m novel_craft write mudn-alzl --phase draft
python -m novel_craft write mudn-alzl --phase polish
python -m novel_craft critique mudn-alzl --draft projects/.../drafts/ch01.md
```

## 3) حلّل رواية

```bash
python -m novel_craft new "تحليل موسم الهجرة" --mode analyze
python -m novel_craft analyze <id> --source path/to/novel.txt
```

الصق النص إن لزم في `analysis/source.txt` ثم مرّر الموجزات للوكيل مع `skill-analyze-novel`.

## 4) انقد مسودة

```bash
python -m novel_craft critique <id> --draft my_draft.txt
```

راجع `critique/RUBRIC.md` و`critique/REPORT.md` بعد عمل الوكيل.

## 5) الواجهة التفاعلية

```bash
python -m novel_craft menu
```

اختَر من القائمة: إنشاء، مقابلة، كتابة، تحليل، نقد، مهارات، سجل…

## 6) أين تُحفظ أعمالي؟

تحت `projects/<project-id>/` — هذا «مجلد العمل» الكامل القابل للأرشفة والمشاركة (احترم حقوق نصوصك ونصوص غيرك).

## 7) العمل مع Grok / وكلاء آخرين

1. `plan` أو `write` لتوليد briefs  
2. انسخ محتوى brief + الملفات المشار إليها  
3. بعد التنفيذ: حدّث YAML/MD في المشروع  
4. `journal` يدوياً عبر إعادة `plan` أو سجّل ملاحظات في `journal/`

(يمكن لاحقًا ربط API؛ v0.1 يفصل الترتيب عن التوليد.)
