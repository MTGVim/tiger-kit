# 작업자 전달 계약

이 스킬의 `direct | delegated` 실행 전략과 위임 작업자 `receipt`에 적용하는
정본입니다. `delegated`를 선택하면 새 `general-purpose` 작업자와 검토자를
사용하고, 작업자를 만들 수 없을 때 `direct`로 대체하지 않고 `Blocked`입니다.

## 세션 모델 라우팅

배정 전에 저장소 루트의 선택적 `.tigerkit/session.md`에서 현재 호스트 `section`을
읽습니다. `cheapest`, `standard`, `strongest` 세 `class` `block`이 모두 있고 각
`block`에 `model`이 있으며 `Status: Ready`일 때만 선택한 `model`/`effort`를
배정 전에 전달합니다.

```markdown
# TigerKit session
Status: Ready

## claude-code

### cheapest
- model: haiku
- effort: low

### standard
- model: sonnet
- effort: medium

### strongest
- model: opus
- effort: high
```

파일 또는 현재 `host section`이 없고 세 `class`의 제어값이 모두 확인되면 정확한 중첩
`block`을 `.tigerkit/session.md`에 원자적으로 초안 생성하고 `Status: Pending`으로
둡니다. 기존 불완전·충돌 `block`은 덮어쓰지 않고 보존하며, 필요한 보정안을 같은
승인 표면에 제시합니다. 둘 다 `routing_state=review-required`로 기록하고 사용자가
초안을 검토·승인하기 전에는 배정하거나 제품/Git/`remote`를 변경하지 않습니다.
승인 뒤에만 `Status: Ready`로 바꾸고 세 `class`/`model`을 `reread`합니다. 확인되지 않은
`selector`를 발명하거나 `unavailable`을 `model` 값으로 쓰지 않고 `Pending`으로
남깁니다. 허용 `key`는 `model`, `effort`뿐입니다.

## Receipt

호스트 배정 표면의 `worker ID/handle`이 정본 `identity`입니다. 하위 작업자의 자체
ID는 선택 사항이며 `unavailable`이어도 됩니다. 완료 `report`에는 다음 `receipt`와
`Plan deviations`를 포함합니다. 빈 `deviation`은 `none`이 아닙니다.

```text
Frozen receipt: strategy=<delegated> model_class=<class> requested_selector=<selector> owned_paths=<exact list>
Host dispatch receipt: worker_id=<host id or handle> receipt_source=<host dispatch surface>
Actual receipt: strategy=<actual> model_class=<actual> requested_selector=<actual> changed_paths=<exact list>
Plan deviations: none | transient-self-corrected:<field; frozen; transient; restored; reason> | scope-violating:<field; frozen; published; reason>
```

`Actual receipt`는 고정된 `strategy`, `class`, `selector`, 경로와 필드별로 일치해야
합니다. `transient-self-corrected`는 새 `ancestry`·게시 `tree/diff`·범위·검사를
제어기가 독립적으로 재검증해 `net effect 0`을 입증한 경우에만 기록합니다. 그 밖의
불일치, 빈 `deviation`, `scope-violating`은 `Pass`가 아닙니다.
