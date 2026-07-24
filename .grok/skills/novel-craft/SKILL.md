---
name: novel-craft
description: >
  نظام حرفة الرواية الكامل: كتابة، مقابلة كاتب، تحليل، نقد، عقل مُدير.
  Use when the user runs /novel-craft or asks to write/analyze/critique a novel
  with the Novel Craft toolkit in this repo.
---

# Novel Craft — نقطة دخول الوكيل

## أولًا

1. اقرأ `README.md` و`docs/USER_GUIDE.md` إن لزم.  
2. شغّل عبر الطرفية عند الحاجة:
   - `python -m novel_craft doctor`
   - `python -m novel_craft menu` أو أوامر الوضع المناسب  
3. اعمل **داخل** `projects/<id>/` واحفظ كل المخرجات هناك.  
4. اتبع العقل المُدير: `plans/latest.yaml` و`plans/briefs/`.  
5. نفّذ المهارة النشطة بقراءة `skills/<id>/SKILL.md` حرفيًا.  
6. سجّل النتائج؛ اطلب من المستخدم تشغيل `python -m novel_craft journal <id> --report` عند الحاجة.

## الأوضاع

- **مقابلة:** `skill-interview-author` + حفظ vision  
- **كتابة:** bootstrap → draft loop → polish  
- **تحليل:** `skill-analyze-novel` + طبقات  
- **نقد:** `skill-revision-critique` + RUBRIC  

## قواعد

- لا تفرض قالبًا واحدًا.  
- وثّق كل شيء في ملفات المشروع.  
- النظرية في `00-foundation/`؛ التنفيذ في المهارات.
