---
name: tk-eli5
description: "[user/auto] 어떤 주제든 초보자가 이해하도록 큰 그림과 적은 글의 self-contained HTML picture explainer로 만든다. 명시적 /tk-eli5 또는 그림 중심 HTML 설명 요청에 사용하며, 직전 답변의 text 재설명·비교 prototype·기존 페이지 편집에는 사용하지 않는다."
disable-model-invocation: false
argument-hint: "<topic and optional output path>"
metadata:
  tigerkit:
    kind: hybrid
    origin: anthropics/claude-plugins-community
    relationship: adapted
    upstream-skill: eli5
---

# Visual ELI5 Explainer

설명할 주제를 처음 접하는 사람이 핵심 흐름을 한눈에 이해하도록 그림 중심의
단일 HTML 자료를 만듭니다. 명시적 `$tk-eli5` 호출이나 큰 그림과 적은 글의
HTML 설명 자료 요청에 사용합니다.

## 경계

- 바로 앞 설명을 text로만 쉽게 다시 말하는 요청은 `tk-mwhat`의 범위이므로
  `NotApplicable`로 중지합니다.
- 둘 이상의 UI/logic 대안을 비교하는 실행물은 `tk-prototype`의 범위이므로
  `NotApplicable`로 중지합니다.
- 일반 prose 설명, code walkthrough, 기존 HTML/page 편집에는 적용하지 않고
  `NotApplicable`로 중지합니다.
- 주제가 없거나 무엇을 설명해야 하는지 모호하면 정확히 `Unverifiable`만 출력하고
  파일을 만들지 않습니다.

## Workflow

1. 하나의 명확한 주제와 사용자가 지정한 출력 경로를 확인합니다. 경로가 없으면
   현재 작업 디렉터리의 `eli5-<topic-slug>.html`을 사용하고, 이미 있으면 숫자
   suffix로 새 경로를 선택합니다. 기존 파일은 명시적 승인 없이 덮어쓰지 않습니다.
2. 핵심 mental model을 3~5개 장면과 하나의 일관된 비유로 나눕니다. 최신성이나
   전문 사실이 중요한 주제는 사용 가능한 근거로 먼저 확인하며, 정확성·필수 경고를
   단순화를 이유로 버리지 않습니다.
3. 하나의 self-contained HTML을 만듭니다. CSS와 SVG/CSS 그림은 inline으로 넣고
   외부 asset, font, framework, dependency, build step, network request를 추가하지
   않습니다.
4. 큰 시각 요소, 짧은 제목, 장면별 35단어 이하의 설명을 사용합니다. semantic HTML,
   충분한 contrast, SVG의 accessible title, color-only가 아닌 구분,
   `prefers-reduced-motion`을 기본으로 지킵니다.
5. HTML이 offline에서 바로 열리고 3~5개 장면, inline visual, AI 작성 footer를
   포함하는지 확인합니다. server를 시작하거나 browser를 자동으로 열지 않습니다.

HTML 마지막에는 다음 문장을 그대로 넣습니다.

```text
🤖 본 설명 자료는 AI가 작성했습니다.
```

## 완료와 출력

성공은 지정한 HTML 하나가 존재하고 별도 설치나 network 없이 열리며, 큰 그림과
적은 글로 주제의 핵심 흐름을 설명할 때만 `Pass`입니다. 생성 실패를 성공으로
보고하지 않습니다.

사용자에게는 다음 한 줄만 반환합니다.

```text
<path> — 초보자용 그림 중심 HTML 설명 자료.
```

## Source

`anthropics/claude-plugins-community`의 `eli5` v1.0.0, commit
`863e70dc7cff21a2facc749e40a7ecd1a5d19833`에서 큰 그림·적은 글의 HTML artifact와
`/eli5 <topic>` 동작을 적용했습니다. TigerKit은 offline self-contained output,
skill 경계, 검증, 충돌 없는 path, 접근성 및 작성자 표시를 추가했습니다.
원본 저작권과 MIT 고지는 repository `NOTICE.md`에 있습니다.
