# MBC AI 데이터저널리즘 — K-pop × Olist GitHub 분석 과제 제출본

제출 기준일: 2026-11-09. 수업 과제는 **노트북 1개 + 차트 PNG 3장 이상 + 각 차트 질문과 해석 1문장 + GitHub 두 개 분석 + Olist Streamlit 감성분석 화면**입니다.

## 먼저 제출할 파일

| 요구사항 | 파일 | 결과 |
|---|---|---|
| 연습 노트북 1개 | `KPOP_Olist_데이터분석_실습.ipynb` | 7개 코드 셀 실행 결과 저장 · 차트 4개 삽입 |
| 차트 PNG 3장 이상 | `charts/` 안의 PNG 4개 | 완료 · 제목/단위/출처/질문/한 줄 결론 포함 |
| 차트 생성 코드 | `generate_charts.py` | Olist 출처 기반 집계표로 재현 |
| 분석 수치와 출처 | `data/olist_verified_facts.csv` | Olist 원본 사실표 F08·F14·F23~F25·F27에서 재구성 |
| 분석기법과 비교보고서 | `분석보고서_제출용.md` | Log Scale / log1p / StandardScaler 구분, 추가 분석기법 |
| Streamlit 화면 | `streamlit_app.py` | Keras 모델/토크나이저 로딩, 리뷰 입력과 예측 버튼, 차트 전시, CSV 다운로드 |
| 설치/검증 방법 | `00_환경점검.bat` ~ `03_감성분석_화면.bat` | Windows Python 3.12 / TensorFlow 2.18.1 |

## 차트 4장 · 질문 → 결과

1. **배송과 리뷰 (F14)** — 질문: 늦게 도착하면 리뷰는 어떻게 다른가? → 제때 4.30점, 지연 2.57점, 차이 **1.73점**.
2. **감성분석 모델 비교 (F23~F25)** — 질문: 딥러닝이 항상 더 정확한가? → Bigram 머신러닝 **92.6%**, Embedding 평균 모델 **92.4%**, **0.2%p** 차이.
3. **지역별 주문 비중 (F08)** — 질문: 주문은 어디에 집중됐나? → SP 42.0%, RJ 12.8%, MG 11.8%, 상위 3개 주 **66.6%**.
4. **판매자 유형 (F27)** — 질문: 가장 큰 집단은? → 신규 성장 **947명**, 핵심 우량 **876명**, 휴면 461명, 저평점 위험 218명.

> 위 수치는 **Olist GitHub의 집계 사실표**를 시각화한 것이며, 이 과제에서 전체 원본 주문 데이터를 새로 계산하거나 모델을 재학습했다는 뜻은 아닙니다. 차트의 상관관계는 인과관계 증명이 아닙니다.

## 과제 대상 GitHub 주소

- K-pop DATA LAB: https://github.com/dominickim77-ui/mbc-kpop-data  
  이번 확인에서는 API 404로 원본 최신 CSV/코드에 접근 불가. **실측 K-pop 그래프 생성은 보류**, 노트북은 실제 CSV가 제공되면 연결되는 구조.
- Olist Data Analysis: https://github.com/journal-izm/Olist-Data-Analysis  
  실제 열람: `README.md`, `rag/olist_facts.csv`, `STEP2_Model_Serving/01_sentiment_demo_gradio.ipynb`, 모델 목록, 기존 Streamlit 관련 코드.
- 딥러닝 모델: https://github.com/journal-izm/Olist-Data-Analysis/tree/main/model
- 과제 제출 Drive 폴더: https://drive.google.com/drive/folders/1qCloI4HiTNBCypiVgafhlMQNpVIimIx8

**참고:** 두 저장소는 과제 분석 대상의 **원본 GitHub 주소**이며, 이 제출 ZIP 자체를 GitHub에 push한 링크가 아닙니다. Claude의 독립 코드 분석 결과 역시 받지 않았으므로 수행했다고 적지 않았습니다.

## 발표 핵심: 왜 로그축(Logarithmic Scale)인가?

- **로그축**: 눈금 간격만 바꿔서 크기 차이가 매우 큰 숫자를 보기 쉽게 표현. 원본 값 자체는 수정하지 않음.
- **`np.log1p(x)`**: 양수/0으로 된 관측값을 `log(1+x)`로 실제 변환. 치우친 분포를 완화할 수 있음.
- **`StandardScaler`**: 머신러닝 입력값의 평균 0·표준편차 1 표준화. 로그축과 **목적이 다름**.
- 머신러닝에서는 `log1p` 후 `StandardScaler`를 연속 적용할 수 있으며, 학습 데이터만으로 변환 규칙을 학습하여 누수 방지.
- **Spotify 주간 스트리밍 수치와 YouTube 누적 조회수는 시점/기간이 다르므로 직접 인기 비교 불가.**

## Windows에서 감성분석 화면 실행 (선택 시연)

이미 TensorFlow/Streamlit이 설치된 컴퓨터에서는 **이 제출 폴더가 기존 폴더와 다른 위치**이므로, 새 `model/`에 모델을 내려받거나 검증된 두 파일을 복사해야 합니다. 기존 가상환경은 ZIP에 넣지 않았습니다.

1. ZIP 전체 압축 풀기 → `00_환경점검.bat` (설치 상태 확인).
2. `01_설치_모델다운로드.bat` (필요한 가상환경과 원본 모델 설치/다운로드). **설치에 인터넷 필요, 수백 MB**.
3. `02_실제예측_검증.bat` (실제 모델 추론이 되면 `actual_prediction_results.csv` 생성).
4. `03_감성분석_화면.bat` → 브라우저 `http://127.0.0.1:8501`.
5. 포르투갈어 예제 `produto muito bom, chegou antes do prazo` 입력 → **감성 분석 실행** → 확률과 판정 확인.

**실행 검증 근거:** 사용자가 제공한 Windows 화면에서 Python 3.12, TensorFlow **2.18.1**, Streamlit **1.67.0** 실행을 확인했으며 이후 사용자가 "처리됐다"고 전달함. 다만 현재 제출 ZIP에는 **실제 모델 추론 확률값 CSV가 없고**, 모델 추론 성공 로그 원본도 전달되지 않아 **예측 정확도·실제 출력값을 검증 완료로 기재하지 않음**.

### 기사용 차트 검수

모든 차트는 막대축 0 시작, 제목, 수치 단위, 관련 사실ID를 포함합니다. 기간·분모·구분을 정확히 읽고, 인과관계를 추정하지 않습니다.

**제출자 점검:** GitHub 원본 링크 확인, `.ipynb` 1개, `.png` 4개, 각 질문과 해석, 개인정보·API 키 미포함. ZIP 안에 `.venv` 및 `.pkl`/`.keras` 원본 바이너리 파일은 포함하지 않음.
