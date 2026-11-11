# Olist STEP4 · LangChain RAG + 근거 검증 (독립 과제)

2026-11-11 통합수업일지 기준: STEP4_RAG_Chatbot, `11_olist_rag_chatbot.ipynb`, `utils/rag.py`, `qa.py`, `olist_facts.csv`, `olist_model_guide.md`, `olist_seller_policy.pdf`.
원본 수업 노트북과 기존 Olist Streamlit 대시보드는 **수정하지 않았습니다**. SHAI는 별도 시스템으로 이 패키지에 포함되지 않습니다.

## 동작
- A: 사실표 Fxx, B: Fxx+모델 Mxx, C: Fxx+Mxx+가상 규정 Rxx
- LangChain `Document` → OpenAI Embeddings → `InMemoryVectorStore` → 관련 조각 k개 검색 → `ChatPromptTemplate` → `ChatOpenAI` → `StrOutputParser` → **근거 ID 후검증**.
- 찾지 않은 ID, 누락/형식이 틀린 ID가 인용되면 답변 자체를 **차단**. 자료 밖 질문은 확인 불가.
- 주의: 인용된 ID가 실제로 검색되었다는 것은 **그 문장이 사실임을 의미하지 않습니다**. 원본 숫자 재계산과 기자의 확인이 필수입니다.

## 실행 · Windows 11 VS Code
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m streamlit run app.py
```
`data/` 폴더에 수업용 `olist_facts.csv`, `olist_model_guide.md`, `olist_seller_policy.pdf`를 넣습니다. UI에 API 키를 직접 입력합니다. Streamlit 캐시에 키가 메모리로 전달되므로 공동 PC에서 세션 종료 후 프로세스도 종료하세요.

## Colab과 VS Code 차이
원본 Colab 노트북의 `from google.colab import drive,userdata`, `/content/drive/MyDrive/...` 코드를 이 패키지에서 사용하지 않습니다. `pathlib.Path` 로컬 `data/` 경로를 사용합니다.

## LangChain 있음/없음 비교
- 기존 `chatbots-non-shai/evidence_qa_demo.py`는 규칙기반 로컬 예제. **의미 검색/LLM 없음**.
- 이 패키지 `utils/rag.py`는 LangChain의 진짜 `Document`, 벡터스토어, 검색, 채팅 모델을 연결하는 코드. **실제 OpenAI API 호출은 별도 키·비용이 필요**.
- `tests/test_rag.py`는 저장소와 모델을 테스트 대역으로 바꿔 가짜 ID 차단 등을 검증. **실제 LangChain 임베딩 호출 테스트 아님**.

## 수업 제출 체크
- [ ] GitHub README 및 실제 원본 자료 출처
- [ ] VS Code 혹은 Colab 실행 화면
- [ ] 질문 A/B/C 비교 스크린샷
- [ ] 근거 ID와 원본 사실표 대조
- [ ] 가짜 ID 차단 / 모르는 질문 확인 불가
- [ ] Streamlit URL 및 작동 검증

### 확인된 수업 자료
- [통합수업일지](https://docs.google.com/document/d/1vSeKZW3o3qWyyTn_n1IAkFmWvDxNO4j2cfKaMQaIZtk/edit)
- [Olist STEP4 강의 원본 노트북](https://drive.google.com/file/d/1yYTHQBjdefncsxsnngN7Q3a8CaOqNh1x/view)
- [Olist RAG 교재](https://drive.google.com/file/d/1QIfuXthNpuY0IQBdj3zn_yuPmCmJTjCE/view)
- [수업용 사실표·모델·PDF 폴더](https://drive.google.com/drive/folders/1q60CTVdW63L4RPMeTXqzUyV8IVpsrELP)

**검증 상태:** 오프라인 단위 테스트만 완료; 실제 LangChain 패키지 설치/실사용 API 호출/Streamlit 브라우저 테스트는 미검증입니다.

## 2026-11-11 · 수업 ③ 프롬프트/④ 근거 검증 추가
- 사용자 제공 코드의 `PROMPT` 구조를 `build_prompt()`로 분리해 기존 Streamlit UI의 재사용 구조를 유지합니다.
- `ask(question, channel, api_key, k=4, folder=None, model='gpt-5.4-mini')`를 보조 API로 추가했습니다.
- 원래 스크린샷에서 `re.findall(r"**\[**([FMR]\d{2})**\]**", answer)`처럼 굵게 표시된 문자는 **정규식의 일부가 아닙니다**. 올바른 패턴은 `r"\[([FMR]\d{2})\]"`입니다.
- 거짓 ID는 `fake_ids`에 남기되, 화면에 보여줄 `answer`는 `제공된 자료로는 확인할 수 없습니다.`로 차단합니다. 근거 없는 답변도 동일하게 차단합니다.
- 추가 테스트: 거짓 ID 기록, 정상 답변, `ask()` 진입점의 모의 검색/모의 모델 검증.
- 사용자 참고 교재 『랭체인으로 만드는 RAG 시스템』의 3장 프롬프트·5장 LCEL·6장 Streamlit 흐름을 반영했습니다.
- 실제 PDF 원본은 출처와 저작권 확인을 위해 GitHub에 업로드하지 않았습니다.
