# Olist RAG V1.3 — 공개 교육용 최소 샘플 (SHAI 미포함)

**실제 원본은 사용자의 수업용 Google Drive 자료**에서 확보했습니다.
사실표 35행, 모델 설명서 8항목, 교육용 가상 규정 17조를 사용한 비공개 패키지 검증은
[개인 백업 ZIP](https://drive.google.com/file/d/1d5Rw20Xt6YgEw8hNIJSelx0R3qY6EDIw/view)과 [노션 관리 문서](https://app.notion.com/p/41428cb9cfd78163b3a2fc7700122d0f)에 기록합니다.

이 공개 저장소의 예시는 **수업 숫자를 소량 요약·재작성한 교육용 사례**만 포함합니다. 자료 전체의 재배포 권리는 확인하지 않았으므로 원본 전체 CSV/MD/PDF는 업로드하지 않습니다.
- F14: 늦게 도착한 주문 평균 리뷰 2.57점 (원본 05_eda 분석 사실표에 기재)
- F07: 2회 이상 구매 고객 3.0% (동일)
- M09: 이탈 모델 입력 14개 (교재 모델 설명서)
- R06: 3일 이상 배송 지연 보상 (가상 규정집; **실제 Olist 정책 아님**)

## 실행 방법 — API 키 불필요
```powershell
py -3 demo.py
py -3 -m unittest discover -s tests -v
```
이 코드는 **지정된 근거 ID를 직접 조회**하는 샘플로, 진짜 벡터 검색·LangChain·OpenAI API는 실행하지 않습니다. 실제 LangChain 연결 코드와 화면은 [V1.2 분리 소스](../langchain-rag-v1-2/)에 있습니다.

## 본 수업자료 전체 검증 결과
- 사실표/모델/가상 규정: 35 / 8 / 17 구조 확인
- A/B/C × 5가지 질문: 15개 오프라인 비교
- 전체 개발 패키지의 단위 테스트: 21/21 PASS
- 실제 OpenAI embeddings/LLM 호출: **미실행**
- 원본 Olist 주문 CSV로 분석 숫자 재계산: **미실행**

## 출처
- [Olist 사실표 (Google Drive)](https://drive.google.com/file/d/1eJn5g3qkcsFKsp1vYOVcHgLA6wRVNO0P/view)
- [Olist 모델 설명서 (Google Drive)](https://drive.google.com/file/d/1tckTU6OiLvQJG8TncUFdikhg52w04AXr/view)
- [실습용 가상 규정 PDF (Google Drive)](https://drive.google.com/file/d/1kW72Ku5vEV0gOqLpxs_rpmoCHa2Olyrz/view)
- [수업 노트북](https://drive.google.com/file/d/1yYTHQBjdefncsxsnngN7Q3a8CaOqNh1x/view)

수업 자료의 숫자를 인용했다고 해서 실제 사업 통계나 회사 정책으로 해석해서는 안 됩니다.
