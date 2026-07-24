---
name: skill-character-patterns
description: >
  أنماط الشخصيات — بطاقات Want/Need/Ghost، أدوار، أصوات، استدارة.
  Triggers: شخصيات، character، بطاقة، /skill-character-patterns
layer: character
inputs: [vision]
outputs: [characters/char_*.yaml, characters/CAST.md]
---

# أنماط الشخصيات

## الدور

تبني ذوات قابلة للمفاجأة المقنعة (Forster) وذات خطاب مستقل (Bakhtin).

## بطاقة إلزامية

```yaml
id: char_01
name: 
role_in_plot: protagonist|antagonist|catalyst|foil|witness
surface_want: 
deep_need: 
ghost_wound: 
core_fear: 
core_value: 
contradiction: 
voice_traits: 
arc: change|fall|flat-impact|revelation|tragic-stasis
relationship_edges: []
environment_bond: 
```

## اختبارات

- **الاستدارة:** هل تفاجئ بإقناع؟  
- **التناقض:** هل يوجد كذب على الذات؟  
- **الصوت:** هل المعجم مختلف عن الآخرين؟  

## مخرجات

- ملف لكل شخصية + `CAST.md` جدول مقارن.

## ما لا تفعله

- لا قوائم سمات بلا رغبة.  
- لا تجعل الجميع يتكلمون بلغة المؤلف.  
