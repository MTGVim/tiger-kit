<a id="dependency-and-dependabot-evidence"></a>
# 의존성과 Dependabot 근거

의존성/보안 감사가 선택되면 읽습니다. 로컬에서 해석된 의존성과 제공자의 보안 권고 backlog는 별도의 근거 집합으로 유지합니다.

먼저 관련 manifest와 lockfile을 확인합니다. 영향을 받는 각 manifest, package/ecosystem과 해석된 버전을 보존합니다. 출처가 뒷받침할 때만 직접, 전이 및 알 수 없는 관계를 구분합니다. 확인한 revision과 누락되거나 충돌하는 lockfile 근거를 기록합니다.

감사 대상 저장소가 GitHub에서 식별되고 기존 읽기 접근 권한이 있으면 미해결 Dependabot alert를 확인합니다. 검증된 저장소 host와 식별 정보로 REST 목록 endpoint를 사용하고 `state=open`, 최대 `per_page=100`을 적용합니다. 반환된 Link cursor 또는 기존 client의 동등한 pagination을 끝까지 처리합니다. before/after 대신 추측한 page 번호를 사용하지 않습니다.
요청 범위, 수집 시각, 가능하면 확인한 default-branch revision과 미완료 page를 보존합니다. 완전하고 성공적인 빈 수집은 해당 시각의 해당 제공자 범위에서 열린 alert가 0개라는 뜻일 뿐입니다.

alert 번호/URL, GHSA나 CVE, 심각도, package/ecosystem, manifest, 제공된 경우 의존성 범위/관계, 취약 버전 범위와 null일 수 있는 최초 수정 버전을 보존합니다. package/advisory가 같아도 서로 다른 manifest instance는 유지합니다.
REST alert는 해석된 버전 목록이 아닙니다. 관련 lockfile을 별도로 대조합니다. 없는 필드를 확실한 값으로 말없이 대체하지 않습니다.

부분 수집, 접근 실패, 사용 불가/비활성화된 제공자, 잘못된 데이터나 알 수 없는 범위는 점검 한계로 보고하며 문제가 없는 0개로 보고하지 않습니다. 기존 근거로 로컬 발견 사항을 뒷받침할 수는 있습니다. 감사의 일부로 새 인증 정보를 요청하거나 계정을 연결하거나 접근 범위를 넓히지 않습니다. 필요한 경우에만 그 필요를 인계합니다.

로컬 checkout과 default branch의 노출은 구분합니다. alert 상태를 보존합니다. dismissed/auto-dismissed는 수정됨을 뜻하지 않으며 로컬에서 수정된 의존성이 제공자의 default branch도 수정되었음을 입증하지 않습니다. 명시적이고 검증된 alert-to-PR 관계가 있을 때만 수정 PR을 보고합니다. 버전 업데이트 PR, 일치하는 package 이름이나 merge된 PR만으로는 해당 관계나 개선 완료가 입증되지 않습니다. 확인할 수 없으면 관계나 해결 여부를 미상으로 둡니다. 수정 버전이 없다고 추측성 upgrade를 해도 되는 것은 아닙니다.

읽기 전용을 유지합니다. alert를 dismiss하거나, 의존성/lockfile을 편집하거나, 새 scanner를 설치하거나 실행하거나, PR을 merge하거나, 제공자 설정을 바꾸지 않습니다. 기존 근본 원인별 발견 사항 묶음을 따르면서 영향받은 instance와 감사한 범위/감사하지 않은 범위를 보존합니다.

출처: [REST alert](https://docs.github.com/en/rest/dependabot/alerts#list-dependabot-alerts-for-a-repository),
[페이지네이션](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api).
