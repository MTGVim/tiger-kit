# Skill 배치 rubric

candidate가 reusable하고 repository-specific인 경우에만 이 rubric을
적용합니다. 한 번에 독립적으로 적용 가능한 skill instruction 또는 workflow
하나씩 판단합니다.

## 정규화된 evidence

candidate text, verified skill source path, host, ownership evidence, 정확한
proposed native skill target을 기록합니다. repository/user rule path는
조사하거나 분류하지 않습니다.

Unicode를 normalize하고 English는 case-insensitively 비교합니다. 정확한
host-native path와 ownership이 검증된 경우에만 skill target을 유효한 것으로
봅니다.

## 순서 있는 decision table

처음 일치하는 항목에서 멈춥니다.

1. 검증된 tracked repository skill은 repository-native target을 유지합니다.
2. 검증된 host-owned user skill은 user-native target을 유지합니다.
3. path/ownership evidence가 없거나 충돌하면 `Unverifiable`입니다.

이미 존재하거나 current-host discovery가 허용한 current-host native skill
path만 사용합니다. evidence로 current host를 식별하고, 식별할 수 없으면
target을 지어내지 말고 caller-specific `Partial/Blocked` 또는
`Unverifiable` 경로로 넘깁니다. 한 host의 path convention을 다른 host에
복사하거나, 여러 host로 fan out하거나, target을 synchronize하거나, TigerKit
global state를 만들지 않습니다.
