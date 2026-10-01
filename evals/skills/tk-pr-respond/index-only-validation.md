# 임시 인덱스 경로 검증

- 검증일: 2026-10-01.
- `Baseline`: `59d97faa4630b338d5f1cfd777bd39bbc0528b45`.
- 반영 대상: `MTGVim/tiger-kit` 상류 저장소 `checkout`. 로컬 설치본은 수정하지 않았습니다.
- 사용자 요청에는 수정과 `main` 반영 권한이 포함되어 있습니다.

## 독립 시나리오 비교

서로 다른 새 에이전트가 현행 리비전과 후보의 소유 스킬/참조 문서를 읽고 다음 요청에 대한 실행 결정을
산출했습니다. 실제 GitHub PR의 원격 CI와 댓글 처리를 실행한 결과는 아닙니다.

| 요청 | 현행 | 후보 |
| --- | --- | --- |
| 관련 없는 변경이 있는 상태 부모, 소실 `worktree`, 승인된 일반 주석 두 줄 수정 | 격리 입증 불가로 Blocked | 승인된 `index-only` 허용, 정확한 범위 검토와 현재 `head` CI 및 발행 의무 충족 뒤 Pass |
| 조건 분기 변경, 로컬 회귀 테스트 필요, 안전한 `workspace` 부재 | Blocked | `workspace` 경로를 요구하고 입증 전 Blocked |
| 푸시된 현재 `head`의 `build`/`test` CI pending | Pending | Pending |
| 승인 후 원격 `head` 변경, `commit-tree` 전 | Blocked | `commit-tree` 전 Blocked |
| 첫 요청을 `tk-pr-sweep`에서 `workspace` 경로 없이 전달 | 전용 `workspace` 요구 | 승인된 정확한 PR/`head`/행/실행 소유권을 `tk-pr-respond`에 전달하여 담당자가 격리를 입증 |

## 실제 Git `plumbing` 검증

실행 소유 로컬 Git 저장소와 `bare` `remote`에서 일반 JavaScript 주석 두 줄을 수정했습니다.
`read-tree → hash-object → update-index --cacheinfo → write-tree → commit-tree`를 실행했고,
`Prettier` `3.9.9`에 `--stdin-filepath src/example.js`로 후보 `stdin`을 전달했습니다.

부모 HEAD/`branch`, 실제 `index` 바이트, `staged`/`unstaged` `diff`와 `untracked` 파일 내용은 커밋 구성 전후 및
`fast-forward` `push` 이후에도 일치했습니다. 커밋에는 승인된 주석 파일만 포함됐으며 관련 없는 `staged` 변경은
포함되지 않았습니다. 원래 파일 `mode`와 단일 부모가 유지됐고 `bare` `remote`의 정확한 `branch`가 후보 SHA와
일치했습니다. 이동한 원격 `head`와 승인된 `base`의 불일치를 다음 커밋 구성 전에 감지했습니다.
`zsh`에서 중괄호 `refspec`과 `$C:refs/...`의 출력 차이도 재현했습니다.
이 실험에는 GitHub CI가 없으므로 실제 CI 통과를 주장하지 않습니다.

## 독립 검수

두 독립 검수자는 `Spec`/AC와 `Quality`/`Standards` 및 `fidelity`/`change-risk`를 검토했습니다.
초기 후보에서 `.tigerkit/`이 무시되지 않은 상태이면 공통 `Artifact` `Paths`가 부모 `.gitignore`를 수정하는 충돌을
발견했고, 별도 검증자가 해당 실행 경로를 확인했습니다. 후보는 기존 유효한 제외 규칙을 선행조건으로
요구하고 부모 `ignore` 설정을 금지하도록 수정됐습니다. 직접 영향받는 경계의 재검수와 최종 계약 검수는
모두 Pass였으며 남은 `Critical`/`Important` 항목은 없었습니다. 이 경계를 별도 `behavior` `eval`로 보존했습니다.

정적 릴리즈 게이트는 행동 계약 보존과 저장소 검사를 증명합니다. 독립 시나리오 평가 및 로컬 `plumbing`
실험과 함께 해석하며, 실제 운영 PR의 CI나 `worktree` 회수 원인을 검증한 것으로 해석하지 않습니다.
