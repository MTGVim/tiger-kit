# 원천 자료 유형

제품별 가정보다는 범용 원천 자료 범주를 사용합니다.

## 이슈 트래커

공통 필드:

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

## 지식베이스

공통 필드:

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

## PRD 또는 브리프

공통 필드:

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
