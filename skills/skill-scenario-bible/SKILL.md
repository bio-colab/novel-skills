---
name: skill-scenario-bible
description: >
  إنجيل المادة — الفابيولا، الخط الزمني، حقائق العالم المتماسكة.
  Triggers: سيناريو، bible، فابيولا، timeline، /skill-scenario-bible
layer: material
inputs: [vision, world]
outputs: [world/timeline.yaml, plot/fabula.md]
---

# إنجيل المادة (Scenario Bible)

## الدور

تحفظ **ما حدث/سيحدث** في العالم بترتيب زمني خام، منفصلًا عن ترتيب الحكي.

## المخرجات

- `plot/fabula.md`: أحداث مرقّمة زمنيًا  
- `world/timeline.yaml`: نقاط زمنية + فاعلون  
- `world/facts.yaml`: حقائق لا يجوز كسرها دون قرار واعٍ  

## قواعد

- ميّز بوضوح: معلوم للشخصيات / معلوم للقارئ فقط / سر بعد.  
- سجّل التناقضات كـ OPEN QUESTIONS لا تسكت عنها.

## ما لا تفعله

- لا تخلط الفابيولا بترتيب السرد الفني (ذلك للحبكة).  
