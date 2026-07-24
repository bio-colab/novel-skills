---
name: skill-relationship-web
description: >
  شبكة العلاقات — تداخل الشخصيات، السلطة، الأسرار، الدين العاطفي.
  Triggers: علاقات، relationship، تداخل شخصيات، /skill-relationship-web
layer: character
inputs: [characters]
outputs: [characters/relationships.yaml, characters/WEB.md]
---

# شبكة العلاقات

## الدور

كل علاقة = نظام قوى يتحرّك بالمشاهد.

## نموذج حافة

```yaml
- a: char_01
  b: char_02
  type: love|power|debt|rivalry|secret|kin|mentor
  tension: 0-10
  secret: 
  what_a_wants_from_b: 
  what_b_wants_from_a: 
  fault_line: # أين ستنكسر
```

## قواعد

- حدّث التوتر بعد كل مشهد كبير.  
- الخصم الجيد يريد شيئًا مفهومًا.  
- أضف مثلثات (A-B-C) حيث يلزم.

## ما لا تفعله

- لا علاقات ثابتة طوال الرواية بلا سبب فني.  
