---
name: tk-comic
description: "[user/auto] 기술 개념·검증된 코드 변경을 원본 근거에 맞춘 교육용 만화로 제작해 달라는 명시적 요청에 사용합니다. 일반 설명, 삽화 한 장, HTML, 영상 제작에는 사용하지 않습니다."
disable-model-invocation: false
argument-hint: "[topic, source, or prepared directory] [--preset name] [--art name --tone name --layout name] [--pages N] [--prompts-only | --images-only | --regenerate N[,M...]]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
---

<a id="technical-comic"></a>
# 교육용 기술 만화 제작

## 범위와 소유권

사용자가 만화 제작을 요청하거나 명확히 위임했을 때만 실행합니다. 이 스킬은 근거에 맞춘 스토리보드, 등장인물 연속성, 말풍선, 페이지별 생성·복구를 독립적으로 소유합니다. `tk-explain`이나 `tk-illustrate`의 설치·선행 호출을 요구하지 않습니다. 일반 설명·삽화·HTML·영상으로 범위를 넓히지 않으며, 새로운 이미지 엔진, 제공자 선택기, 서버와 공통 오케스트레이터를 만들지 않습니다.

조건부로 필요한 공통 기준은 현재 설치된 소유 스킬에서 읽습니다. 대상·선택·승인을 묻기 직전에 [질문 라운드](../tk-questioning/references/questions.md)를, 파일을 쓰기 전에 [산출물 경로](../tk-artifacts/references/artifact-paths.md)를, 결과를 전달하기 전에 [채팅 전달](../tk-writing/references/delivery.md)을 읽습니다. 의존 스킬이 설치되지 않았거나 계약이 일치하지 않으면 해당 단계는 `Blocked`로 보고하고 `tk-setup-skills`를 안내합니다. 참조 읽기는 추가적인 실행·발행 승인이 아닙니다.

## 입력과 제작 결정

인자가 없거나 제작 조합이 미정이면 [제작 결정](references/workflow.md)을 읽습니다. 네이티브 질문 도구로 **주제부터 확정한 다음**, 그 주제에 맞는 제작 조합 세 개를 추천합니다. 주제·스타일·페이지 수 등 이미 지정한 축과 유효한 위임은 재질문하지 않습니다. 범위가 확정되면 콘티부터 전달까지 진행하며, 사용자가 요청하지 않은 중간 스타일·콘티 승인을 추가하지 않습니다.

옵션을 해석하거나 조합을 추천할 때 [옵션과 조합](references/options.md)을 읽습니다. 선택된 `art`·`tone`·`layout`·`preset`의 참조만 추가로 읽습니다. 일부 실행·재개 요청에만 [부분 제작](references/partial-workflows.md)을 읽습니다.

```text
/tk-comic architecture.md --preset ohmsha --layout webtoon --pages 4 --lang ko
/tk-comic concept.md --art manga --tone warm --layout four-panel --storyboard-only
/tk-comic ./prepared-comic --regenerate 3
```

## 제작 흐름

1. **근거 고정:** 출처·revision/시점·독자·교육 목표와 정확한 용어를 확인합니다. 코드 변경에는 확인한 commit/diff와 실행 조건을 연결합니다. 확인되지 않은 동작, 추론과 비유를 사실로 묘사하지 않습니다. 외부에 전달할 최소 내용과 참조 이미지의 사용 권한을 확인하고 비밀·무관한 사용자 파일은 제외합니다.
2. **콘티 작성:** [만화 구성 및 검사](references/comic-production.md)를 읽고 페이지·패널 ID, 장면·대사·출처·연속성을 명세합니다. 선택된 프리셋의 서사 규칙과 개별 옵션을 반영하되 기존 상업용 캐릭터를 기본값으로 복제하지 않습니다. `--storyboard-only`는 이 단계의 품질 확인 후 전달합니다.
3. **프롬프트 보존:** [패키지와 결과 계약](references/handoff.md)에 따라 각 페이지와 필요한 캐릭터 시트의 **완전한 독립 프롬프트**를 `prompts/`에 저장하고 확인합니다. 이미지 도구가 없어도 이 단계까지 완료합니다. `--prompts-only`는 검증된 준비물을 전달하고 종료합니다.
4. **기능 확인·생성:** 현재 호스트가 노출한 네이티브 래스터 도구를 우선합니다. 비율, 참조 전달, 결과 파일/이미지 접근, 동시 호출 지원을 실제 도구 계약으로 확인합니다. 필요한 캐릭터 시트를 먼저 검증한 후 종속 페이지를 생성합니다. 지정된 참조를 텍스트 설명으로 조용히 대체하지 않습니다. 필요한 기능이 없으면 생성 단계만 차단하고 외부 생성용 패키지를 완성합니다.
5. **검사·복구:** 읽기 크기와 확대 상태에서 실제 픽셀·대사·작은 라벨·기술 관계·페이지 연속성을 대조합니다. 근거 있는 오류는 프롬프트를 먼저 수정하고 해당 페이지의 새 후보를 생성합니다. 검증된 기존 후보와 비선택 페이지를 보존합니다. 컷 전체 교체는 만화 구성 참조의 제한을 모두 충족해야 하며 현재 호스트의 이미지 편집 도구 규칙도 따릅니다.
6. **전달:** 요청된 페이지·준비물을 순서대로 전달하고 패키지의 `README.md`에 적용 옵션, 실제 도구, 프롬프트·이미지 연결, 확인 결과와 남은 한계를 기록합니다. `change` 및 명시적인 검토 요청에는 최종 콘텐츠·근거·실제 이미지에 대한 독립 리뷰를 적용합니다. 필요한 리뷰나 픽셀 검사를 수행할 수 없으면 `Pass`로 보고하지 않습니다.

## 실패·승인 경계

래스터 제작을 요청받았지만 도구나 필수 참조 기능이 없으면 **텍스트 콘티와 최종 프롬프트가 있는 외부 인계 패키지를 자동으로 완성**합니다. 실제 래스터가 없으면 `status: Blocked`, 검증된 준비물에는 `preparation: Pass`, `rendering: Blocked`, `deliverable: external-handoff-ready`를 기록합니다. 명시적 준비물 요청과 픽셀을 확인할 수 없는 경우는 [결과 상태](references/handoff.md#결과-상태)로 구분합니다.

래스터 도구 부재로 차단된 경우에는 준비물을 전달한 뒤 질문 기준에 따라 **"SVG로 콘티를 그려 드릴까요? 외부 이미지 모델에 참조로 넣을 수 있습니다"**라고 제안합니다. 수락 전에는 SVG를 만들지 않습니다. 수락하여 만들면 `벡터 콘티`로 표시하고 래스터 페이지 완료로 보고하지 않습니다. SVG/HTML/캔버스나 프롬프트만 만든 것을 생성 만화라고 주장하지 않습니다.

기존 승인을 보존하되 설치, 자격 증명, 새로운 비용, 승인 범위 밖의 외부 전송·원격 발행, 사용자 파일 덮어쓰기는 별도 권한 없이 실행하지 않습니다. `--no-confirm`이나 부분 실행 플래그가 이 경계를 바꾸지 않습니다.

## 산출물

명시적 목적지 또는 호스트가 승인한 지속 산출물 경로를 우선합니다. 별도 경로가 없으면 `.tigerkit/comics/<slug>/`를 사용하고, worktree를 제거하면 함께 사라지는 로컬 경로라는 점을 밝힙니다. `tk-explain` 전용 `artifacts.durableRoot`나 도우미를 빌려 쓰지 않습니다. 기본 목적지가 이미 있으면 고유 접미사를 붙이고, 명시적으로 요청한 기존 패키지는 부분 제작 절차로 재개합니다. 임시 작업·근거는 각각 `.tigerkit/tmp/tk-comic/<run-id>/`, `.tigerkit/evidence/tk-comic/<run-id>/`에 두며 안전한 소유 경로·Git ignore를 먼저 확인합니다. 패키지 자체에는 실행 산출물을 쓰지 않습니다.

## 출처

[출처와 적용 판단](references/sources.md)에 고정 revision과 조정 범위를 기록합니다. [LICENSE.txt](LICENSE.txt)의 고지를 독립 배포에도 유지합니다.
