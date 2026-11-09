# MBC AI 데이터저널리즘 — GitHub 2개 분석과 추가 기법 실습 (제출용)

**검수일:** 2026-11-09  
**과제:** ChatGPT·Claude를 이용한 두 GitHub 분석, 추가 데이터 분석기법 적용, 노트북 1개, PNG 차트 3장 이상, 차트마다 질문과 결과 한 문장, GitHub 링크 공유. Olist 사전학습 tokenizer·Keras 모델로 Streamlit 감성분석 화면 구성.

## 1. 제출 링크와 파일

- **실제 시각화 웹페이지:** https://choisunghwan1004-dev.github.io/postfolio/mbc-kpop-olist-20261109/
- **GitHub 공개 과제 폴더:** https://github.com/choisunghwan1004-dev/postfolio/tree/main/mbc-kpop-olist-20261109
- **실습 노트북 1개:** [KPOP_Olist_데이터분석_실습.ipynb](KPOP_Olist_데이터분석_실습.ipynb) — 전체 23셀, **코드 셀 11개**, 저장된 실행 기록 11개, 오류 출력 0개.
- **PNG 차트 7장:** [charts/](charts/) — **Olist 4장 + Spotify 한국 주간 3장**.
- **입력 CSV:** [Olist 사실표](data/olist_verified_facts.csv), [Spotify 주간 TOP20](data/spotify_kr_weekly_2026-11-05_top20.csv).
- **Python 코드:** [Olist 차트 생성](generate_charts.py), [Spotify 차트 생성](generate_spotify_charts.py), [Streamlit 감성분석](streamlit_app.py), [모델 다운로드](다운로드_모델.py), [실제 예측 검증](실제예측_검증.py).
- **실행 결과 ZIP (Drive):** https://drive.google.com/file/d/1QcId4pkSIB51OMdgqctqUupA46JQeauL/view?usp=drivesdk
- **수업 제출 폴더:** https://drive.google.com/drive/folders/1qCloI4HiTNBCypiVgafhlMQNpVIimIx8

> GitHub에는 재현용 소스와 그래프만 등록했습니다. Python 가상환경, 모델 원본 바이너리, 비밀 API 키는 업로드하지 않았습니다. ZIP의 Windows 배치 파일은 GitHub 폴더의 파일 목록에 없는 별도 배포 보조 파일입니다.

## 2. 분석 대상 GitHub 두 곳

| 원본 | 검토 내용 | 현재 상태 |
|---|---|---|
| [K-pop DATA LAB](https://github.com/dominickim77-ui/mbc-kpop-data) | 2026-11-06 수업 검토 기록: Spotify 주간 CSV, YouTube 누적 조회, MySQL·Chart.js, 로그축; UNIQUE 중복 방지 및 공식 영상 매칭 검증 필요 | 2026-11-09 GitHub API 404. **원본 소스를 현재 재검증하거나 원본 5곡 데이터를 다시 실행할 수 없음.** |
| [Olist Data Analysis](https://github.com/journal-izm/Olist-Data-Analysis) | README, 원본 사실표 F08·F14·F23~F25·F27, 노트북·모델 파일 목록, Streamlit UI 구성 확인 | 공개 파일 확인. 원본 주문 단위 전체 데이터 재학습은 수행하지 않음. |

**대체 Spotify 실습:** [Kworb의 한국 Spotify 주간 차트(2026-11-05)](https://www.kworb.net/spotify/country/kr_weekly.html)에서 상위 20곡을 따로 확보했습니다. 이는 **한국 Spotify 전 장르 차트**이지 K-pop 전용 차트가 아니며 원래 GitHub의 **Spotify 5곡 대 YouTube 누적 조회수 비교**와는 전혀 다른 자료입니다. Kworb는 Spotify 공식 API가 아닌 제3자 집계 사이트입니다.

**Claude 독립 검토:** 실제 Claude 분석 기록이나 결과물을 받지 못했으므로 수행 완료로 표시하지 않았습니다. ChatGPT의 코드 분석·편집과 검증 내역은 구분해 기록합니다.

## 3. 차트 7장 · 질문 → 읽은 결과

| 차트 | 질문 | 데이터로 말할 수 있는 한 줄 | 출처 |
|---|---|---|---|
| [① 배송과 리뷰](charts/01_배송과_리뷰.png) | 배송 시점과 평균 평점은 어떻게 다른가? | 제때 도착 4.30점, 지연 도착 2.57점으로 **1.73점 차이**가 있다. | Olist F14 |
| [② 감성분석 모델](charts/02_감성분석_모델비교.png) | 딥러닝이 항상 가장 높은 정확도를 내는가? | Bigram 머신러닝 **92.6%**, 딥러닝 **92.4%**로 **0.2%p 차이**였다. | Olist F23~F25 |
| [③ 지역별 주문](charts/03_지역별_주문비중.png) | 주문이 어디에 집중되는가? | SP 42.0%, RJ 12.8%, MG 11.8%로 **상위 세 주의 합이 66.6%**다. | Olist F08 |
| [④ 판매자 유형](charts/04_판매자_유형.png) | 판매자 군집 중 어느 유형이 큰가? | **신규 성장형 947명**이 가장 많다. | Olist F27 |
| [⑤ 주간 재생수](charts/05_Spotify_한국주간_상위10.png) | Spotify 한국 주간 TOP10에서 1위는? | **A2O / NEON**이 **1,078,815회**로 1위다. | Kworb, 2026-11-05 |
| [⑥ 전주 대비 증감률](charts/06_Spotify_주간증감률.png) | 누가 가장 크게 늘고 줄었나? | 비교 가능한 19곡 중 **ILLIT +147.15%**, **Jung Kook -37.89%**였다. | Kworb, 2026-11-05 |
| [⑦ TOP20 집중도](charts/07_Spotify_TOP20_집중도.png) | 상위 5곡은 TOP20 합계의 몇 %인가? | TOP20 합계 **8,380,754회** 중 상위 5곡이 **40.63%**를 차지했다. | Kworb, 2026-11-05 |

**주의:** ① 배송 지연이 평점을 낮췄다는 *인과관계*를 입증한 것이 아닙니다. ② 원래 저장소에서 학습한 모델들의 **기존 테스트 성능**을 시각화한 것이며 이 과제에서 모델을 재학습한 수치는 아닙니다. ⑦은 상위 20곡 내부 비중이고 시장 전체 점유율은 아닙니다. 신규 진입 1곡의 전주 값은 0으로 대체하지 않고 변화율 계산에서 제외했습니다.

## 4. 왜 Logarithmic Scale이고 StandardScaler가 아닐까?

| 방법 | 목적 | 데이터가 실제로 바뀌나? | 적용 |
|---|---|---|---|
| **Logarithmic axis** | 크기 차이가 큰 원본 수치를 한 그래프에서 읽기 | 아니오. **눈금만 변경** | Spotify/YouTube처럼 큰 수치 시각화(0값 주의) |
| **`np.log1p(x)`** | 0 이상인 오른쪽 치우친 분포 압축 | 예, `ln(1+x)`로 변환 | 주문 금액, 판매량 등 |
| **`StandardScaler`** | 모델 입력 변수들을 평균 0·표준편차 1로 맞춤 | 예, 학습 평균·표준편차로 변환 | KNN, K-Means, 회귀 등 |

로그축과 표준화는 대체 방법이 아닙니다. 거리 기반 모델에서는 필요에 따라 **log1p → StandardScaler** 순서로 둘 다 적용할 수 있습니다. 변환기 학습은 훈련 데이터에서만 수행해 데이터 누출을 막습니다. Spotify **주간 재생수**와 YouTube **누적 조회수**는 관측 기간이 다르므로 원값끼리 인기 우열을 단정하면 안 됩니다.

## 5. 추가 분석기법: 이번에 적용 / 향후 제안

**실제 적용한 기법:** 데이터 행·결측·중복 확인, 그룹별 평균·비율 표시(Olist 기존 사실표 기반), Spotify 주간 증감률 계산, 상위 5곡 집중도 계산, 막대 및 양·음수 비교 시각화, 로그축 대비 표준화 개념 설명.

**원자료 확보 후 제안할 기법:** K-pop 동일 기간 Spotify/YouTube 자료의 Spearman 순위 상관, YouTube 영상별 공식 채널 검증 및 주간 증가분 비교, 여러 주차 이동평균·이상치 탐지. Olist 원본 주문 데이터로 배송 지연 효과 크기와 혼란변수 확인, 모델 정확도 외 F1·재현율·혼동행렬, 시간순 검증 및 판매자 이탈 조기 경보.

> 위 '향후 제안'은 **실행 완료가 아닙니다.** 별도의 원자료·검증이 필요합니다.

## 6. Streamlit 감성분석 실행 조건과 상태

- [원본 토크나이저](https://github.com/journal-izm/Olist-Data-Analysis/blob/main/model/part7_2_tokenizer.pkl) / [원본 Keras 모델](https://github.com/journal-izm/Olist-Data-Analysis/blob/main/model/part7_2_sentiment_model.keras) (GitHub에 별도 업로드하지 않음)
- 모델 다운로드·크기 확인: `python 다운로드_모델.py` → 프로젝트 `model/` 폴더.
- 포르투갈어 예제: `produto muito bom, chegou antes do prazo`; `MAX_LEN=50`, `padding='post'`, `truncating='post'`.
- Windows Python 3.12 가상환경과 TensorFlow **2.18.1**, Streamlit **1.67.0** 실행 화면은 사용자가 전달해 확인했습니다.
- **실제 개별 모델 예측 확률과 `actual_prediction_results.csv`는 제출받지 못해 미검증**입니다. 브라우저에서 Streamlit이 열리는 것과 모델 추론 성공은 구분합니다.
- Google/GitHub Pages는 **정적 차트 페이지**입니다. GitHub Pages 자체에서 TensorFlow Python 버튼은 실행되지 않습니다.

### Windows 실행 예시 (압축을 푼 실습 폴더)

```powershell
py -3.12 -m venv .venv_tf312
.\.venv_tf312\Scripts\python.exe -m pip install -r requirements_tensorflow.txt
.\.venv_tf312\Scripts\python.exe 다운로드_모델.py
.\.venv_tf312\Scripts\python.exe 실제예측_검증.py
.\.venv_tf312\Scripts\python.exe -m streamlit run streamlit_app.py
```

Notebook/PNG 재생성은 `requirements_노트북.txt` 설치 후 Jupyter에서 과제 폴더의 `.ipynb` 파일을 열어 실행합니다. Olist 차트 4장은 `python generate_charts.py`, Spotify 3장은 `python generate_spotify_charts.py`로 재생성할 수 있습니다.

## 7. 최종 제출 체크

- [x] GitHub 분석 대상 2개 링크 명시 — *원본 K-pop 최신 코드 접근 제한 고지*
- [x] 연습 노트북 **1개**, 코드 셀 11개 저장 실행 기록
- [x] PNG 차트 **7장**, 각 질문·해석·단위·출처
- [x] 데이터 검증과 실제 계산 결과, 분석기법 비교
- [x] Streamlit 감성분석 화면 소스 및 Windows 실행 안내
- [x] GitHub 공개 파일/Pages 배포 기록 확인
- [ ] 원래 K-pop 저장소 최신 소스와 YouTube 데이터 재확보
- [ ] Olist 실제 Keras 모델 추론 확률 CSV와 재현 로그 제출
- [ ] Claude 독립 분석 결과 확보

**검수 원칙:** AI는 초안·코드 보조, 데이터 출처와 숫자 확인 및 게시 최종 승인 책임은 제출자. 상세 재실행 검수는 [실행검증_기록.md](실행검증_기록.md)를 참고합니다. 미검증 사항은 보류하고 결과를 과장하지 않습니다.
