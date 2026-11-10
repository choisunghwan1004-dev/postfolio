# 과제 제출용 README

## 과제명
**통합수업일지 · 데이터 분석 기법 더하기 · 데이터 저널리즘 및 정직한 차트 실습**

2026-11-10 | **실제 과거 로또 데이터와 가상 뉴스·PM10 데이터를 엄격히 구분**

**실제 웹사이트:** https://choisunghwan1004-dev.github.io/postfolio/data-methods-lab-20261109/chart-journalism/

**기존 로또 확률게임:** https://choisunghwan1004-dev.github.io/postfolio/data-methods-lab-20261109/lotto/

## 강의 자료 근거

- **「데이터 분석 기법 더하기.pdf」 14쪽:** 로그축·IQR·표준화·검정·이동평균·비율·RFM/코호트·지도·Plotly·TF-IDF **10종**. 이미 게시한 [로또 과제](../lotto/README.md)의 실제 데이터/가상 데이터 구분과 연결합니다.
- **「빅데이터와 저널리즘 · 기사용 차트 문법 (1).pdf」 20쪽:** 3쪽 '질문→찾기→정제→분석→검증→기사', 8~10쪽 날짜 병합과 어긋난 날 찾기, 13~18쪽 정직한 차트 6가지 규칙, 19~20쪽 차트 3쌍 검수·제출.
- **「데이터 시각화 한눈에 보기_20261109.pdf」 12쪽:** 3쪽 질문→차트 선택, 4쪽 상자·바이올린·카운트·히트맵, 5쪽 제목·축·단위·출처·기준일, 9~11쪽 시각화의 함정과 8개 검수 항목.

원본 교육용 PDF는 공개 저장소에 업로드하지 않았습니다. 교육용 내용을 요약·재구성하여 실습했습니다.

## ① 실제 실행 데이터

- `data/lotto_949_1248_sample.csv`: 이전 제출자가 제공한 로또 기록 중 949~1248회 300회차의 번호/날짜 일부, 마지막 날짜 **2026-10-31**. 최신 로또 자료가 아님. 번호 예측력 주장 아님.
- `data/synthetic_news_articles.csv`: **가상 기사 425건**, 제목도 가상.
- `data/synthetic_pm10_daily.csv`: **가상 PM10 85일치**. 실제 관측 자료가 아님.
- `data/synthetic_news_pm10_joined.csv`: 날짜별 기사 수를 계산한 뒤 가상 PM10과 left merge 한 85행.
- `data/analysis_results.json`: Python에서 재계산한 데이터 검증/상관/어긋난 날짜/로또 결과 요약.

**계산 결과:**

| 항목 | 결과 | 해석·주의 |
|---|---:|---|
| 가상 관측 일수 | 85일 | 날짜 2026-08-01~10-24 |
| 가상 기사 수 | 425건 | 수업용으로 생성 |
| 기사 없는 날 | 4일 | 날짜 조인 시 0 처리 |
| 가상 기사 수–PM10 상관 | -0.165 | 원인 아님, 가상 상관 |
| 가상 기사 많고 PM10 낮은 날 | 4일 | 중앙값 미만 + 기사 상위 10% 초과 |
| 로또 최근 60회 번호 최다 | 38번 13회 | 미래 출현 확률 향상 아님 |
| 로또 백테스트 평균 일치 | 무작위 0.913개 | 150회차 과거 시험/전략마다 1게임 |

## ② 3쌍(6개) 차트 고치기 전·후

| 차트 | 잘못된 표현 | 교정 후 | 연결 규칙 |
|---|---|---|---|
| 01. 최근 60회차의 로또 번호별 등장 횟수 | [`01_before_truncated_axis.png`](charts/01_before_truncated_axis.png) | [`01_after_zero_axis.png`](charts/01_after_zero_axis.png) | 막대는 0부터 |
| 02. 가상 뉴스 건수와 가상 PM10 | [`02_before_dual_axis.png`](charts/02_before_dual_axis.png) | [`02_after_shared_dates.png`](charts/02_after_shared_dates.png) | 축 하나, 단위 다르면 두 칸 |
| 03. 로또 150회차 시간순 백테스트 | [`03_before_unfocused.png`](charts/03_before_unfocused.png) | [`03_after_one_highlight.png`](charts/03_after_one_highlight.png) | 강조색은 하나 + 정확한 제목 |


모든 차트에 **제목(핵심 결론), 축·단위, 출처·기간, 라벨**을 넣습니다. **수정 전 그래프는 의도적으로 오류를 넣은 교육용 예시**이므로 실제 기사에 사용하지 않습니다.

**추가 차트 2개:** 가상 뉴스-PM10 산점도(`04_scatter_relationship.png`), 실제 과거 로또 홀짝×연속번호 히트맵(`05_heatmap_lotto.png`). 총 **PNG 8장, GitHub 표시용 SVG 8장**.

## ③ 정직한 차트 6가지 필수 규칙

1. 막대는 0부터 시작한다.
2. 서로 다른 지표는 이중 축보다 **같은 날짜의 위아래 두 칸**으로 나눠 보여준다.
3. 강조색은 하나만 사용한다.
4. 제목은 기사 결론이 보이는 문장으로 쓴다.
5. 출처·기간·단위·축 이름을 빠짐없이 표시한다.
6. 색만으로 의미를 전달하지 않고 수치·이름을 함께 적는다.

**추가 검수:** 원본 숫자와 차트가 일치하는가, 상관을 인과로 표현하지 않았는가, AI 초안을 사용했다고 표시했는가.

## ④ 재현 방법

Windows 11 / Python 3.12에서 본 디렉터리 기준:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_analysis.py
.\.venv\Scripts\python.exe -m jupyter notebook
```

`run_analysis.py`는 고정 시드의 가상 뉴스·PM10 데이터와 기존 로또 300회차 CSV를 사용해 숫자와 PNG/SVG를 재생성합니다. `data/lotto_949_1248_sample.csv`는 제공되므로 전체 원본 재다운로드가 필요 없습니다. **의도적 과장 그림은 수정 전 예제로만 사용**하십시오.

### 제출 파일

- `통계확률_기사차트_추가기법_실습.ipynb` — 실제 실행 출력 포함
- `charts/` — 고치기 전/후 3쌍 PNG(6장), 추가 PNG 2장 / GitHub 미리보기 SVG
- `탐사기획서.md` — 1장짜리 질문·출처·분석·검증 기획서
- `차트검수표.md` — 6규칙별 비교 검수
- `run_analysis.py`, `data/*.csv`, `data/analysis_results.json`, `requirements.txt`
- `index.html` — GitHub Pages 실습 결과 화면

## 책임과 한계

**로또는 과거 추첨 자료(949~1248회), 뉴스·PM10은 100% 가상 시뮬레이션**입니다. 두 종류의 데이터를 같은 실제 사건으로 합치지 않습니다. 로또의 각 특정 6개 조합 1등 확률은 균등하게 1/8,145,060이며, 빈도/백테스트가 미래 당첨확률을 높였다는 근거는 없습니다.

**AI 사용 표시:** 초안·코드·시각화는 AI의 도움으로 생성했고, 실제 기사로 게시할 때는 원본 출처를 기자가 확인·수정하고 최종 승인해야 합니다.