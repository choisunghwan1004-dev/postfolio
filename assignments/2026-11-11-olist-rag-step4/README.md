# MBC 데이터저널리즘 STEP4 — Olist LangChain RAG 챗봇 과제

**제출 기준일:** 2026-11-11 · **범위:** SHAI 제외, 독립 수업 과제

## 과제 목표
수업 Olist 자료로 사실(F) / 모델 설명(M) / 수업용 가상 규정(R) 책장을 만들고, LangChain으로 질문→근거 검색→답변→출처 ID 후검증 흐름을 구현한다. 기존 수업 노트북과 Olist 대시보드 UI는 원본을 보존한다.

## 관련 파일
- [정식 과제 보고서](과제보고서.md)
- [실제 원본 근거 A/B/C 검증 기록](ABC_검증결과_요약.md)
- [수업 LangChain 연결 코드 V1.2](../../chatbots-non-shai/langchain-rag-v1-2/)
- [수업 원본 기반 공개용 소량 샘플 V1.3](../../chatbots-non-shai/olist-rag-real-sample-v1-3/)
- [수업 원본 20셀 Jupyter 노트북 보존본](../../chatbots-non-shai/11_olist_rag_chatbot_source.ipynb)
- [노션 과제 관리](https://app.notion.com/p/41428cb9cfd78163b3a2fc7700122d0f)
- [수업 통합일지](https://docs.google.com/document/d/1vSeKZW3o3qWyyTn_n1IAkFmWvDxNO4j2cfKaMQaIZtk/edit)

## 검증 상태
**Python 오프라인 단위/회귀 테스트 21/21 PASS**, 실제 수업 자료 F 35건 / M 8항목 / R 17조 확인, 5개 질문×3채널=15개 규칙형 근거 조회 사례 검증.

**미검증:** 실제 OpenAI 임베딩·LLM 호출, LangChain 유사도 검색 결과의 실제 적합성, Streamlit 브라우저·공개 배포, 원천 Olist 주문 CSV 재계산, 사용자 Windows 전체 화면 캡처.

> 과제 표의 답변은 교육용 문서에서 직접 조회한 오프라인 예상/검증 결과이며, 실제 API 챗봇 답변으로 가장하지 않습니다. 규정집은 Olist 실제 정책이 아닌 **교육용 가상 규정**입니다.

## VS Code에서 재실행
1. V1.3의 개인 실습 ZIP(원본 데이터 포함)을 받아 로컬에서 압축 해제.
2. Python 3.12 권장 가상환경과 requirements 설치.
3. `python -m unittest discover -s tests -v`와 `python sample_offline.py`.
4. API키를 안전하게 별도 입력한 뒤 `python -m streamlit run app.py`로 실제 RAG 테스트. 이 단계는 **본 제출 패키지의 실제 검증 내역에 포함되지 않음**.

## 개인 제출 패키지와 공개 범위
저작권을 확인하지 않은 수업 PDF와 대량 원본은 공개 GitHub에 재배포하지 않음. 공개용 작은 예시, 로직, 테스트·검수 상태만 등록. 개인 제출본 ZIP에는 실제 수업 파일이 포함될 수 있으며, 교내 실습 용도로만 사용.

**GitHub 제출 주소:** https://github.com/choisunghwan1004-dev/postfolio/tree/main/assignments/2026-11-11-olist-rag-step4
