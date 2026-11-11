# 통계기법 AI V1.0 구조·화면·저장 설계

## 사용자 입력→결과 흐름
1. 파일 형식(CSV/Parquet/Excel/API/DB)과 권한 확인. V1 자동검사는 CSV만.
2. 현 PC의 RAM, CPU, GPU, 사용 가능 디스크, 클러스터 유무 입력(자동 탐지·결과 조작 금지).
3. 분석 목적 선택: 품질/요약/시계열/비교/관계/예측/분류/군집/텍스트/확률/딥러닝.
4. CSV 최대 500행 표본의 컬럼·결측·형식 힌트 표시. 전체 데이터의 결측 개수는 아직 계산하지 않음.
5. 통계 기법 후보 카드: 쉬운 해설, 필요한 자료, 조건 질문, 추천 이유, 금지할 해석.
6. 처리 후보 엔진(pandas/Polars/Dask/Ray/PySpark)와 설치/메모리 위험·속도 미확인 표시.
7. 사람 승인 후 작업 실행: V1 pandas 기본 그룹별 평균/count; Dask/Polars 선택 실행은 설치 환경 필요.
8. JSON 결과·검수 로그 저장, 재실행 코드와 입력 출처 식별.

## 1차 화면 설계 (후속 UI 개발)
- 좌측: 데이터 등록/원본 출처/형식/크기, 개인정보 체크.
- 중앙 상단: 목적·변수·분할·결측 처리·메모리/GPU 조건.
- 중앙 하단: 추천 기법 3개/추천 엔진+대체안/예제/검증 주의.
- 우측: 미리보기·결과·Python 코드·작업 실행 상태·오류.
- PC: 3열, 모바일: 1열 단계형. 기존 V2.6 UI 연결 전 원본 확보/회귀 테스트.

## 저장 구조 제안
- `datasets`: dataset_id, original_name, content_sha256, source_uri, format, bytes, permissions, loaded_at.
- `profiles`: profile_id, dataset_id, sampled_rows, missing_sample, column_types, sampled_at.
- `plans`: plan_id, profile_id, goal, question, selected_columns, selected_method, selected_engine, constraints_json, approval_status.
- `runs`: run_id, plan_id, start_utc, end_utc, status, versions_json, seed, input_hash, error_message.
- `outputs`: output_id, run_id, file_path, sha256, result_metadata, independently_verified.
- `source_ledger`: source_id, uri, access_checked, license, access_scope, privacy_state.

실제 DB 마이그레이션이나 대용량 로컬 저장은 구현되지 않음. API 키/비공개 원본은 GitHub에 올리지 않음.

## 원본 보존/재개발 승인
REA 조사·출력은 **노션 지시문만 등록해도 실제 실행이 아니다**. 독립 실행 로그가 제출되면 사용자가 기존 통계연구소 원본/두 안정 버전 ZIP을 확인 후 ChatGPT가 통합한다. SHAI·제어 엔진 소스나 UI를 끌어오지 않음.
