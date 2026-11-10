# V1.0 → V1.1 원본 대조·검수 기록

## 원본 확인
- V1.0 원본: `통계기법_AI_엔진_V1_조건추천_REA_개발패키지.zip` 보존.
- V1.1 신규 독립 폴더를 통해 수정. 기존 Streamlit 화면/문구/상태를 그대로 유지.

## 결함 및 수정 필요성
| V1.0 관찰 | 위험 | V1.1 조치 |
|---|---|---|
| `groupby` 엔진마다 결측 그룹 정책이 달라질 수 있음 | 교차 엔진 결과 불일치 | `dropna=False`와 null 정규화 추가, 실제 Dask 결과 후속 확인 |
| Polars CP949를 `utf8-lossy`로 읽을 수 있음 | 조용한 문자 손실 | UTF-8이 아닌 입력을 명시 차단 |
| pandas 결과를 `.to_dict`로 바로 JSON 출력 | pandas.NA / NaN 직렬화 오류 | 집계 결과 count/mean/그룹값을 JSON 안전형으로 정규화 |
| 그룹 수 무제한 materialize | 메모리 사용 급증 위험 | 10000 그룹 결과 상한 추가. 다만 backend 내부 collect 전에 상한을 계산하지 않아 메모리 상한을 보장하는 것은 아님 |
| 결과 숫자가 아닌 CSV 행·중복 헤더가 있을 수 있음 | 부정확한 프로파일 | 열 수 초과·중복·빈 헤더 탐지 강화 |
| 무효 RAM NaN/Inf, 없는 분석 목적 | 엔진 추천 불안정 | 입력 검증 및 실패 테스트 |
| 추천 backend가 설치된 것처럼 오해 | 실행 실패·오해 | availability=not_checked 추가 |

## 검증 증거
- Python 3.13.5, `python -m unittest discover -s tests -v`: **18 PASS**.
- Python 컴파일 검사: engine.py, run_group.py, app_streamlit.py, tests **PASS**.
- V1.0 대비 12개 추가 테스트, pandas 기본 집계·누락 그룹·비숫자·최대 그룹 수·CP949 원본 보존 포함.
- `data_air_2022.csv`: 파일 CP949 표본 검사 500행, pandas 전체 집계 종로구 PM10 count=673, mean=33.09806835066865.

## 미검증·확정 보류
- Polars: 라이브러리 미설치, 실제 scan/streaming 동작 미실행.
- Dask: 라이브러리 미설치, 파티션·그룹 집계·결측 그룹 일치 미실행.
- Ray: 라이브러리 미설치, 멀티 워커·GPU 분산 훈련 미실행.
- PySpark: 라이브러리 미설치, Java·Spark/MLlib 실행 미실행.
- Streamlit: 라이브러리 미설치, 실제 브라우저 UI·실기기 미실행.
- REA 실제 연구/테스트 로그는 수령하지 않았음. 기존 노션 의뢰만 확인.
- 장비/비용/운영권한 및 SHAI와의 통합 결정은 보류.

## 조건부 승인 기준
- 현재 단계: **V1.1 검증 후보**, 엔진 확정 아님.
- 통계·집계 함수는 입력 경계 및 실제 데이터를 대상으로 테스트. 대규모 분산·정식 모델 학습은 후속 검증 게이트.
- 기존 안정본 ZIP 및 승인된 새 최종본 ZIP을 각각 보존하고 복원 시험 완료 후 최종 승인.
