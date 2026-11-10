# 통계기법 AI · 데이터 조건 추천 엔진 V1.0 (독립 개발 패키지)

## 현재 위치
[**실제 개발 소스 ZIP / 17개 파일 (Google Drive)**](https://drive.google.com/file/d/1m_p1C_ApR-2A5l_pwLhiHSHafSJ232vr/view?usp=drivesdk)

ZIP SHA-256: `e436e867a913d341a369329147fd4080c780336a309d25cfa139d3c972df869a`
ZIP 무결성 테스트 완료, Python unittest **6/6 PASS**.
GitHub에는 ZIP의 17개 파일에 해당하는 소스·설명·샘플·테스트 기록을 같은 폴더에 동기화했습니다. 기존 README는 프로젝트 개요용으로 별도 유지하며, **최종 복원 기준은 manifest와 SHA-256이 기록된 Drive ZIP**입니다.

## 구현된 내용
- `engine.py`: CSV 500행 제한 표본 읽기, 열·결측·형식 힌트, 통계기법 후보·필수조건·주의점 추천, RAM/목적별 pandas/Polars/Dask/Ray/PySpark 엔진 제안
- `run_group.py`: pandas 집계 실제 실행 / Dask·Polars 선택 실행 어댑터(환경 미설치로 미검증)
- `app_streamlit.py`: 선택형 로컬 UI 소스(실제 브라우저 실행 미검증)
- `METHOD_CATALOG.md`: 통계·확률·머신러닝·딥러닝·대규모 처리·시각화·텍스트 등 방법 목록
- `ARCHITECTURE.md`: 조건 추천 흐름, 사용자 화면, DB/감사 기록 설계
- `REA_TASK.md`: Dask/Polars/Ray/PySpark 조사 및 기존 Orange3·KNIME 등 연계 지시
- `tests/test_engine.py`: 검증 테스트 6개
- `manifest.json`: 소스 파일별 SHA-256 기록

## 사용 예
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-base.txt
.\.venv\Scripts\python.exe engine.py --csv examples/sample_air.csv --goal trend --ram-gb 8 --out results/recommendation.json
.\.venv\Scripts\python.exe run_group.py --csv examples/sample_air.csv --group site --value pm10 --backend pandas
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## 도입 기준
| 데이터와 요구 | 추천 후보 | 확인 조건 |
|---|---|---|
| 작고 RAM에 충분 | pandas | dtype, 결측, 원본 크기 |
| pandas 형태를 유지한 대용량 집계 | Dask | API 차이, compute(), 파티션 |
| Lazy/columnar 대용량 집계 | Polars | pandas 문법과 다름, streaming 지원 연산 |
| 분산 모델 학습/튜닝 | Ray | GPU, 워커, 클러스터/비용 |
| 대규모 ETL 및 ML Pipeline | PySpark spark.ml | Java, Spark cluster, MLlib |

## 미실행
REA 에이전트 실행, Ray/PySpark 실분산 학습, Dask/Polars 설치 후 정합성·성능 비교, 기존 통계연구소 UI 통합, Windows/모바일 실기기 검증.
**기존 통계연구소·SHAI·제어 프로젝트 소스는 변경하지 않았음.**
