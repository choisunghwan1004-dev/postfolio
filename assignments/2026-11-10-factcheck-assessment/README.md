# 5차 과제 — AI-Powered Python 자동 팩트체킹 (기존 제출답안 보강)

> 자료 기준: 사용자가 제공한 **5차_자동팩트체킹_작성답안_최성환.docx** (3페이지).
> **주의:** 이 폴더의 수치는 첨부 제출답안에 기재된 값입니다. 이 작업에서 원본 CSV를 독립 재실행하지 않았으며, 실제 RAG/Gemini 챗봇 답변도 확보하지 않았습니다.

## 과제 구성
1. **문제 1 — 데이터에서 사실 3개 찾기**: pandas air_quality_long.csv 데이터의 행·열, 결측치, 런던 PM2.5 평균, 사실표 F-1~F-3
2. **문제 2 — 근거 있는 챗봇 답 확인**: 사실표 기반 질문 3개, 인용할 사실 ID, 근거 없는 질문은 '확인 불가'
3. **재현 코드**: [verify_air_facts.py](verify_air_facts.py), 원본 CSV의 실제 데이터로 F-1~F-3 계산
4. **검토용 수치 표**: [fact_table_from_submitted_draft.json](fact_table_from_submitted_draft.json)

## 원본 제출지의 사실표 (아직 독립 재검산 전)
| 사실ID | 정의 | 초안 기재 수치 | 검증 |
|---|---|---:|---|
| F-1 | 2019년 대기질 관측 행 | 5,272건 | 원본 CSV 실행 필요 |
| F-2 | PM2.5 관측 행 | 1,825건 | 원본 CSV 실행 필요 |
| F-3 | London PM2.5 평균 | 13.44 µg/m³ | 원본 CSV 실행 필요 |

원본 제출지에는 London PM2.5 관측 1,648건, 중앙값 9.0 µg/m³도 기재되어 있습니다.

## Windows 11 · VS Code 실행
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install pandas
.\.venv\Scripts\python.exe verify_air_facts.py --csv "C:\\실제경로\\air_quality_long_original.csv"
```
명령에 나오는 경로는 사용자의 실제 CSV 위치로 바꾸세요.
정상 실행되면 `results/facts.json`에 로컬 계산 결과를 저장합니다.
원본 자료가 없으면 **파일 없음 오류**로 종료하며 임의 가상 결과를 만들지 않습니다.

## 챗봇의 검증용 지시문
> 제공한 F-1~F-3 사실표에서 근거를 찾을 때만 답하세요. 숫자 뒤에는 [F-1] 같은 사실 ID를 표시하세요. 사실표에 없는 질문은 '확인 불가'라고 답하세요. 외부 정보를 만들어내지 마세요.

| 질문 | 예상 답변 | 근거 |
|---|---|---|
| 원본의 관측 행 수는? | 총 5,272건입니다. [F-1] | F-1 |
| 런던 PM2.5 관측 평균은? | 13.44µg/m³입니다. [F-3] | F-3 |
| 2026년 11월 서울 PM2.5 평균은? | 확인 불가 | 자료 범위 외 |

위 답변은 **사람이 작성한 검증용 예상 답안**으로, 실제 챗봇 로그가 아닙니다.

## 제출 직전 확인
- [ ] 실제 `air_quality_long_original.csv` 확보·권리 확인
- [ ] Python 계산 결과와 F-1~F-3 숫자 재대조
- [ ] VS Code/Jupyter **코드+결과 한 화면** 촬영
- [ ] 실제 RAG 챗봇 또는 Gemini 노트북에서 3문항 질의
- [ ] 챗봇 질문/답변 화면 촬영, 근거 ID 확인
- [ ] 제출지에 실제 캡처 삽입, 최종 확인자 승인

## 출처
- pandas 교육용 대기질 원본: https://github.com/pandas-dev/pandas/blob/main/doc/data/air_quality_long.csv
- 기존 작성본: 사용자가 제공한 Word 제출지. 업로드 원본은 이 공개 저장소에 게시하지 않았습니다.
- 공개 GitHub에는 **코드·설명·검증용 예시만** 등록합니다. 실제 미공개 원본 데이터 및 API 키는 올리지 않습니다.
