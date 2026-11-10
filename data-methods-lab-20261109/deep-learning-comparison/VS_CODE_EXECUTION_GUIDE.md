# VS Code · Windows 11 로컬 실행 안내

> 교육자료 「VS Code로 파이썬 노트북 실행하기 (설치 안내)」 5쪽 검토 후 학습 추가3 환경에 맞게 정리.
> 컴퓨터에 Python 3.12가 이미 설치되어 있다고 단정하지 않습니다.

## 5단계
1. VS Code 확장 설치: Microsoft **Python**, **Jupyter**
2. 프로젝트 폴더 열기. 해당 노트북의 CSV·상대경로가 올바른지 확인
3. 해당 폴더에서 가상환경 생성
4. 노트북의 **Select Kernel → Python Environments → .venv** 선택, 셀별 ▶ 실행
5. GPT API를 실제로 사용하는 실습만 `.env`와 `python-dotenv`를 사용. **학습 비교와 데이터 정제는 API 키 불필요**

### 학습 비교 폴더에서
```powershell
py -3.12 --version
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe train_compare.py
```
이 비교 코드는 현재 `.py`로 작성됨. 노트북(`.ipynb`) 실행을 원하는 경우 `ipykernel` 설치 후 별도 노트북 작성 필요.
VS Code GPU 실습은 교재의 특정 RTX 50/CUDA 12.8 장비 전용 지침을 모든 PC에 그대로 적용하면 안 됨. GPU가 없어도 이 비교 과제는 **CPU 기본**.

### 데이터 정제 폴더에서
```powershell
cd dataset_pipeline
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe prepare_dataset.py --input sample_press.csv --output-dir output
```
`sample_press.csv`는 사용자가 마련한 허용된 원본 파일 경로로 바꾸세요. 제공하지 않은 CSV가 있다고 가정하지 않습니다.

### 노트북 실행이 필요할 때만
```powershell
.\.venv\Scripts\python.exe -m pip install ipykernel
```
VS Code Python/Jupyter 확장 설치 후 노트북에서 해당 .venv 커널 선택.

## 문제 해결 표
| 증상 | 확인/대응 |
|---|---|
| `ModuleNotFoundError` | 현재 .venv 커널·설치 경로 확인 |
| `FileNotFoundError` | VS Code 열린 폴더 및 상대 경로 점검 |
| `google.colab` 모듈 오류 | VS Code용 코드인지 확인. Colab 전용 마운트 제거 |
| 한글이 □로 나옴 | Windows `Malgun Gothic` 설정 확인 |
| `py` 명령 없음 | `python --version`으로 설치 경로 확인 |
| 커널 목록에 .venv 없음 | VS Code 창 새로고침, ipykernel 설치 |
| `401` API 오류 | 필요한 실습에서만 .env를 확인하고 커널 재시작 |
| `torch.cuda.is_available()` False | CPU 환경이면 정상. GPU 장치·드라이버·전용 휠은 별도 확인 |

## 보안·배포
- `.env`, `.venv`, `output/`, `press_clean.csv`, `review_queue.csv`, `lead_approved.jsonl`은 GitHub 업로드 금지
- 직접 수집한 원문은 사이트별 재사용/AI 학습 권리 확인. 승인되지 않은 데이터는 로컬에서만 다룸
- 학습 결과가 없으면 공개 웹은 '미실행·미검증' 표시

## 자료와의 차이점
교재는 강의장 PC에 Python 3.12/RTX 5070이 있다고 설명하지만, 사용자 PC에도 설치돼 있다고 가정하지 않습니다. 실행 환경과 패키지 버전은 실제 장치에서 검증해야 합니다.
