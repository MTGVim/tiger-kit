# Skill discovery 후보

Repository 스킬은 `.agents/skills/`, `.claude/skills/`, 또는
`.hermes/skills/` 아래에 있을 수 있습니다. User 스킬은 호스트의 `.agents`,
`.claude`, `.codex`, 또는 `.hermes` 스킬 directory 아래에 있을 수 있습니다.
Repository와 user rule 파일은 이 스킬의 범위 밖입니다.

실제 경로 또는 호스트-discovery 근거로 현재 호스트를 식별하고 해당 호스트의
native 대상만 해석합니다. 호스트를 알 수 없으면 대상을 지어내지 말고
`Unverifiable` 로 둡니다. 한 호스트의 location을 다른 호스트에 강제하거나 여러
호스트로 fan out/synchronize하지 않습니다.
`.tigerkit/` 을 persistent registry로 사용하지 않습니다.

## Ownership 증거

edit를 proposal하기 전에 각 후보 경로와 관련된 모든 symlink를
resolve합니다. 관찰된 근거로 소유권을 분류합니다.

- package-manager installation root 또는 manifest
- updater가 관리하는 marker, version 파일, update metadata
- 외부 installation root로 resolve되는 version/현재 파일 또는 directory
  symlink
- user authorship를 보여주거나 보여주지 않는 확인 가능한 author 이력

약한 signal 하나만으로 결론 내리지 않으며 user 이력가 없다는 사실만으로
vendor 소유권을 증명하지 않습니다. 경로, link, installer, updater,
이력 근거를 조합합니다. vendor 소유권이 확인된 후보는
`keep (vendor)` report-only로 처리합니다. Unknown 소유권은 edit proposal
전에 user 결정 하나가 필요합니다. 활성 conversation 또는 durable
governing 소스에 이미 있는 explicit exclusion을 존중하고 hidden global
상태나 `.tigerkit/` 에 저장하지 않습니다.

User-facing progress와 receipt prose는 사용자의 언어를 따릅니다.
