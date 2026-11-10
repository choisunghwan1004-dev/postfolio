# VS Code 수업 데이터저널리즘 과제 — 원본 코드 검토

원본: https://github.com/journal-izm/ai-datajournalism-labs
교재: VS Code로 파이썬 노트북 실행하기 (설치 안내), 빅데이터와 저널리즘 · 기사용 차트 문법_Jupyter.
수업코드_데이터저널리즘.zip은 현재 직접 확보하지 못하여 GitHub 공개 원본 노트북 세 개를 기준으로 수정본을 준비했습니다.

## 수정한 파일
- visualization_basics.ipynb: 기존 코드 유지, VS Code 재실행·커널 안내 추가.
- 1_bigdata_news_vs_air.ipynb: 분석/차트 셀 유지. CSV encoding 확인, 빅카인즈 엑셀 파일 유무와 작업 폴더 확인 코드 추가.
- 2_chart_grammar.ipynb: 차트 원본 유지, 네트워크/재실행 안내만 추가.

## 오류 유형별 판정
| 증상 | 판단 | 대응 |
|---|---|---|
| UnicodeDecodeError | 인코딩 불일치 가능 | 파일의 실제 인코딩 확인, cp949/utf-8-sig/utf-8 등 확인; 단순 재실행만으로 해결하지 않음 |
| 빈 glob 목록 / pd.concat([]) | 데이터 파일 부재 | 빅카인즈 XLSX 파일의 경로와 이름 확인 |
| FileNotFoundError | CSV 파일 또는 경로 문제 | data_air_2022.csv 파일 확인 |
| ModuleNotFoundError | 커널/설치 환경 문제 | VS Code .venv 선택 및 requirements 설치 |
| 커널 재시작 직후 NameError | 실행 상태 초기화 | 처음 셀부터 Run All |
| sns.load_dataset 일시 연결 실패 | 원격 네트워크 문제 가능 | 연결 확인 뒤 제한적으로 재실행, 반복되면 원인 조사 |
| HTTP 429 | 서버 요청 제한 | 무한 재시도 금지, 정책에 맞춰 대기 |

## 제출 증빙과 검증 상태
- 원본 GitHub 코드 열람 및 보존형 수정본 GitHub 등록: 완료.
- 사용자 PC의 VS Code 전체 창 스크린샷: 미확보. 실제 실행한 화면을 캡처해야 함.
- 수업 실측 data_air_2022.csv 와 빅카인즈 기사 엑셀: 미확보. 따라서 실측 결과 실행 완료 주장은 하지 않음.
- 별도로 만든 가상 미세먼지 실행 예제와 이 수업 원본 코드 수정본은 서로 구분.
- 제출 시 VS Code 전체 화면, 실행 결과, 오류 메시지(실제 발생 시), 전후 코드, 수정 이유, 출처, 실행 일시를 기록.

## Windows VS Code 실행
1. 원본 저장소를 내려받고 Python 3.12 가상환경(.venv)을 생성.
2. requirements.txt 패키지 설치, VS Code Python/Jupyter 확장 설치.
3. 노트북에서 Select Kernel -> .venv, 모든 셀 순서대로 Run All.
4. 미세먼지 노트북은 수업 데이터 CSV와 빅카인즈 엑셀이 해당 노트북의 작업 폴더에 있어야 실행 가능.
5. API 키나 개인정보가 화면에 보이지 않도록 하고 VS Code 전체 화면 캡처.

## 원본 보존 원칙
교사의 GitHub 저장소는 읽기만 하며 수정하지 않았습니다. 수정본은 개인 postfolio 저장소에 별도 저장했습니다.