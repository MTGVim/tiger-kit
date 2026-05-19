# TigerKit 운영 산출물 구조

이 문서는 `.tigerkit/docs/` 아래 TigerKit 운영 문서 중 산출물 배치와 책임을 설명합니다. 사용 흐름은 `.tigerkit/docs/usage.md`, receipt 규칙은 `.tigerkit/docs/output-contract.md`를 기준으로 봅니다.

TigerKit은 절차 상태 파일에 의존하지 않습니다. 기본 산출물은 branch-local source reference, gap evidence, 회고 기록, 인계 계약입니다.

## 기본 구조

```text
.tigerkit/
  branches/
    feature__example/
      requirements.md
      gap.md
      reflect.md
      handoff.md

docs/SOT_MANIFEST.md          # existing target-repo SOT registry candidate
docs/REQUIREMENTS.md          # example existing target-repo requirement SOT category
docs/DESIGN.md                # example existing target-repo design SOT category
IMPLEMENTATION_POLICY.md # binding project policy SOT candidate, if present
docs/assets/sot/              # preferred stable local SOT asset root
DESIGN.md                     # existing-only, not created by TigerKit
COMPONENT_REUSE_MAP.md        # preferred derived reuse map, existing-only
reuse-map.md                  # legacy alias / migration candidate only
CLAUDE.md                     # repo instruction; managed section은 없으면 강한 반영 추천 후보
```

`.tigerkit/branches/{escaped-branch}/`는 TigerKit working material입니다. `DESIGN.md`와 `COMPONENT_REUSE_MAP.md`는 repo-level derived knowledge입니다. `docs/SOT_MANIFEST.md`, `docs/REQUIREMENTS.md`, `docs/DESIGN.md`, `IMPLEMENTATION_POLICY.md`, `docs/assets/sot/`는 target repo에 이미 있으면 SOT candidate로 intake할 수 있습니다. `reuse-map.md`는 legacy alias 또는 migration candidate로만 읽습니다.

Root-level `.tigerkit/requirements.md`, `.tigerkit/gap.md`, `.tigerkit/reflect.md`는 deprecated artifact입니다. active write target이 아니며, legacy 형상을 만나면 `/tk:reflect`에서 migration guidance를 surfaced 할 수 있습니다.

`{escaped-branch}`는 현재 git branch의 collision-safe path encoding입니다. ASCII letter, digit, `.`, `_`, `-`는 그대로 두고 다른 byte는 `~HH` uppercase hex로 encode합니다. 예: `feature/foo` → `feature~2Ffoo`, `feature__foo` → `feature__foo`.

TigerKit branch-local artifact는 detached HEAD나 protected branch(`main`, `master`, `develop`)에서 쓰지 않습니다. write command 실행 전 feature branch로 전환합니다.

## 파일 책임

| 파일 | 역할 |
| --- | --- |
| `.tigerkit/branches/{escaped-branch}/requirements.md` | branch-local source reference index와 access manifest |
| `.tigerkit/branches/{escaped-branch}/gap.md` | indexed SOT와 clean HEAD baseline 비교 기록 |
| `.tigerkit/branches/{escaped-branch}/reflect.md` | session reflection과 durable artifact 반영 후보 정리 |
| `.tigerkit/branches/{escaped-branch}/handoff.md` | 다음 세션용 continuation contract |
| `/tk:review` output | 파일 산출물이 아닌 chat review output |
| `CLAUDE.md` | 세부 정책과 운영 규칙의 기준 문서 |
| `DESIGN.md` | existing-only derived design knowledge |
| `COMPONENT_REUSE_MAP.md` | existing-only derived reuse map |
| `reuse-map.md` | legacy alias / migration candidate only |
| `docs/SOT_MANIFEST.md` | target repo에 이미 있으면 SOT registry candidate |
| `IMPLEMENTATION_POLICY.md` | target repo에 이미 있으면 project policy candidate |
| `docs/assets/sot/` | binding visual/document SOT의 stable local asset root candidate |

## 운영 메모

- `requirements.md`는 source of truth 본문이 아니라 source reference index입니다.
- `gap.md`는 비교 기록입니다. 구현 작업 목록을 대신하지 않습니다.
- `reflect.md`는 기록과 반영 후보를 남기고, 실제 적용 여부는 별도로 확인합니다.
- `handoff.md`는 다음 세션용 인계 문서입니다.
- `CLAUDE.md`와 repo-level derived artifact에 대한 세부 정책은 `CLAUDE.md`를 기준으로 봅니다.
