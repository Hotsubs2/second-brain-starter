---
type: weekly
week: {{date:GGGG-[W]WW}}
---

# Week {{date:GGGG-[W]WW}}

*Five questions, the same every week. A year of answers becomes a measurement.*

## 1. What actually happened this week?

-

## 2. What did I avoid, and what did it cost?

-

## 3. What worked, that I would do again?

-

## 4. The one thing that changes next week

*One. A list is a way of committing to nothing.*

-

## 5. What moved the first-priority project?

*Something concrete. If nothing, say so.*

-

## Still open from the last two weeks

```dataview
TASK
FROM "Daily"
WHERE !completed AND text != "" AND file.day >= date(today) - dur(14 days)
```
