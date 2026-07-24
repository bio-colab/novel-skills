# خريطة مهارات AI — كتابة الرواية

الحالة: **مُنفَّذ في v0.1** — انظر `skills/` و`novel_craft/`

## الحزمة 0 — النواة

| المهارة | الوظيفة | تعتمد على |
|---------|---------|-----------|
| `novel-craft-core` | الأونتولوجيا، معايير الجودة، المفردات المشتركة، عقود المدخل/المخرج | القاعدة v0.1 |

## الحزمة 1 — MVP (أقل مجموعة مفيدة)

| المهارة | المخرج الرئيسي |
|---------|----------------|
| `skill-character-patterns` | بطاقات شخصيات + تناقضات + أصوات |
| `skill-plot-architecture` | عمود فقري حبكي + نقاط تحوّل + سؤال درامي |
| `skill-scene-engine` | مشاهد بتحوّل + صراع + سبتيكست أولي |

## الحزمة 2 — العمق

| المهارة | المخرج الرئيسي |
|---------|----------------|
| `skill-relationship-web` | شبكة علاقات متغيّرة |
| `skill-character-arcs` | أقواس قرارات تحت ضغط |
| `skill-environment-interaction` | المكان كفاعل |
| `skill-subtext-irony` | باطن، مفارقة، ثيم-سؤال |
| `skill-voice-narration` | راوٍ، تبئير، أسلوب حر غير مباشر |
| `skill-poetics-semiotics` | موتيفات، إيقاع، حقول دلالية |
| `skill-dialogue` | حوار كفعل |

## الحزمة 3 — العالم والمادة

| المهارة | المخرج الرئيسي |
|---------|----------------|
| `skill-worldbuilding` | أنظمة العالم |
| `skill-scenario-bible` | إنجيل المادة / الخط الزمني / الحقائق |

## الحزمة 4 — العدسات التراثية

| المهارة | متى تُفعَّل |
|---------|-------------|
| `lens-arabic-heritage` | سرد إطاري، مدينة، تاريخ، عجائبي تراثي |
| `lens-russian-polyphonic` | تعدد أصوات، حوارية |
| `lens-anglophone-craft` | حرفة Forster/Wood/McKee |
| `lens-classical-poetics` | ضوابط أرسطو/هوراس |

## الحزمة 5 — المراجعة

| المهارة | الوظيفة |
|---------|---------|
| `skill-revision-critique` | نقد طبقي وفق Definition of Done |

## تدفق نموذجي (pipeline اختياري)

```
worldbuilding → scenario-bible → character-patterns
        → plot-architecture → relationship-web
        → scene-engine (loop) → arcs update
        → subtext + poetics pass → revision-critique
```

يمكن دخول الحلقة من أي عقدة حسب حاجة الكاتب.
