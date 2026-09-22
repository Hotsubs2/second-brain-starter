---
type: daily
date: {{date}}
---

# {{date:dddd, D MMMM YYYY}}

## Today

*Three that would make today count. Written in the morning, ticked at night.*

- [ ]
- [ ]
- [ ]

### Rolled over from yesterday

```dataview
TASK
FROM "Daily"
WHERE !completed AND text != "" AND file.name = dateformat(date(today) - dur(1 day), "yyyy-MM-dd")
```

## Log

*One line, any time. Time first, then whatever it is. Link a project with `[[...]]`. Start a line with `- [ ]` and it is a task. Add `#idea` and the weekly review collects it.*

- {{time}}
