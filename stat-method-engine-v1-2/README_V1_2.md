# 통계기법 AI 엔진 V1.2 — 조건 변경·기법 전환·결과 비교

## 목적
수업 원본 `journal-izm/ai-datajournalism-labs`의 시각화, 기사수·PM10 관계, 차트 표현 규칙을 학습 자료로 연결합니다. V1.1 코어 `engine.py`, `run_group.py`, 기존 Streamlit UI는 보존하고, 아래에 **3. 조건을 바꾸며 기법 비교하기**를 추가합니다.

## 실행
```
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-base.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m pip install streamlit
.\.venv\Scripts\python.exe -m streamlit run app_streamlit.py
```
`data_air_2022.csv`는 수업 Google Drive에서 받은 본인의 로컬 파일을 선택하고 인코딩 `cp949`를 지정합니다. 소스와 UI는 공유하지만 실제 Windows 브라우저 실행은 미검증입니다.

## 사용자 흐름
1. CSV 파일·문자 인코딩·기본 분석 목적·RAM/GPU 선택
2. 열 목록과 자료형·결측 *표본* 검사
3. 기법 후보의 **필요 조건**·예시·주의점 확인
4. 기법(기술통계/집단요약/시간이동평균/상관) 변경
5. 날짜 필터/그룹/값 같음 필터/PM10 최소·최대/이동평균 기간 변경
6. 각 실행 결과를 최대 12개 저장해 비교 · JSON 다운로드 · 전체 기록 삭제

* 지원하지 않는 조합은 이유와 함께 차단. 결측은 임의 보정하지 않고 분석별 유효값만 사용합니다.
* V1.2의 기법 실행은 **pandas**로만 검증했습니다. Dask/Polars의 선택 추천은 V1.1에서 유지되며 실연산 동일성은 미검증입니다.
* 학습용 64MiB 이하 CSV만 한 번에 로드합니다. 더 큰 데이터는 검증된 Dask/Polars 어댑터로 이관하기 전 실행을 중단합니다.
* 결과에 인과관계/대표성/통계 검정 결과를 자동 부여하지 않습니다.
* 이 V1.2는 최종 통합 엔진이 아니라 **분리된 검증 후보**입니다. SHAI/독립 운영 여부 보류.

## 검증
- 기존 회귀 테스트 + V1.2 신규 테스트 **32개 PASS**
- 실측 `data_air_2022.csv` CP949, 673행. 6개 조건·기법 실행 PASS, 원본 SHA-256 변경 없음
- 실제 검증 결과: [examples/real_course_comparison.json](examples/real_course_comparison.json)
- 기존 V1.1 디렉토리는 변경하지 않고 별도 V1.2로 복사
- 실제 Dask/Polars/Ray/PySpark 분산 계산·Windows 실기기·Streamlit 시각 검증·REA 실제 조사: **미검증**

## 강의 원본 코드 연결
- 수업 자료 `https://github.com/journal-izm/ai-datajournalism-labs`
- 내 보관본 `https://github.com/choisunghwan1004-dev/postfolio/tree/main/course-source/ai-datajournalism-labs`
- `1_시각화기초/visualization_basics.ipynb`: 선·히스토그램·상자·막대·산점도
- `2_빅데이터_차트문법/1_bigdata_news_vs_air.ipynb`: PM10과 기사 수 상관·시계열
- `2_빅데이터_차트문법/2_chart_grammar.ipynb`: 차트 축·왜곡·비교 원칙

**주의:** 강의 수업자료에는 명시적인 LICENSE 파일을 확인하지 못했으므로 원본 코드를 새로운 제품에 재배포하는 행위는 권리 확인이 필요합니다. V1.2는 자체 모듈을 추가한 개발본으로 보관합니다.
