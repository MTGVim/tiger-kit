# Skill discovery 후보

Repository skill은 `.agents/skills/`, `.claude/skills/`, 또는
`.hermes/skills/` 아래에 있을 수 있습니다. User skill은 host의 `.agents`,
`.claude`, `.codex`, 또는 `.hermes` skill directory 아래에 있을 수 있습니다.
Repository와 user rule file은 이 skill의 scope 밖입니다.

실제 path 또는 host-discovery evidence로 current host를 식별하고 해당 host의
native target만 해석합니다. host를 알 수 없으면 target을 지어내지 말고
`Unverifiable`로 둡니다. 한 host의 location을 다른 host에 강제하거나 여러
host로 fan out/synchronize하지 않습니다.
`.tigerkit/`을 persistent registry로 사용하지 않습니다.

## Ownership 증거

edit를 proposal하기 전에 각 candidate path와 관련된 모든 symlink를
resolve합니다. 관찰된 evidence로 ownership을 분류합니다.

- package-manager installation root 또는 manifest
- updater가 관리하는 marker, version file, update metadata
- external installation root로 resolve되는 version/current file 또는 directory
  symlink
- user authorship를 보여주거나 보여주지 않는 확인 가능한 author history

약한 signal 하나만으로 결론 내리지 않으며 user history가 없다는 사실만으로
vendor ownership을 증명하지 않습니다. path, link, installer, updater,
history evidence를 조합합니다. vendor ownership이 확인된 candidate는
`keep (vendor)` report-only로 처리합니다. Unknown ownership은 edit proposal
전에 user decision 하나가 필요합니다. active conversation 또는 durable
governing source에 이미 있는 explicit exclusion을 존중하고 hidden global
state나 `.tigerkit/`에 저장하지 않습니다.

User-facing progress와 receipt prose는 사용자의 언어를 따릅니다.
