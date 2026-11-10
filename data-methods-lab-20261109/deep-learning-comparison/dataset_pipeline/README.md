# 크롤링 → 정제 → JSONL 학습 데이터 준비 (학습 추가4)

> **현재 상태: 코드/설명 등록, 실제 외부 사이트 크롤링·유료 API 생성·100쌍 검증 미실행.**
> 강의자료 「크롤링으로 학습 데이터 만들기」(22쪽)의 4단계(수집→정제→리드 초안→JSONL)를 따릅니다.
> 기존 통계 모델 비교(가상 분류 데이터)와 별도 파이프라인이며, 크롤링된 보도자료를 바로 수치 예측 학습에 사용하지 않습니다.

## 순서
1. 공공 CSV·Open API가 있는지 먼저 확인. 없을 때만 크롤링 검토
2. 대상 사이트 robots.txt, 이용약관, 저작권·공공누리 유형, 개인정보, AI 학습 허용 범위를 **담당자가 직접 확인해 기록**
3. 작은 표본으로 정적 HTML/선택자/상태 코드/요청 간격 점검. 로그인·403/429 차단은 우회하지 않음
4. 수집 원본 CSV는 **로컬에만 저장**. 중복·공백·빈 본문·길이(200~2500자) 정제
5. 승인된 본문에서만 기사 리드 초안을 생성. 숫자·인용·원인 조작 금지
6. 사람이 원문을 대조해 승인한 쌍만 `instruction`/`input`/`output` JSONL로 확정
7. 중복·출처별 분리, 검수 표, 개인정보/저작권 점검 후 훈련·평가 분리

## 로컬 실행 (VS Code / PowerShell)
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe prepare_dataset.py --input sample_press.csv --output-dir output
```
위 `sample_press.csv`는 **직접 작성한 예시 또는 사용 승인을 받은 CSV**를 지정하세요.
필수 열: `제목`, `본문`. 출력은 `press_clean.csv`, `review_queue.csv`, `audit.json`입니다.
첫 실행에서 검수용 대기열의 `승인` 값은 비어 있습니다. `리드`를 사람이 작성·검토하고 `승인`에 `Y`를 입력한 다음:
```powershell
.\.venv\Scripts\python.exe export_approved.py --input output/review_queue.csv --output output/lead_approved.jsonl
```
승인된 데이터가 없으면 빈 JSONL을 만들지 않고 오류로 안내합니다.

## 실제 크롤링을 추가하려면
강의의 `requests + BeautifulSoup`, `select`, `urljoin`, `time.sleep(1)` 구조를 참조하되 **먼저 특정 사이트의 수집 권한과 실제 HTML 선택자를 확인**하세요. 이 폴더에는 확인되지 않은 보도자료 사이트 주소나 작동한다고 주장하는 임의 선택자를 넣지 않았습니다. 응답 403·429, robots 차단은 수집 중단으로 처리합니다.

## 공개 정책
- GitHub: 코드, 설명서, 누락·중복 건수 집계, 익명화된 가상 예시만
- GitHub에 업로드 금지: 원문 수집 CSV, 기사 본문 쌍, 미승인 리드, API 키, 개인 정보
- 실제 데이터 100쌍 도달 여부, 날짜, 원출처, 검수자, 사용허락, 분할 기준은 검증 후 기록
- AI 초안은 '검수 전'이며 정답 데이터로 간주하지 않음
- 모델 학습 전 복제·유사 텍스트 유출을 방지하는 중복 점검과 소스별 train/test 분리를 추가 검증할 것

## 강의 근거
- 4쪽: 파일 → API → 크롤링 → 정보공개청구
- 10쪽: robots/약관/공공누리/서버예절/원문 비공개
- 16~18쪽: 수집/오류/정제
- 19~21쪽: instruction-input-output, 사람이 검수한 답, JSONL
