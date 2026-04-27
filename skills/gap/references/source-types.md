# Source Types

Use generic source categories rather than product-specific assumptions.

## Issue Tracker

Common fields:

```yaml
source_type: issue_tracker
id: string
title: string
description: string
acceptance_criteria: string[]
comments: string[]
attachments: string[]
linked_sources: string[]
status: string
assignee: string
updated_at: string
```

## Knowledge Base

Common fields:

```yaml
source_type: knowledge_base
id: string
title: string
sections: object[]
decisions: string[]
constraints: string[]
comments: string[]
related_sources: string[]
updated_at: string
```

## PRD or Brief

Common fields:

```yaml
source_type: prd_or_brief
title: string
problem: string
goal: string
requirements: string[]
non_goals: string[]
constraints: string[]
open_questions: string[]
```
