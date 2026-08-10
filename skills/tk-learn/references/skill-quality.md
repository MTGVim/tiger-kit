# 스킬 품질

명확한 name, narrow description, input, core behavior, boundaries,
completion criteria, minimum output shape을 요구합니다. directory는
self-contained하게 유지합니다. 간결한 지침을 우선하고, 반복되는 누락,
비용이 큰 ordering error, mutation safety, 객관적인 completion proof,
specialist procedure, bounded delegation/review에만 세부사항을 추가합니다.

## 승격 게이트

- 독립적인 반복 2건 또는 artifact가 뒷받침하는 재사용 workflow를 요구합니다. 출처 없는 claim과 일회성 case는 threshold를 충족하지 못합니다.
- existing skill, default model capability, short rule로 충분한지를 확인합니다. duplicate directory보다 `merge | no-op`을 우선합니다.
- 구분 가능한 positive/negative trigger를 제공합니다. description training과 regression validation을 분리합니다. trigger가 불명확하면 생성을 중지합니다.
- 관찰 가능한 assertion을 포함한 success 및 boundary/failure behavior eval을 하나 이상 포함합니다. raw secret, credential, log, screenshot을 저장하지 않습니다.
- prior skill, no-skill 또는 이름이 있는 baseline과 비교하도록 정의합니다. prose score만으로는 충분하지 않습니다.
- Agent Skills portable-core field와 target-host extension을 분리하고 host별로 body를 복사하지 않습니다. 알 수 없는 target-host invocation은 `pending`으로 남깁니다.
- approval 전 candidate status는 `reported | pending`이며 어떤 file도 applied하지 않습니다. approval 후 성공만 `applied`를 받습니다.

## Draft artifact checkpoint

pre-approval draft는 저장소 루트의 `.tigerkit/learn.md`에만 pending scratch
ledger로 기록합니다. candidate, evidence, checklist, target path, not-created
paths, next step, decision/status를 기록하고 atomic rename 뒤 reread합니다.
missing, stale, 또는 readback mismatch면 `Blocked`이며 approval 질문과
canonical write를 모두 중지합니다. 채팅은 absolute path, 상태, 짧은 요약,
approval question 하나만 보여주고 장부 전문이나 exact file body를 복사하지
않습니다. approval 전 canonical skill path와
`.tigerkit/skill-drafts/<skill-name>/`는 반드시 `not created`입니다.

User-facing progress와 receipt prose는 사용자의 언어를 따릅니다.
