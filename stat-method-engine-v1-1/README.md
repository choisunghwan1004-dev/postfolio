# 통계기법 AI 엔진 V1.1 후보 — 검증·재개발 분리본

**배포 상태: 독립 검증 후보. SHAI 통합/독립 운영 결정 보류.**

# 통계기법 AI · 데이터 조건 추천 엔진 V1.0

## 상태
**분석 조건 추천·CSV 표본 검사·기본 집계의 초기 독립 패키지.** 기존 통계연구소 UI나 REA 본체에 연결하지 않았다. Dask/Polars/Ray/PySpark 실행 완료를 의미하지 않는다.

## 처리 흐름
질문/목적 선택 → CSV **최대 500행 표본**과 파일 크기 검사 → 통계 기법 후보/필수 조건/주의점 안내 → 데이터 크기·RAM·GPU·클러스터 조건으로 pandas/Polars/Dask/Ray/PySpark 후보 추천 → 사용자가 승인한 작은 작업만 실행 → 근거·결과·오류 기록.

**주의:** CSV 파일 크기만으로 RAM 사용량을 정확히 예측할 수 없다. 엔진 추천은 휴리스틱으로서 100MB/1GB 등의 확정 문턱이 아니다. 모든 표본 수치는 전체 통계라고 주장하지 않는다. 라이선스/권리 없는 데이터·키는 저장하지 않는다.

## 사용
Windows PowerShell에서 이 폴더를 연다.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-base.txt
.\.venv\Scripts\python.exe engine.py --csv examples/sample_air.csv --goal trend --ram-gb 8 --out results/recommendation.json
.\.venv\Scripts\python.exe run_group.py --csv examples/sample_air.csv --group site --value pm10 --backend pandas --out results/group_result.json
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

분석 목적: `quality`, `summary`, `trend`, `relationship`, `difference`, `prediction`, `classification`, `segmentation`, `text`, `probability`, `deep_learning`.

실측 대기질 원본을 별도 보유한 경우 경로와 `--encoding cp949` 등을 명시하고, **원본은 변경하지 않음**.

## 선택 예시
| 데이터/상황 | 추천 분석 | 후보 엔진 | 먼저 확인할 조건 |
|---|---|---|---|
| 작은 관측 CSV | 기술통계·시계열 | pandas | 날짜·단위·결측 |
| 큰 CSV, pandas 문법 익숙 | 그룹 집계·분할 | Dask | 파티션·RAM·집계 compute 크기 |
| 큰 컬럼형 집계, 속도 중요 | lazy query·집계 | Polars | pandas 문법과 차이, 스트리밍 가능 연산 |
| 분산 PyTorch/모델 튜닝 | 분산 학습 | Ray Train/Tune | GPU·워커·체크포인트 |
| 다수 노드 ETL+ML | Spark DataFrame+MLlib | PySpark (spark.ml) | Java·클러스터·파이프라인 |
| Olist 판매자 | 분류/예측 | sklearn→Ray/Spark 조건부 | 레이블·유출·정밀도/재현율 |
| 로또 과거 당첨 | 빈도·확률·백테스트 | pandas(기본) | 미래 누출 방지, 독립 시행, 예측력 주장 금지 |
| 기사 제목 | TF-IDF/임베딩/군집 | sklearn→Ray 조건부 | 기사 저작권·표본 편향 |

## 실행 기능 범위
- `engine.py`: 표본 열 추정, 날짜 열 이름 힌트, 방법 후보, 필수 조건, 엔진 추천 JSON. **실제 분석/학습이 아닌 추천**.
- `run_group.py`: pandas/Dask/Polars 중 **직접 선택한 라이브러리가 설치된 경우에 한해** 그룹별 비결측 count와 평균 실행. 자동 전환하지 않음.
- Ray/PySpark: 현재 **기획/설치 체크·REA 비교 대상**, 실분산 실행은 아직 아님.
- `REA_TASK.md`: 기존 REA 조사 → 증거 검수 → ChatGPT 재개발 작업지시.

## 기록 기준
계획 / 로컬 Python 실행 / 타 프레임워크 설치 / GPU/클러스터 시험 / REA 조사 / UI 통합 / PC·모바일 검증을 각각 구별. 기존 통계연구소 원본 ZIP 및 직전 안정본은 보존한 뒤 후속 통합.

## 참고
- Dask: https://docs.dask.org/en/latest/dataframe-best-practices.html
- Polars: https://docs.pola.rs/user-guide/lazy/using/
- Ray: https://docs.ray.io/en/latest/ray-overview/
- Spark MLlib: https://spark.apache.org/docs/latest/ml-guide.html

## 선택형 브라우저 화면
`pip install streamlit` 후 `streamlit run app_streamlit.py` 실행. 데이터 경로·목적·RAM·GPU·클러스터를 선택하면 기법·조건 카드를 보여주고 추천 JSON을 저장합니다. **실제 브라우저 UI/모바일 회귀 테스트는 미실행**. 로컬에 파일 경로를 입력하므로 외부 공개 배포 전 사용자 인증과 경로 제한이 필요합니다.


## V1.1 검수 결과 (2026-11-11)
- V1.0 원본 보존; 기존 기능과 UI 소스를 변경·삭제하지 않음.
- Python 3.13.5 · pandas 로컬 환경에서 unittest **18/18 통과**.
- 실제 수업 `data_air_2022.csv` CP949 표본 500행 검사 및 전체 CSV pandas 집계: 종로구 PM10 비결측 673건, 평균 33.09806835066865 (원자료 단위/기간 별도 확인).
- 빈 그룹/비수치 값, 유효하지 않은 컬럼, CSV 헤더, RAM NaN/무한대, 그룹 결과 제한, UTF-8 전제 검증을 추가.
- 엔진 추천은 용량/RAM 휴리스틱이며 각 백엔드의 설치·실행 가능성은 `availability: not_checked`로 표시.
- 현재 개발 컨테이너에는 Dask/Polars/Ray/PySpark/Streamlit이 설치되지 않아 **네 프레임워크 실제 엔드투엔드 실행·성능 비교 미완료**.
- Dask/Polars에서 CP949를 묵시적 손실 인코딩으로 읽지 않음. 필요 시 승인된 UTF-8 변환 단계를 별도 개발.
- 핵심 코드는 `engine.py`, `run_group.py`에 있으며 UI는 `app_streamlit.py` 원형 그대로 유지.
- V1.1 최종 승인 조건: Dask/Polars의 동일 입력 기준 pandas 대조 PASS, Ray/PySpark 실제 학습/분산 시험, UI/Windows/모바일 회귀 시험, 실행·복원 및 ZIP 백업 검증.

### 명령 예제
```powershell
py -3.12 -m unittest discover -s tests -v
py -3.12 engine.py --csv examples/sample_air.csv --goal trend --ram-gb 8
py -3.12 run_group.py --csv examples/sample_air.csv --group site --value pm10 --backend pandas
```
