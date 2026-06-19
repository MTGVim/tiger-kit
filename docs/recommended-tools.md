# Recommended Tools

Recommended tools는 optional이다. TigerKit core 기능에 필요하지 않다.

## Policy

- 기본 설치하지 않는다.
- 설치하지 않아도 TigerKit core 기능에 영향이 없어야 한다.
- README 확인, 설치, 설정은 사용자가 `/tk:config`의 기타 추천 도구 메뉴에서 고른 경우에만 진행한다.
- 설치 전 변경 범위와 설치 방식을 설명하고 승인받는다.
- 외부 도구를 TigerKit core에 직접 내장하지 않는다.
- TigerKit은 추천 외부 도구를 자동 설치하지 않는다.
- upstream GitHub 문서에 설치 방법이 있으면 그 문서를 우선 안내한다.
- 설치 방법이 불명확하면 repo/README 링크만 주고 upstream 확인을 요청한다.
- 설치 안내 후에는 verify installation 단계를 분리해 요구한다.

## Catalog

```yaml
recommended_tools:
  context-mode:
    display_name: Context Mode
    repo: mksglu/context-mode
    readme: README.md
    install_doc: https://github.com/mksglu/context-mode/blob/main/README.md
    verify: verify installation before continuing TigerKit recommended-tools setup
    purpose: AI coding agent의 context window 사용량을 줄이고, 큰 tool output을 sandbox/index 기반으로 다루는 보조 도구
    integration_level: recommendation-only

  rtk:
    display_name: RTK
    repo: rtk-ai/rtk
    readme: README.md
    install_doc: https://github.com/rtk-ai/rtk/blob/master/README.md
    verify: verify installation before continuing TigerKit recommended-tools setup
    purpose: 터미널 명령 출력 압축/필터링을 통한 컨텍스트 절약 보조 도구
    integration_level: recommendation-only

  superpowers:
    display_name: Superpowers
    repo: obra/superpowers
    readme: README.md
    marketplace_repo: obra/superpowers-marketplace
    install_doc: https://github.com/obra/superpowers/blob/main/README.md
    marketplace_doc: https://github.com/obra/superpowers-marketplace/blob/main/README.md
    verify: verify installation before continuing TigerKit recommended-tools setup
    purpose: Claude Code용 추가 skills/workflows 컬렉션
    integration_level: recommendation-only
```

## UI placement

`/tk:config` 마지막에 “기타 추천 도구” 메뉴를 둔다. 기본 설정 단계에서는 바로 노출하지 않는다.

## Response policy

사용자가 특정 추천 도구를 고르면 TigerKit은 아래 순서로 안내한다.

1. 설치가 core requirement가 아님을 먼저 알린다.
2. GitHub 설치 문서가 확인되면 그 링크를 제공한다.
3. 설치가 끝나면 verify installation을 요청한다.
4. 설치 확인 전에는 TigerKit config state를 해당 도구 기준으로 확정하지 않는다.
