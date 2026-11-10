# REA 분석 지시 001 — 대용량 데이터 처리·분산 학습 엔진

참조 노션: [기존 통계연구소 REA 4종 지시](https://app.notion.com/p/40928cb9cfd7819e98c8e9c148d6c75d)
개발 ZIP: [초기 독립 패키지](https://drive.google.com/file/d/1m_p1C_ApR-2A5l_pwLhiHSHafSJ232vr/view?usp=drivesdk)

## 목표
기존 Orange3/PyGWalker/ydata-profiling/KNIME 분석 지시와 통합하여 Dask, Polars, Ray, PySpark(MLlib)을 **동일 CSV로 비교**하라.
원본 통계연구소 V2.6, 기존 UI·상태·스타일·API는 수정하지 말고 분석 결과를 ChatGPT 검수 후 재개발에 인계하라.

## REA 필수 조사 대상
| 대상 | 공식 소스 | 핵심 조사 |
|---|---|---|
| Dask | https://github.com/dask/dask | pandas 유사 API, partition, compute, RAM, shuffle |
| Polars | https://github.com/pola-rs/polars | lazy/streaming, API 차이, 메모리, 형 변환 |
| Ray | https://github.com/ray-project/ray | Ray Data/Train/Tune, GPU, checkpoint, 오류 복구 |
| PySpark | https://github.com/apache/spark | SparkSession, DataFrame, spark.ml pipeline, Java/OS |

## 공통 테스트·제출
1. 공식 버전/커밋/라이선스/설치 Python·Java·GPU 조건 명시.
2. 동일한 샘플 CSV를 전 도구에서 읽어 집단별 count/mean, 결측·형식 확인. pandas 결과와 재현 가능한 비교.
3. 가능한 경우 100MB/1GB 이상 합성 CSV의 시간·최대 메모리·스케일 측정. 테스트하지 않은 성능 수치 작성 금지.
4. 원본 보존·예상 RAM·데이터 누출·인코딩·예외·중단·복원·Parquet 변환 검토.
5. Ray 실제 멀티 워커 및 PySpark `spark.ml` 모델 평가. 장비/설치 없으면 미실행 표시.
6. 기존 4종 GUI 도구와 기능 중복·라이선스·Windows/모바일 제약.
7. 결과: 소스 URL, 실행 명령, PASS/FAIL 로그, 스크린샷, 버전, 채택/보류/재개발 결론.

## 총괄 검증·승인 게이트
REA 실행 지시 등록 ≠ REA 실행 완료. 결과 수령 → ChatGPT 독립 재검산 → 통계기법 AI 엔진에 선택 모듈만 통합.
기존 통계연구소 원본 ZIP, 직전 안정본, 새 검증본 **두 개**를 버전·SHA-256과 함께 백업한 뒤 통합/배포.
사용자 최종 승인 전 공개 배포 금지.

## 상태
작업지시 작성 완료 / 실제 REA 실행 **대기** / 네 프레임워크의 실측·성능 결과 **미검증**.
