# 독립 챗봇 자료실 — SHAI 제외

> 범위: AI 데이터저널리스트 수업용 **Olist STEP4 RAG Q&A**, **5차 근거 기반 팩트체킹 챗봇**, **Olist 분석 화면과의 연동 참고**.
> **SHAI 통합 AI 챗봇, Mistral/Claude/Gemini/GPT 통합 엔진, SHAI 소스·API 키·설정은 포함하지 않습니다.**

## 자료 및 진행 상태 (2026-11-10)

| 구분 | 실제 확인된 자료 | 등록/검증 |
|---|---|---|
| Olist RAG 강의 노트북 | Google Drive `STEP4_RAG_Chatbot/11_olist_rag_chatbot.ipynb` | 원본 확인, Drive 링크로 연결. LangChain API 실행은 미검증 |
| 강의 교재 | 「Olist 분석 Q&A 챗봇 (RAG)」 PDF | 교재 내용을 토대로 설명, PDF 파일 자체는 복제하지 않음 |
| Olist 범위별 검색 | A 사실표, B 사실표+모델 설명서, C +규정집 | [SOURCE_INDEX.md](SOURCE_INDEX.md) |
| 출처 ID 점검 | 사실 F / 모델 M / 규정 R, 검색하지 않은 ID 거부 | [evidence_qa_demo.py](evidence_qa_demo.py) **로컬 규칙형 검증 예제** |
| 5차 자동 팩트체킹 과제 | 기존 GitHub 실제 등록 코드·사실표 | [별도 과제 폴더](../assignments/2026-11-10-factcheck-assessment/) |
| Olist 분석+모델 차트 | 기존 포트폴리오 자료 | [Olist 포트폴리오](../mbc-kpop-olist-20261109/) |

## RAG 수업의 목적과 안전장치
강의는 질문이 오면 사실표/모델 설명서/규정에서 관련 조각을 검색하고, 각 문장에 해당 근거 ID를 붙여 답하도록 지도합니다.
검색된 ID 집합과 답에 인용한 ID 집합을 비교하여 **검색하지 않은 ID는 답 근거로 인정하지 않습니다**.
원래 강의 노트북은 `langchain-core`, `langchain-openai`, `langchain-community`, `pypdf` 등을 사용합니다.
해당 라이브러리와 OpenAI 임베딩·LLM 호출을 **이 저장소에서 실제 실행해 검증하지는 않았습니다**.

### A/B/C 책장
- A: 분석 사실표 (`olist_facts.csv`, 교재상 35건)
- B: A + 모델 설명서 (`olist_model_guide.md`, 교재상 8항목)
- C: B + 수업용 판매자 규정집 PDF (`olist_seller_policy.pdf`, 교재상 17조)
- 수업용 규정집은 **실제 Olist 정책이 아니라 교육용 가상 문서**입니다.

## 실행 가능한 최소 검증 코드 (실제 RAG 아님)
```powershell
py -3.12 evidence_qa_demo.py
py -3.12 -m unittest test_evidence_qa_demo.py -v
```
이 예제는 **미리 등록된 교육용 사실을 규칙으로 찾아 답하는 로컬 기준선**입니다. 외부 API·임베딩·벡터 검색을 호출하는 정식 RAG라고 주장하지 않습니다.
실제 수업 노트북과 동일한 질문/근거/거부 규칙을 확인하기 위한 재현 코드입니다.

## 유지·공개 정책
- 기존 Olist 포트폴리오, 자동 팩트체킹 과제, Streamlit UI는 **수정하지 않음**
- GitHub에는 공개 가능한 설명·검수표·샘플 코드를 게시
- 실제 대용량 데이터, 개인/고객 정보, API 키, `.env`, `secrets.toml`, 모델 가중치, 연결된 계정 토큰은 게시하지 않음
- 실제 RAG 앱 동작과 배포를 검증하기 전까지 상태는 **자료 정리 및 기준선 코드 등록**

## 연동 문서
- [자료 출처·보류 항목](SOURCE_INDEX.md)
- [검증 절차](VALIDATION_CHECKLIST.md)
- [5차 팩트체킹 Python 코드](../assignments/2026-11-10-factcheck-assessment/verify_air_facts.py)
