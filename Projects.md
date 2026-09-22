---
type: index
---

# Projects

Every note with `type: project` shows here by itself. One project is `priority: first`, the thing this season is measured on. Everything else is `later`.

## Active

```dataview
TABLE WITHOUT ID
  file.link AS "Project",
  priority AS "Priority",
  repos AS "Repositories"
FROM ""
WHERE type = "project" AND status = "active" AND file.folder != "Templates"
SORT priority ASC, file.name ASC
```

## Parked or done

```dataview
TABLE WITHOUT ID file.link AS "Project", status AS "Status"
FROM ""
WHERE type = "project" AND status != "active" AND file.folder != "Templates"
SORT file.name ASC
```

## Open tasks

```dataview
TASK
FROM ""
WHERE type = "project" AND !completed AND file.folder != "Templates"
GROUP BY file.link
```
