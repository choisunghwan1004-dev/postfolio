# 통합수업일지 데이터 분석기법 실습관 (2026-11-09)

> **전 데이터가 교육용 가상 데이터입니다. 실제 스포츠센터·고객·여론·영화 소비 통계가 아니며, 기사나 정책의 사실 근거로 사용할 수 없습니다.**

## 웹에서 실제 결과 보기

- **시각화 실습관:** https://choisunghwan1004-dev.github.io/postfolio/data-methods-lab-20261109/
- [원본 수업 통합수업일지](https://docs.google.com/document/d/1vSeKZW3o3qWyyTn_n1IAkFmWvDxNO4j2cfKaMQaIZtk/edit)
- [기존 K-pop × Olist 과제](../mbc-kpop-olist-20261109/)

## 수업일지 → 기법 → 코드 매칭

| 수업일지 | 기법 | 적용 데이터/코드 |
|---|---|---|
| 10/29, 11/02 | Pandas: read_csv/head/info/describe | 원본 가상 회원 50행·기술통계 |
| 10/29, 11/02 | 중복·결측: drop_duplicates, fillna, dropna | 중복 2행, 요금 3건·방문 1건·만족 2건의 결측 처리 |
| 11/02 | groupby/agg/merge | A/B 프로그램별 월평균 방문: 8.54회 / 10.42회 |
| 10/28, 11/02 | corr 상관 | 활동 개월·방문수의 피어슨 r=0.6374 |
| 10/29~10/30 | Welch t-test / p-value | A/B 방문 평균 검정 p=0.025388 (인과관계 아님) |
| 10/30, 11/02 | 선형/다중회귀, train_test_split | 훈련36·테스트12, MAE=2.3875, R²=−0.2779 |
| 11/02, 11/09 | StandardScaler 및 Log 변환·로그축 개념 | 단위 다른 변수의 표준화; 로그축과 표준화 구분 |
| 10/30, 11/02 | K-Means · Elbow | k=2~6 SSE 계산, k=3에서 군집 14·16·18명 |
| 11/02 | 코사인 유사도 · KNN 영화 추천 | 영화A → B(0.974) · E(0.838) · F(0.4174) |
| 11/03, 11/09 | 데이터 종류별 기법 지도, 차트 문법, 결과 해석 | 기법 선택·질문/코드/결과/한계 문서 및 웹 화면 |

**원본 수업 자료:** 10/29의 `DA_01` 결측·t-test, 10/30 `DA_02` 통계/회귀/군집, 11/02 병아리·자동차연비·스포츠센터·영화 미니 예제, 11/03 분석기법 지도, 11/09 Matplotlib/Seaborn과 결과물 제출.

## 예제 데이터

- [sports_center_members_demo.csv](data/sports_center_members_demo.csv) — 가상 원본 50행(고유 회원 48명 + 고의 중복 2행)
- [program_metadata_demo.csv](data/program_metadata_demo.csv) — merge를 위한 A/B 프로그램 설명
- [movie_ratings_demo.csv](data/movie_ratings_demo.csv) — 영화 6편 × 평점 입력자 5명의 가상 평점
- [analysis_results.json](data/analysis_results.json) — pandas, SciPy, scikit-learn 실제 계산 결과
- [통합일지_분석기법_예제실습.ipynb](통합일지_분석기법_예제실습.ipynb) — 복습용 Jupyter 노트북, 파일 내 코드 셀을 직접 실행하는 형태
- [analysis.py](analysis.py) — 가상 CSV를 읽어 모든 통계·모델·요약 JSON을 재생성
- [검수기록.md](검수기록.md) — 실제 계산 결과·실행 범위·모형 성능 한계
- [figures/](figures/) — GitHub Pages에 표시하는 SVG 차트 5개

## Windows 11 + Python 실행

```powershell
# 이 폴더에서 실행; SHAI/ComfyUI 가상환경과 분리
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe analysis.py
.\.venv\Scripts\python.exe -m notebook
```

**브라우저:** GitHub Pages에서 `index.html`을 열면 원자료 CSV를 직접 읽어 결측 처리 방식과 영화 추천 기준을 바꿔 볼 수 있습니다. **브라우저는 SciPy의 t-검정/회귀/KMeans를 새로 학습하지 않고 Python에서 검증한 결과 JSON의 수치를 보여줍니다.** 반면 결측 처리와 코사인 추천 인터랙션은 브라우저 안에서 CSV 값으로 계산합니다.

## 윤리·검증 기록

- **가상/실측 구분:** 이 페이지의 모든 회원·영화 수치는 가상입니다. 기존 K-pop·Olist 포트폴리오의 실측·수업집계 수치와 결합하지 않았습니다.
- **p값:** 가상 데이터에서 `p=0.025388`은 프로그램 효과의 증명이 아니며 인과관계를 말할 수 없습니다.
- **회귀 평가:** 테스트 R²가 `−0.2779`로 좋지 않으므로 예측기를 실제 현장에 적용하지 않습니다.
- **군집 해석:** k=3은 설명을 위한 선택이며 실제 최적 k가 확정된 게 아닙니다.
- **누락 처리:** 중앙값 대치는 실습상 선택입니다. 실제 데이터에서는 결측 발생 원인부터 확인해야 합니다.
- **실제 실행:** Python pandas/SciPy/scikit-learn 코드로 CSV 생성·정제·통계·회귀·군집·추천 계산과 SVG/PNG 차트 생성 테스트를 수행했습니다. GitHub에 공개된 원본 CSV와 결과 JSON을 통해 재현할 수 있습니다.
- **권리:** 실제 인물 사진·목소리·외부 음원을 사용하지 않았습니다.

기존 `postfolio`의 K-pop/Olist 화면·소스는 유지하고 링크만 추가했습니다.


## 추가 과제: 로또 6/45 통계 + 분석 기법 더하기 PDF 10종

- [실제 분석 웹페이지](https://choisunghwan1004-dev.github.io/postfolio/data-methods-lab-20261109/lotto/)
- [로또 분석 자료·노트북·CSV·시각화·검수기록](lotto/README.md)
- 사용자 제공 CSV 949~1248회 300회차 분석. **미래 로또 당첨을 예측하거나 당첨확률을 높인다는 주장 아님.** PDF의 RFM·지역·TF-IDF는 별도 가상 자료 사용.
