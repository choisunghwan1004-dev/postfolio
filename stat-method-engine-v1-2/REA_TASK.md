# REA 분석 의뢰 001 — 대용량 분석·분산 ML 엔진 비교

## 역할
기존 통계연구소 분석 의뢰(Orange3, PyGWalker, ydata-profiling, KNIME)를 보완하되 완료로 간주하지 않는다. Dask, Polars, Ray, PySpark(MLlib) 공식 문서·설치·라이선스·최신 호환성과 실제 실행 근거를 조사한다. REA 분석 결과는 개발 승인과 별개다.

## 공식 소스
- Dask: https://github.com/dask/dask  / https://docs.dask.org/
- Polars: https://github.com/pola-rs/polars / https://docs.pola.rs/
- Ray: https://github.com/ray-project/ray / https://docs.ray.io/
- Spark: https://github.com/apache/spark / https://spark.apache.org/docs/latest/ml-guide.html

## 공통 테스트
1. 동일한 작은 CSV와 큰 합성 CSV(실측/합성 구분) 입력, 샘플 추출, 숫자·문자·날짜형 구분, 인코딩 오류 검사.
2. 동일한 그룹별 count/mean, 누락값 처리 규칙, 기간 필터, 교차분석을 pandas와 비교해 오차 확인.
3. 100MB/1GB 이상에서 최대 메모리·시간·CPU, Parquet 저장, 중도 취소, 재시작 측정. 임의 성능 수치 작성 금지.
4. Ray: CPU/단일 GPU/멀티 워커별 Train/Tune 기능과 오류 복구 검증. 실제 GPU가 없으면 미검증.
5. PySpark: SparkSession, DataFrame 입력, spark.ml 분류·회귀 Pipeline, 시간순 분할/평가, Windows Java 환경 검사.
6. 각 프레임워크 Python 버전, OS, 라이선스, 설치 사이즈/호환성, 컴퓨팅 비용·클라우드 권한 점검.
7. Orange3/PyGWalker/ydata-profiling/KNIME 기존 REA 조사와 연결 가능성 및 채택/제외 보고.

## 반드시 제출
| 항목 | 증거 |
|---|---|
| 버전·라이선스 | 공식 저장소 URL, commit/tag, 라이선스 원문 |
| 설치 재현 | Python/Java/GPU/RAM 및 명령과 설치 로그 |
| 성능 | 동일 CSV, 행 수·dtype·정답 계산·결측 비교, 소요시간/피크 메모리 |
| 실패·제약 | 미실행·실패·제약 구분, 오류 전문 |
| 개발 권고 | 재사용/재개발/제외, 보안 및 라이선스 위험 |
| UI 적용 | 초보자 조건 입력 → 선택 근거 → 실행 계획 → 결과·함수 설명 동선 |

## 승인 게이트
REA 조사 전: 계획만 작성. REA 실행 증거 수령: ChatGPT 독립 검증. 기존 통계 엔진 원본 ZIP/직전 안정본 확보 후 통합 재개발. 기존 UI·State·CSS·API는 보존. 두 정상본 ZIP을 Notion과 Drive에 실제 보관하고 SHA-256/복원 확인. 승인 없이 배포하지 않는다.
