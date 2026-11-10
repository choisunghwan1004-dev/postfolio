# PyTorch · TensorFlow · 통계 모델 비교 실습 (추가3)

> **상태: 코드 등록 / 실제 3모델 통합 학습 결과 미검증.**
> 기존 포트폴리오, 로또, K-pop/Olist, 차트 저널리즘 UI·코드는 수정하지 않습니다.

## 목표
- 같은 **교육용 가상 이진분류 데이터**로 기준 통계/머신러닝 모델(LogisticRegression), PyTorch 신경망, TensorFlow 신경망을 비교
- 같은 train/test 분할과 StandardScaler를 사용하고 테스트 정확도·F1·ROC AUC를 기록
- 테스트 자료를 학습·전처리기에 섞지 않고, 가능하면 반복 실행 결과도 점검
- 모델 파일은 GitHub에 올리지 않고 결과 지표 JSON·차트만 가볍게 공개

## 실행 (Windows 11 / Python 3.11 또는 3.12 권장)
```powershell
cd data-methods-lab-20261109\deep-learning-comparison
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe train_compare.py
```
실행 전 디스크·메모리·Python 및 패키지 호환성을 확인합니다. TensorFlow/PyTorch 설치 용량이 클 수 있습니다. Windows 네이티브 TensorFlow GPU 지원은 환경별 제약이 있으므로 기본값은 **CPU**입니다.

## 실행 후 파일
- `results/metrics.json`: 실제 실행 시점, 라이브러리 버전, 데이터·분할 정보, 테스트 지표 (실행 전에는 존재하지 않음)
- `results/compare.png`: 모델 비교 차트
- `results/compare.svg`: GitHub Pages 경량 비교 차트
- 모델 가중치 및 원본 대용량 데이터 파일: **생성·커밋하지 않음**
- `index.html`: 모델 실행이 아닌 **실제 저장된 JSON 결과 표시 화면**. GitHub Pages에서 직접 파일을 읽습니다. 결과 미생성 시 '미검증' 안내 표시.

## 검증
1. 같은 데이터 인덱스로 학습/시험을 나누고 scaler는 학습 데이터에만 fit
2. 세 모델이 동일한 test set을 예측했는지 확인
3. accuracy, F1, ROC AUC는 서로 다른 평가 관점. 작은 점수 차이만으로 우수성을 단정하지 않음
4. 한 번의 랜덤 시드 결과로 일반화 성능 확정 불가. 추후 반복 시드/교차검증, 클래스 불균형 테스트 필요
5. **실제 뉴스나 로또 당첨번호 예측 데이터가 아니며 미래 예측력 주장 금지**

## 플랫폼 선택
- **GitHub Pages**: 정적 HTML·요약 JSON·SVG, 무료 교육용 화면. Python 학습은 실행 안 됨
- **Streamlit Cloud**: 별도 Streamlit 앱을 작성·검증한 경우에만 동적 배포; 등록만으로 배포된 것은 아님
- **Render / Cloud Run**: 실시간 API가 실제로 필요할 때 선택, 가격·요금 한도·메모리·슬립 정책 확인
- **외부 저장소/DB**: 모델·원본 대용량 데이터, 재시작 후에도 남아야 하는 값. 권리·공개범위 확인 필수

## 교육자료 연결
- 「내 앱은 어디에 올릴까? 배포 플랫폼 7가지」: 정적/동적 구분, 서버 데이터 지속성, GitHub Pages·Streamlit·Render 분리
- 「Olist 대시보드 Streamlit 배포하기」: GitHub 저장소/앱 경로/Secrets/로그/메뉴 점검
- 「빅데이터와 저널리즘 · 기사용 차트 문법」: 질문→수집→정제→분석→검증→기사, 차트 6규칙, 실측/가상 구분

## 배포 체크리스트
[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) 참조.
