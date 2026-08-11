# Skill 배치 rubric

후보가 재사용 가능한하고 저장소-구체적인인 경우에만 이 rubric을
적용합니다. 한 번에 독립적으로 적용 가능한 스킬 instruction 또는 워크플로
하나씩 판단합니다.

## 정규화된 근거

후보 text, verified 스킬 소스 경로, 호스트, 소유권 근거, 정확한
proposed native 스킬 대상을 기록합니다. 저장소/user rule 경로는
조사하거나 분류하지 않습니다.

Unicode를 normalize하고 English는 case-insensitively 비교합니다. 정확한
호스트-native 경로와 소유권이 검증된 경우에만 스킬 대상을 유효한 것으로
봅니다.

## 순서 있는 결정 table

처음 일치하는 항목에서 멈춥니다.

1. 검증된 tracked 저장소 스킬은 저장소-native 대상을 유지합니다.
2. 검증된 호스트-owned user 스킬은 user-native 대상을 유지합니다.
3. 경로/소유권 근거가 없거나 충돌하면 `Unverifiable`입니다.

이미 존재하거나 현재-호스트 discovery가 허용한 현재-호스트 native 스킬
경로만 사용합니다. 근거로 현재 호스트를 식별하고, 식별할 수 없으면
대상을 지어내지 말고 caller-구체적인 `Partial/Blocked` 또는
`Unverifiable` 경로로 넘깁니다. 한 호스트의 경로 convention을 다른 호스트에
복사하거나, 여러 호스트로 fan out하거나, 대상을 synchronize하거나, TigerKit
global 상태를 만들지 않습니다.
