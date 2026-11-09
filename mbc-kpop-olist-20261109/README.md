# MBC 데이터 분석 과제 포트폴리오 — K-pop × Olist (2026-11-09)

이 폴더는 기존 포트폴리오와 분리한 **과제 전용 정적 웹페이지**입니다.

## 웹에서 바로 보기

- GitHub 파일: [index.html](./index.html)
- GitHub Pages 주소 (Pages 설정 시): https://choisunghwan1004-dev.github.io/postfolio/mbc-kpop-olist-20261109/
- [과제 제출용 ZIP 내려받기](https://drive.google.com/file/d/1gORcec-W3NF6R7m894lCxQ_TqMIr97RB/view?usp=drivesdk)
- [MBC 과제 제출 폴더](https://drive.google.com/drive/folders/1qCloI4HiTNBCypiVgafhlMQNpVIimIx8)

**주의:** GitHub에 HTML 코드가 업로드된 것과 GitHub Pages 실제 공개 배포는 서로 다릅니다. 웹주소가 404라면 저장소 **Settings → Pages → Source: Deploy from a branch → main / (root) → Save**로 Pages 게시를 켜야 합니다. 이 저장소에는 이미 루트 `index.html`이 있어 그 설정에서 기존 포트폴리오도 함께 게시됩니다. 기존 루트 웹페이지는 수정하지 않았습니다.

## 차트 4개와 근거

| 차트 | 질문 | 결과 | 원출처 |
|---|---|---|---|
| 배송 / 리뷰 | 지연 배송의 리뷰는 얼마나 다른가? | 제때 4.30점, 지연 2.57점 | F14 |
| 모델 정확도 | 딥러닝은 항상 더 정확한가? | Bigram 92.6%, 딥러닝 92.4% | F23~F25 |
| 지역별 주문 | 주문이 집중된 지역은? | SP 42.0%, RJ 12.8%, MG 11.8% | F08 |
| 판매자 유형 | 가장 큰 판매자 유형은? | 신규 성장 947명 | F27 |

원 수치: [Olist 분석 사실표](https://github.com/journal-izm/Olist-Data-Analysis/blob/main/rag/olist_facts.csv)

## 분석 프로젝트

- [K-pop DATA LAB](https://github.com/dominickim77-ui/mbc-kpop-data) — 2026-11-09 재접속 시 API 404: 최신 데이터 재검증 불가. 웹페이지에는 실측 K-pop 통계 없음.
- [Olist Data Analysis](https://github.com/journal-izm/Olist-Data-Analysis) — README, F01~F35 사실표, 감성분석 Gradio 노트북과 모델 파일 목록을 검토.
- [Olist 딥러닝 모델 예제](https://github.com/journal-izm/Olist-Data-Analysis/blob/main/STEP2_Model_Serving/01_sentiment_demo_gradio.ipynb) — Keras 감성분석/Tokenizer, 입력 길이 50, post padding 및 truncating.

## 포함 / 미포함

- **이 GitHub 폴더:** 데이터저널리즘 요약 HTML, 4개 그래프(HTML로 재구성), 로그축 vs 표준화 비교, 검증·출처 표시.
- **Drive ZIP:** 재현 가능한 연습 노트북 `.ipynb` 1개, 원본 제출 차트 `.png` 4개, Streamlit 감성분석 소스, 모델 다운로더, Windows 실행 파일, 보고서·검수 기록.
- **공개 저장소에 포함하지 않음:** `.venv`, `.pkl`, `.keras`, 개인 비밀키, 개인 PC 경로. 실제 모델 추론 확률값 CSV는 미제출.

**표현 주의:** 차트는 Olist 저장소의 기존 집계 사실을 새로 시각화한 것이며, 주문 전체를 직접 재계산하거나 통계적 인과관계를 입증한 결과가 아닙니다. 웹페이지는 정적 프레젠테이션이며 TensorFlow 추론을 실행하지 않습니다.

---
원본 포트폴리오의 UI·기능·파일은 수정하지 않고 `mbc-kpop-olist-20261109/` 새 하위 폴더만 추가했습니다.
