---
name: arch-review
description: 구조 리뷰 트리거입니다.
---

# Arch Review

구조 문제를 바로 갈아엎는 대신, 어떤 경계가 새고 있고 어디서 반복 마찰이 생기는지 evidence-first로 검토하는 skill입니다.

## Goal

- boundary leak를 찾습니다.
- ownership confusion을 줄일 수 있는 방향을 찾습니다.
- coupling hotspot과 repeated pain을 분리해서 봅니다.
- 큰 rewrite보다 작은 단계적 정리 방향을 제안합니다.

## Process

1. 변경이 자주 엮이는 파일/영역을 읽습니다.
2. 경계, 책임, 의존 방향, 반복되는 마찰을 구분합니다.
3. 이미 잘 된 구조와 진짜 hotspot을 분리합니다.
4. 리팩터링을 당장 강행하지 말고 가장 작은 다음 단계부터 제안합니다.
5. 보고할 때는 아래를 구분합니다.
   - strengths
   - hotspots
   - boundary risks
   - evidence
   - smallest safe next step

## Boundaries

- report-only
- 자동 refactor/rename/이동 금지
- 문서 작성만으로 해결됐다고 주장 금지
- 취향성 리뷰보다 반복 마찰과 구조적 위험을 우선

## Good use cases

- 같은 수정이 여러 파일에 반복 전파될 때
- ownership이 흐려서 버그 수정 경로가 자주 흔들릴 때
- 모듈 경계가 애매해 merge conflict나 coupling이 반복될 때
- 대공사 전에 어디부터 자를지 판단하고 싶을 때
