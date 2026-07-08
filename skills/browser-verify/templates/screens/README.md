# screens/README.md

screen catalog를 작성할 때 쓰는 템플릿입니다.

## 작성 규칙

- 화면 하나당 `screens/<screen-name>.md` 파일 하나를 만듭니다.
- 파일 이름은 진입 대상이 바로 보이게 짧고 명확하게 적습니다.
- 각 screen 문서는 진입 경로, selector, 필요한 데이터, 함정을 같이 적습니다.

## screen 문서 기본 골격

```md
# <screen-name>

## Goal
- 무엇을 비교하는 화면인지

## Entry
- 시작 URL 또는 진입 경로
- 필요한 navigation click / tab / modal open 절차

## Data / Context
- 필요한 계정, fixture, feature flag

## Selectors
- 핵심 container:
- 비교 대상 element:
- ready signal:

## Known pitfalls
- sticky header / lazy load / animation / overlay

## Regression notes
- 이전에 깨졌던 포인트
```
