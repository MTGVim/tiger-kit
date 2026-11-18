<a id="document-assembly"></a>
# 한 페이지 HTML 조립

사람에게 전달하는 한 페이지 설명·조사·비교 문서는 [렌더러 계약](renderer-contract.md)의 보고서 프로필을 사용합니다. 기존 reader 셸이나 3단 목차를 선택하지 않습니다. archify와 제품 고유 UI, 검증용 route/harness는 담당 스킬의 별도 계약을 따릅니다.

원고는 UTF-8 Markdown으로 작성하며 첫 줄은 `# 제목`, 본문은 `## 절 제목`으로 구성합니다. 추가 HTML·CSS·JavaScript 상호작용이 필요하면 원고에 `[[figure:이름]]`을 놓고 별도 `<figures>/이름.html` 조각에 검토한 `<style>`과 `<script>`를 포함합니다. 신뢰할 수 없는 원고나 스크립트를 자동으로 실행하지 않습니다. 근거와 인용의 식별자, 접근 날짜 및 페이지 내 링크를 보존합니다.

```bash
python3 <tk-writing>/scripts/build_report.py <scratch>/manuscript.md <scratch>/report.html --figures <scratch>/figures
python3 <tk-writing>/scripts/package_html.py --root <final-directory> --name report.html report.html
python3 <tk-writing>/scripts/package_html.py --check --root <final-directory> --name report.html report.html
```

그림 조각이 없으면 `--figures`를 생략합니다. `<tk-writing>`은 현재 설치된 스킬 모음에서 찾습니다. 원고, 조각 및 최종 출력은 설치 패키지 밖의 승인된 위치에 둡니다. 빌더의 옵션은 `--css`, `--js`, `--lang`, `--toc-label`, `--allow-missing-figures`이며, 누락 조각을 허용하는 옵션은 검증을 위한 임시 출력에만 사용합니다.

최종 결과에 공통 피드백 Studio를 주입한 경우에는 이후 다시 패키징하고 `package_html.py --check`를 실행합니다. 페이지의 테마·글자 크기·다운로드와 상호작용은 실제 브라우저에서 별도로 확인하며 정적 통과만으로 동작 성공을 주장하지 않습니다. 출력에 실패하면 원본과 근거를 보존하고 해당 출력 분기의 검증 불가를 보고합니다.
