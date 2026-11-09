# 완성 프로젝트 GitHub 정리 현황 — SHAI/공통 엔진 제외

기록일: 2026-11-09 (KST)

이 문서는 기존 프로젝트 자료를 보존하며 정리하기 위한 **현황 목록**입니다. 'GitHub 저장소 확인', '사이트 주소 확인', '개별 소스 확보', '최종 기능 검증'은 서로 다릅니다. 이 문서를 작성했다고 프로젝트 전체 소스 업로드가 완료된 것은 아닙니다.

## 제외 범위
- SHAI 본체, 통합 챗봇, 공통 엔진과 엔진 개발용 자료
- 신호제어 AI 엔진, 통계기법 AI 엔진
- ComfyUI/Wan 모델 파일, 실험용 워크플로와 점프 테스트 자료
- API 비밀 키, .env 실제 설정, 개인정보, 자격증명, 데이터베이스 운영 데이터

## A. 이미 GitHub 저장소가 확인된 비엔진 프로젝트

| 프로젝트 | GitHub 저장소 | 구분 |
|---|---|---|
| 점심·여행 통합 | [lunch-decision-v8.4.4-approved-sync](https://github.com/choisunghwan1004-dev/lunch-decision-v8.4.4-approved-sync) | 기존 소스 저장소; 다른 버전도 존재 |
| 패션 코디 | [fashion-balance-ai-v1.5-editorial](https://github.com/choisunghwan1004-dev/fashion-balance-ai-v1.5-editorial) | 기존 소스 저장소 |
| 여행 안전 연락망 | [travel-safety-circle](https://github.com/choisunghwan1004-dev/travel-safety-circle) | 기존 소스 저장소 |
| 냉장고 요리·재고 | [smart-fridge-chef-v1](https://github.com/choisunghwan1004-dev/smart-fridge-chef-v1) | 비공개 저장소; 접근권한 필요 |
| 경마 데이터 분석 | [horse_race_analysis_v5](https://github.com/choisunghwan1004-dev/horse_race_analysis_v5) | 기존 소스 저장소 |
| 일상·생활 실습 | [daychange_v1_2_workstyle](https://github.com/choisunghwan1004-dev/daychange_v1_2_workstyle) | 기존 저장소 |
| 탐색 프로젝트 | [my-explore](https://github.com/choisunghwan1004-dev/my-explore) | 기존 저장소; 프로젝트 범위 별도 분류 필요 |
| 기존 포트폴리오 | [postfolio](https://github.com/choisunghwan1004-dev/postfolio) | 사이트·영상·기획 자료 정리본 |

위 표는 **저장소 존재 확인**에 해당합니다. 현재 소스의 기능 완성도, 최신 버전 여부, Windows·모바일 실제 실행 성공 여부는 별도 검증 대상입니다.

## B. 기존 포트폴리오에 링크가 보관된 비엔진 결과물

다음 링크는 기존 `postfolio/README.md`에 이미 기록된 링크입니다.

| 결과물 | 공개 사이트 | 기록 유형 |
|---|---|---|
| 마음씨앗 숲 | https://little-seed-adventure.leafytiger512.chatgpt.site | 사이트 및 영상 링크 |
| 다시 내일 | https://tomorrow-choice-journey.leafytiger512.chatgpt.site | 사이트 및 영상 링크 |
| 대한민국 세계를 달리다 | https://korea-world-frontier.leafytiger512.chatgpt.site | 사이트 링크 |
| 그 시절 우리는 — 항일독립투쟁 | https://those-days-we-history.leafytiger512.chatgpt.site | 사이트 링크 |
| 그 시절 우리는 — 한반도 전쟁사 | https://korean-war-history-atlas.leafytiger512.chatgpt.site | 사이트 링크 |
| 함께 짓는 내일 | https://korea-together-tomorrow.leafytiger512.chatgpt.site | 사이트 및 영상 링크 |

**사이트 링크 보관은 원본 소스 코드 GitHub 업로드와 다릅니다.** 사이트가 존재하더라도 전체 소스가 확보되지 않은 항목은 업로드 완료로 표시하지 않습니다.

## C. 프로젝트 점검표에서 확인된 추가 분류 필요 항목

- 일본 지방여행 연구소, 지역 뉴스룸, 주방 재고·예상 발주, 회계 시스템, 한국어 도우미 등은 2026-11-07 점검표에 **부분 검사 또는 소스 검사 기록**이 있습니다.
- 동네친구, 차근차근 수업 도우미, 여행안심 등은 **배포 사이트 주소**가 기록돼 있지만 사이트별 원본 코드 확보 여부를 추가 확인해야 합니다.
- `이름 따라 맛 따라` 로컬 ZIP 패키지는 별도로 확보되어 있으나, 해당 파일을 GitHub에 올리기 전 프로젝트 소스·API 키·저작권·버전 점검이 필요합니다.
- 현재 '완성'이라는 표현은 단순한 소스 존재/정적 사이트 활성 상태와 분리해야 합니다. 완성으로 확정할 프로젝트는 핵심 사용 흐름 실제 실행까지 확인합니다.

## D. 후속 GitHub 업로드 원칙

1. 기존 저장소·UI·실행 기능·Git 이력을 그대로 보존하고, 덮어쓰기보다 신규 폴더/브랜치에서 비교합니다.
2. README, 원본 소스, 실행법, `.env.example`, 라이선스, 테스트 기록을 프로젝트별로 함께 정리합니다.
3. `node_modules/`, 실제 `.env`, API 키, DB 운영 자료, 모델 가중치, 개인 연락처 등은 올리지 않습니다.
4. 엔진 자체와 ComfyUI 실험 자료는 이번 비엔진 프로젝트 업로드에서 제외합니다.
5. 실제 업로드와 검증을 마친 경우에만 해당 프로젝트 상태를 'GitHub 소스 업로드 완료'로 바꿉니다.

**현재 이 문서는 인벤토리(색인)입니다. 일부 프로젝트의 누락된 원본 소스까지 업로드했다는 의미는 아닙니다.**
