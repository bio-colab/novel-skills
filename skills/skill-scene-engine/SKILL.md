---
name: skill-scene-engine
description: >
  محرّك المشهد — هدف، عائق، استراتيجية، تحوّل قيمة، سبتيكست.
  Triggers: مشهد، scene، اكتب مشهد، /skill-scene-engine
layer: scene
inputs: [characters, plot, location]
outputs: [scenes/scene_*.yaml, scenes/*.md]
---

# محرّك المشهد

## الدور

تكتب/تصمم وحدات ذرية: **لا مشهد بلا تحوّل** (McKee).

## قالب

```yaml
id: sc_001
pov_character: 
location: 
sensory_pressure: 
entering_value_state: 
goal: 
obstacle: 
strategy: 
turn: 
exiting_value_state: 
subtext: 
plot_consequence: 
character_consequence: 
motif_image: 
```

ثم مسودة نثر في `scenes/sc_001.md` إن طُلب.

## قواعد

1. ادخل متأخرًا؛ اخرج مبكرًا.  
2. الصراع: داخلي / علائقي / بيئي — واحد على الأقل.  
3. الحوار فعل (انظر skill-dialogue).  
4. إن لم يتغيّر شيء → ادمج أو احذف أو زِد العائق.

## ما لا تفعله

- مشاهد معلومات محضة.  
- مونولوج ثيم صريح.  
