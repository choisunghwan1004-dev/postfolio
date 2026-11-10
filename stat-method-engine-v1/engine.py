"""Statistical method adviser, V1.0. Safe read-only inspection + small data execution.

Never loads an entire untrusted CSV merely to suggest an engine. No eval or shell calls.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
from collections import Counter
from datetime import datetime
from pathlib import Path

METHODS = [
 {"id":"quality", "name":"결측·중복·자료형 진단", "goals":["quality","any"], "required":"식별할 열·원본 행 수", "caution":"표본 결과와 전체 결과 구분", "example":"미세먼지 관측값이 비어 있는 날짜 확인"},
 {"id":"summary", "name":"기술통계·분포·사분위수", "goals":["summary","any"], "required":"숫자형 변수, 단위, 모집단 범위", "caution":"극단값·가중치·결측 처리", "example":"종로구 PM10 일평균·중앙값"},
 {"id":"timeseries", "name":"시계열 추세·이동평균·계절성", "goals":["trend"], "required":"날짜·측정값·시간 간격", "caution":"누락 날짜·시계열 분할·계절 효과", "example":"월별 PM10 추세"},
 {"id":"correlation", "name":"Pearson/Spearman 상관", "goals":["relationship"], "required":"두 수치형 변수·독립 관측 정의", "caution":"상관 ≠ 인과, 자기상관, 이상치", "example":"기사 건수와 PM10의 동행 관계"},
 {"id":"hypothesis", "name":"t검정·비모수 검정·카이제곱", "goals":["difference"], "required":"집단 구분·표본 독립성·검정 목적", "caution":"분포·등분산·다중검정·효과크기", "example":"두 지역 PM10 평균 차이"},
 {"id":"regression", "name":"회귀·예측·잔차 진단", "goals":["prediction","relationship"], "required":"정답 열·입력 열·자료 분할", "caution":"데이터 누출·과적합·시계열 분할", "example":"기온·습도로 PM10 추정"},
 {"id":"classification", "name":"분류·로지스틱 회귀·트리", "goals":["classification"], "required":"범주형 정답·입력 변수", "caution":"클래스 불균형·정밀도·재현율", "example":"고농도 경보 여부 분류"},
 {"id":"clustering", "name":"KMeans·군집", "goals":["segmentation"], "required":"수치 특성·스케일·거리 정의", "caution":"군집 수 선택·거리 의미", "example":"지역 대기질 패턴 군집"},
 {"id":"text", "name":"텍스트 빈도·TF-IDF·임베딩", "goals":["text"], "required":"텍스트 열·언어·저작권", "caution":"토큰화·개인정보·의미 유사도 검증", "example":"기사 제목 주제 묶기"},
 {"id":"probability", "name":"확률분포·시뮬레이션·부트스트랩", "goals":["probability"], "required":"표본추출 가정·반복 수·난수 시드", "caution":"독립 가정·표본 편향·미래 누출", "example":"표본평균 신뢰구간"},
 {"id":"deep_learning", "name":"PyTorch·TensorFlow 신경망", "goals":["deep_learning"], "required":"학습·검증·시험 분할·목적함수", "caution":"GPU/메모리·반복실험·재현성", "example":"다변량 자료 신경망 비교"}
]
GOALS = {"quality":"데이터 품질", "summary":"요약 통계", "trend":"시간 변화", "relationship":"관계", "difference":"집단 차이", "prediction":"연속값 예측", "classification":"범주 예측", "segmentation":"군집", "text":"텍스트", "probability":"확률", "deep_learning":"딥러닝"}


def inspect_csv(path: Path, *, sample_limit: int = 500, encoding="utf-8-sig") -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"데이터 파일 없음: {path}")
    if not 1 <= sample_limit <= 10000:
        raise ValueError("표본 상한은 1~10000")
    size = path.stat().st_size
    with path.open('r', encoding=encoding, newline='') as handle:
        reader=csv.DictReader(handle)
        columns=reader.fieldnames or []
        if not columns: raise ValueError("CSV 헤더가 없습니다")
        if len(set(columns)) != len(columns): raise ValueError("중복 열 이름")
        empty=Counter(); nonempty=Counter(); numeric=Counter(); distinct={k:set() for k in columns}
        sampled=0
        for row in reader:
            if sampled>=sample_limit: break
            sampled+=1
            for col in columns:
                val=(row.get(col) or '').strip()
                if not val: empty[col]+=1;continue
                nonempty[col]+=1
                if len(distinct[col])<1000: distinct[col].add(val)
                try:
                    z=float(val)
                    if math.isfinite(z): numeric[col]+=1
                except ValueError: pass
    colinfo=[]
    for c in columns:
        typ="numeric" if nonempty[c]>0 and numeric[c]/nonempty[c] >= .9 else "text_or_mixed"
        maybe_date= any(k in c.lower() for k in ('date','day','time','날짜','일시','연월'))
        colinfo.append({"column":c,"inferred_type":typ,"date_name_hint":maybe_date,"missing_in_sample":empty[c],"distinct_in_sample_up_to_1000":len(distinct[c])})
    return {"file":path.name,"size_bytes":size,"sampled_rows":sampled,"total_rows":"not_counted","encoding":encoding,"columns":colinfo,"inspection":"sample_only; no full-file materialization"}


def choose_backend(size_bytes: int, ram_gb: float, goal: str, *, distributed: bool=False, pandas_familiar:bool=True, gpu:bool=False) -> dict:
    if ram_gb <= 0 or size_bytes < 0: raise ValueError("RAM과 파일 크기를 확인하세요")
    # Heuristic only, never performance guarantee. CSV memory can be many times disk size.
    ratio=size_bytes/(ram_gb*(1024**3))
    reasons=[]
    if distributed:
        backend='Ray' if goal in ('deep_learning','classification','prediction') and gpu else 'PySpark'
        reasons.append('클러스터/분산 작업 요청')
    elif goal=='deep_learning' and gpu and ratio<.15:
        backend='PyTorch/TensorFlow'; reasons.append('GPU 기반 단일 장치 학습 우선, 분산 불필요')
    elif ratio >= .3:
        backend='Dask' if pandas_familiar else 'Polars'
        reasons.append('파일 크기 대비 RAM 여유가 작음; 파일 크기 비율은 휴리스틱')
    elif ratio>=.08:
        backend='Polars' if not pandas_familiar else 'Dask'
        reasons.append('메모리 위험 가능성: 지연 실행/분할 처리 검토')
    else:
        backend='pandas'
        reasons.append('소규모 자료에는 간단한 pandas 우선')
    if backend=='Dask': reasons.append('pandas와 유사하지만 일부 API·실행 의미가 다르고 compute()에 주의')
    if backend=='Polars': reasons.append('pandas 문법과 동일하지 않음; lazy scan 및 스트리밍 지원 여부 확인')
    if backend=='Ray': reasons.append('Ray Train/Tune은 설치·GPU·클러스터 설정과 분산 학습 검증 필요')
    if backend=='PySpark': reasons.append('Spark MLlib의 최신 DataFrame 기반 spark.ml API 사용')
    return {"recommended":backend,"alternatives":[x for x in ("pandas","Polars","Dask","Ray","PySpark") if x!=backend],"file_to_ram_ratio":round(ratio,4),"heuristic_only":True,"reasons":reasons}


def advise(inspection:dict,goal:str,ram_gb:float,distributed=False,pandas_familiar=True,gpu=False):
    if goal not in GOALS:raise ValueError('지원되지 않는 분석 목적: '+goal)
    methods=[m for m in METHODS if goal in m['goals'] or 'any' in m['goals']]
    columns=inspection['columns']
    num=[c['column'] for c in columns if c['inferred_type']=='numeric']
    dates=[c['column'] for c in columns if c['date_name_hint']]
    warnings=[]
    if goal in ('trend',) and not dates: warnings.append('날짜 열을 지정해야 합니다.')
    if goal in ('relationship','difference','prediction','summary') and not num: warnings.append('수치형 열을 지정해야 합니다.')
    if inspection['sampled_rows']==0: warnings.append('표본 데이터 행이 없습니다.')
    return {"input":inspection,"goal":goal,"goal_label":GOALS[goal],"method_candidates":methods,"backend":choose_backend(inspection['size_bytes'],ram_gb,goal,distributed=distributed,pandas_familiar=pandas_familiar,gpu=gpu),"suggested_numeric_columns":num,"date_name_hints":dates,"questions_to_confirm":["분석 질문과 정답/결과 열은 무엇인가?","관측 단위·기간·대상·원본 출처는 무엇인가?","결측·중복·이상치·개인정보를 어떻게 처리할 것인가?","표본 결과를 전체 결과로 오해하지 않는가?","반복/시간순 분할과 검증 지표는 무엇인가?"],"warnings":warnings,"status":"recommendation_only; not trained"}


def main(argv=None):
    p=argparse.ArgumentParser(description='Statistical Method Adviser V1')
    p.add_argument('--csv',type=Path,required=True)
    p.add_argument('--goal',choices=GOALS,default='summary')
    p.add_argument('--ram-gb',type=float,default=8)
    p.add_argument('--encoding',default='utf-8-sig')
    p.add_argument('--distributed',action='store_true')
    p.add_argument('--gpu',action='store_true')
    p.add_argument('--prefer-polars',action='store_true')
    p.add_argument('--out',type=Path)
    args=p.parse_args(argv)
    info=inspect_csv(args.csv,encoding=args.encoding)
    report=advise(info,args.goal,args.ram_gb,distributed=args.distributed,pandas_familiar=not args.prefer_polars,gpu=args.gpu)
    raw=json.dumps(report,ensure_ascii=False,indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(raw,encoding='utf-8')
    print(raw)

if __name__=='__main__':main()
