"""V1.2: read-only parameterized comparisons of statistical methods.

For educational small/medium tabular data; never claims causality or distributed execution.
"""
from __future__ import annotations
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

METHODS_V12 = {
    'summary': {'name':'기술통계', 'requires':'숫자 열 1개', 'example':'선택한 기간의 PM10 평균·중앙값·표준편차', 'caution':'결측과 이상치, 관측 단위를 확인'},
    'group_compare': {'name':'집단별 요약', 'requires':'그룹 열+숫자 열', 'example':'지역별 PM10 평균·중앙값', 'caution':'집단 크기와 비교 가능성을 확인'},
    'timeseries': {'name':'시간 추세·이동평균', 'requires':'날짜 열+숫자 열', 'example':'날짜별 PM10 이동평균', 'caution':'관측 간격과 누락 날짜를 확인'},
    'correlation': {'name':'Pearson/Spearman 상관', 'requires':'두 수치 열+유효 쌍 3개 이상', 'example':'PM10과 PM2.5 관계', 'caution':'상관은 인과를 뜻하지 않으며 극단값에 유의'},
}

@dataclass(frozen=True)
class Scenario:
    name: str = '기본'
    method: str = 'summary'
    value_col: str = 'pm10'
    second_col: Optional[str] = None
    group_col: Optional[str] = None
    date_col: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    filter_col: Optional[str] = None
    filter_equals: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    window: int = 7
    missing_policy: str = 'drop'


def _validate(s: Scenario, columns: list[str]):
    if s.method not in METHODS_V12: raise ValueError('등록되지 않은 기법')
    if s.missing_policy != 'drop': raise ValueError('V1.2에서는 결측 제거만 지원; 임의 대치 없음')
    needed=[s.value_col]
    if s.method=='group_compare':needed += [s.group_col]
    if s.method=='timeseries':needed += [s.date_col]
    if s.method=='correlation':needed += [s.second_col]
    if s.filter_col and s.filter_equals is not None:needed += [s.filter_col]
    if s.start_date or s.end_date:needed += [s.date_col]
    missing=[c for c in needed if not c or c not in columns]
    if missing: raise ValueError(f'분석에 필요한 열 없음/미지정: {missing}')
    if s.method=='correlation' and s.second_col == s.value_col:raise ValueError('상관에는 서로 다른 두 수치 열 필요')
    if s.window < 2 or s.window > 90:raise ValueError('이동평균 기간은 2~90')
    if s.min_value is not None and not math.isfinite(s.min_value):raise ValueError('최소 기준값 오류')
    if s.max_value is not None and not math.isfinite(s.max_value):raise ValueError('최대 기준값 오류')
    if s.min_value is not None and s.max_value is not None and s.min_value > s.max_value:raise ValueError('최소값이 최대값보다 큼')
    if s.start_date and s.end_date and s.start_date > s.end_date:raise ValueError('시작 날짜가 종료 날짜보다 늦음')


def recommend_methods(columns:list[dict], *, goal='summary') -> list[dict]:
    """Recommendations depend on column profiles, but don't imply actual data suitability."""
    names={c['column'] for c in columns}
    numeric=[c['column'] for c in columns if c.get('inferred_type')=='numeric']
    dates=[c['column'] for c in columns if c.get('date_name_hint')]
    opts=[]
    for key,d in METHODS_V12.items():
        unmet=[]
        if not numeric: unmet.append('수치 열 확인')
        if key=='correlation' and len(numeric)<2:unmet.append('수치 열 2개 확인')
        if key=='timeseries' and not dates:unmet.append('날짜 열 선택')
        if key=='group_compare' and len(names)<2:unmet.append('그룹 열 선택')
        opts.append({'id':key,**d,'status':'candidate' if not unmet else 'needs_conditions', 'conditions_to_confirm':unmet, 'goal_match':key==goal or (goal=='trend' and key=='timeseries') or (goal=='relationship' and key=='correlation')})
    return sorted(opts,key=lambda x:(not x['goal_match'], x['status']!='candidate'))


def run_scenario(path:Path, scenario:Scenario, *, encoding='utf-8-sig', max_csv_bytes=64*1024*1024, max_result_rows=10000) -> dict:
    """Runs against full file only below explicit safe bound; no source mutation."""
    path=Path(path)
    if not path.is_file():raise FileNotFoundError(path)
    if path.stat().st_size>max_csv_bytes:raise ValueError('64MiB 초과: V1.2 직접 실행 제한; Dask/Polars 검증 후 처리')
    with path.open(encoding=encoding,newline='') as h:
        columns=next(csv.reader(h),[])
    if not columns or len(set(columns))!=len(columns) or any(not c.strip() for c in columns):raise ValueError('CSV 헤더 누락·중복·공백')
    _validate(scenario,columns)
    import pandas as pd
    df=pd.read_csv(path,encoding=encoding)
    original_n=len(df)
    s=scenario
    if s.filter_col and s.filter_equals is not None:
        df=df[df[s.filter_col].astype('string')==s.filter_equals]
    if s.start_date or s.end_date:
        date=pd.to_datetime(df[s.date_col],errors='coerce')
        df=df[date.notna()].copy()
        date=pd.to_datetime(df[s.date_col],errors='coerce')
        if s.start_date: df=df[date>=pd.Timestamp(s.start_date)] ; date=pd.to_datetime(df[s.date_col],errors='coerce')
        if s.end_date: df=df[date<=pd.Timestamp(s.end_date)]
    df=df.copy()
    df[s.value_col]=pd.to_numeric(df[s.value_col],errors='coerce')
    if s.min_value is not None: df=df[df[s.value_col]>=s.min_value]
    if s.max_value is not None: df=df[df[s.value_col]<=s.max_value]
    result:dict={}
    if s.method=='summary':
        x=df[s.value_col].dropna()
        if x.empty:raise ValueError('조건에 맞는 유효 수치 관측이 없음')
        result={'count':int(x.count()),'mean':float(x.mean()),'median':float(x.median()),'std':float(x.std()) if len(x)>1 else None,'min':float(x.min()),'max':float(x.max())}
    elif s.method=='group_compare':
        df=df[df[s.group_col].notna() & df[s.value_col].notna()]
        if df.empty:raise ValueError('그룹별 유효 관측이 없음')
        r=df.groupby(s.group_col,dropna=True)[s.value_col].agg(['count','mean','median']).reset_index()
        if len(r)>max_result_rows:raise ValueError('그룹 수 상한 초과')
        result={'groups':[{s.group_col:str(v[s.group_col]), 'count':int(v['count']),'mean':float(v['mean']),'median':float(v['median'])} for _,v in r.iterrows()]}
    elif s.method=='timeseries':
        df['_date']=pd.to_datetime(df[s.date_col],errors='coerce')
        df=df.dropna(subset=['_date',s.value_col]).sort_values('_date')
        # Same date may have multiple observations; aggregate first to preserve one data point per day.
        day=df.groupby('_date')[s.value_col].mean().sort_index()
        if day.empty:raise ValueError('유효 시계열 자료 없음')
        if len(day)>max_result_rows:raise ValueError('시계열 출력 상한 초과')
        roll=day.rolling(s.window,min_periods=s.window).mean()
        result={'window':s.window,'series':[{'date':t.isoformat()[:10], 'value':float(v),'moving_average':None if pd.isna(roll.loc[t]) else float(roll.loc[t])} for t,v in day.items()]}
    else:
        df[s.second_col]=pd.to_numeric(df[s.second_col],errors='coerce')
        pair=df[[s.value_col,s.second_col]].replace([float('inf'),float('-inf')],float('nan')).dropna()
        if len(pair)<3:raise ValueError('상관분석 유효 쌍 최소 3개 필요')
        if pair[s.value_col].nunique()<2 or pair[s.second_col].nunique()<2:raise ValueError('상관분석 두 변수 모두 변화가 있어야 함')
        result={'pairs':len(pair),'pearson':float(pair.corr(method='pearson').iloc[0,1]),'spearman':float(pair.corr(method='spearman').iloc[0,1]),'causality_warning':'상관은 인과관계를 뜻하지 않습니다.'}
    return {'status':'executed_locally','backend':'pandas','source':path.name,'input_rows':original_n,'filtered_rows':len(df),'scenario':asdict(s),'result':result,'limits':'본 도구 결과는 교육용 기술통계이며 대표성/인과관계 미보증'}


def compare_scenarios(path:Path, scenarios:list[Scenario], *, encoding='utf-8-sig')->dict:
    if len(scenarios)>12:raise ValueError('비교는 최대 12개 조건')
    out=[]
    for s in scenarios:
        try: out.append(run_scenario(path,s,encoding=encoding))
        except (ValueError,KeyError,UnicodeError,FileNotFoundError) as e:out.append({'scenario':asdict(s),'status':'blocked','error':str(e)})
    return {'count':len(out),'scenarios':out,'note':'조건·기법 변경 시 다시 계산함; 서로 다른 표본의 결과를 직접 비교할 때 주의'}
