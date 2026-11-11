# VS Code에서 수업코드 불러오기 (2026-11-11)

> **원본 소스 보존 폴더:** [ai-datajournalism-labs](./ai-datajournalism-labs/)
> **원본 저장소:** https://github.com/journal-izm/ai-datajournalism-labs
> **복사 기준:** GitHub 원본 main 트리 `c9550255b80894c1cf05f447bb55c1b95e6e2fff`
> **내 저장소 반영 커밋:** `be0dd272c61df35dc47592d6bc759fb59beff98e`
>
> 강의실 원본 `.ipynb`, PNG, TXT, JSON, README, requirements 및 .gitignore **19개 파일을 바이트 단위 동일하게 복사**했습니다. 사용자 기존 과제 코드는 수정하지 않았습니다.

## Windows 11 + VS Code

**VS Code Extensions**에서 Microsoft **Python** 및 **Jupyter** 확장 설치.

### 1. 처음 PC로 가져오기

PowerShell 터미널:

```powershell
cd C:\workspace
git clone https://github.com/choisunghwan1004-dev/postfolio.git
cd .\postfolio\course-source\ai-datajournalism-labs
code .
```

이미 `C:\workspace\postfolio`를 내려받았다면 **다시 clone하지 말고**:

```powershell
cd C:\workspace\postfolio
git pull origin main
cd .\course-source\ai-datajournalism-labs
code .
```

### 2. Python 독립 환경 만들기

VS Code의 **Terminal > New Terminal**에서 (현재 폴더는 `ai-datajournalism-labs`):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Windows PowerShell 실행 정책으로 Activate가 차단돼도 위의 `.venv\Scripts\python.exe` 직접 실행 방식은 활성화 없이 사용할 수 있습니다.

### 3. 실행 순서

1. `0_환경확인/check_env.ipynb` 열기.
2. VS Code 오른쪽 위 **Select Kernel(커널 선택) → Python Environments → .venv**.
3. **Run All(모두 실행)**.
4. 이어서 `1_시각화기초/visualization_basics.ipynb`, `2_빅데이터_차트문법/1_bigdata_news_vs_air.ipynb` 및 `2_chart_grammar.ipynb` 실행.

수업 원본 코드 자체는 변경하지 않았으므로, 일부 노트북의 다운로드/외부 API/GPU 호출은 네트워크와 PC 사양에 따라 추가 설정이 필요합니다.

### 4. 데이터 파일 주의

원본 강의 GitHub에는 대용량 BigKinds Excel, `data_air_2022.csv` 같은 실측 파일이 **포함되지 않습니다**. 이 파일들은 기존 Google Drive 수업 자료에서 내려받아 사용하세요. 노트북 안의 상대경로를 보고 적절한 폴더에 배치해야 합니다. 공개 저장소에 원본 저작권 자료나 `.env` API 키를 업로드하지 마세요.

- 개인 수업자료 폴더: https://drive.google.com/drive/folders/1vpLwF3T5nS7On0gImyEsTEhDCOT0kIIM
- 기존 실측 미세먼지 과제의 실행/검증 자료는 **별도 과제 폴더**에서 관리합니다.

### 5. 소스 저작권·출처

이 하위 폴더는 강의 원본을 공부하기 위한 **출처 표시 보존본**입니다. 원본 트리에는 명시적인 LICENSE 파일이 확인되지 않았습니다. 공개 재배포 및 2차 이용 허락 범위는 강의 저장소 운영자에게 별도로 확인해 주세요. GitHub에 공개돼 있다는 사실만으로 자유 라이선스가 부여되는 것은 아닙니다.

### 6. 앞으로 원본 업데이트

이 폴더의 원본을 실습 중 직접 수정하지 말고, 다른 `assignments/` 폴더에 수정본을 만들면 원본과 비교하기 쉽습니다. 강의 원본이 업데이트되어도 이 커밋을 기준으로 비교할 수 있습니다.
