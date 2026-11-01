<a id="source-dispositions"></a>
# 출처별 처리 판단

<a id="pinned-evidence"></a>
## 고정된 근거

주 출처는 [phuryn/pm-skills](https://github.com/phuryn/pm-skills/tree/8607e3b077817f89bf4a9b623246219734ac3be0)입니다.
다음 위치에서 구현과 포함된 논거를 읽었습니다.

- `pm-execution/skills/outcome-roadmap/SKILL.md`
- `pm-product-discovery/skills/opportunity-solution-tree/SKILL.md`
- `pm-product-discovery/skills/prioritize-features/SKILL.md`

보충 출처는 [mattpocock/skills wayfinder](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/wayfinder/SKILL.md)입니다.
이 정확한 절차에 대한 upstream 동작 평가는 검증되지 않았습니다. 저장소 구조 테스트는 인터뷰 품질을 입증하지 않습니다. TigerKit은 자체 동작 사례를 제공합니다.

| 처리 판단 | 요소 | TigerKit 결정 |
| --- | --- | --- |
| keep | 기능 목록보다 결과를 중심에 둡니다. | 각 마일스톤에는 수혜자와 관련된 결과와 완료 근거가 필요합니다. |
| adapt | 결과·기회·해결책·실험을 분리합니다. | 필수 트리 깊이나 개수 없이 관련 대안과 한정된 조사를 사용합니다. |
| adapt | 영향, 노력, 위험과 전략적 정합성을 고려합니다. | 권한, 역량, 의존성과 운영 부담을 포함합니다. 수치 근거가 없으면 정성적으로 판단합니다. |
| adapt | Wayfinder의 미지정 범위와 제외 범위를 구분합니다. | 조건부 후속 단계를 제외된 작업과 별도로 보존합니다. |
| omit | 분기별 기간, 고정 해결책 개수·상위 5개 개수를 생략합니다. | 기한 없음과 부족한 근거도 유효합니다. 정밀성을 꾸며 내지 않습니다. |
| omit | tracker map, 배정, 조사 전달과 런타임을 생략합니다. | 로드맵 작성은 작업 실행이나 이슈 발행이 아닙니다. |

<a id="existing-owners-and-distinct-gap"></a>
## 기존 담당자와 고유한 공백

`tk-grill`은 산출물 없이 결정을 철저히 검증하고 공통 이해를 확인합니다. `tk-research`는 외부 접근법을 비교합니다. `tk-prep`은 승인된 저장소 구현을 준비하고 수행합니다. 이 스킬은 저장소 없는 비기술 작업을 포함하여 사용자가 선택하는 선택적 계획 인터뷰와 로드맵을 담당합니다. 필수 선행 단계나 shared-state runner가 아닙니다.

단일 주제 인터뷰, 빈 호출, 유효한 미확인 답변과 별도 운영은 사용자가 명시적으로 요청한 조정 사항입니다. 출처 예시는 보편적인 도메인 규칙이 아닙니다. 라이선스는 [upstream 라이선스](../UPSTREAM-LICENSES.txt)로 배포합니다.
