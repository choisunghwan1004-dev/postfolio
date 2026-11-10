"""Low-risk count/mean group aggregation. No implicit backend fallback.
All backends must use the same explicit missing-group policy.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
from pathlib import Path

SUPPORTED = {"pandas", "Dask", "Polars"}


def _validate_inputs(path, group_col, value_col, backend, encoding):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"입력 CSV를 찾을 수 없습니다: {path}")
    if backend not in SUPPORTED:
        raise ValueError("사용 가능한 집계 엔진: pandas, Dask, Polars")
    if group_col == value_col:
        raise ValueError("집단 열과 수치 열은 서로 달라야 합니다")
    with path.open('r', encoding=encoding, newline='') as f:
        header = next(csv.reader(f), [])
    if not header or len(set(header)) != len(header):
        raise ValueError("CSV 헤더 누락/중복")
    missing = [x for x in (group_col, value_col) if x not in header]
    if missing:
        raise ValueError(f"선택한 열을 찾을 수 없습니다: {missing}; 실제 열: {header}")
    return path


def _normalize(records, group_col):
    """Small grouped results only. Keep group None as JSON null and avoid NaN/Inf."""
    output=[]
    for x in records:
        group=x[group_col]
        if not isinstance(group, str):
            # Only string grouping values are accepted. pandas.NA and float NaN are null.
            group=None
        mean=x['mean']
        if mean is None or (isinstance(mean,float) and not math.isfinite(mean)):
            mean=None
        output.append({group_col:group, 'count':int(x['count']), 'mean':None if mean is None else float(mean)})
    return sorted(output,key=lambda x:(x[group_col] is None,str(x[group_col])))


def execute(path, group_col, value_col, backend='pandas', encoding='utf-8-sig', max_groups=10000):
    path = _validate_inputs(path,group_col,value_col,backend,encoding)
    if not isinstance(max_groups,int) or max_groups<=0:
        raise ValueError('max_groups는 양수 정수')
    if backend=='pandas':
        if path.stat().st_size > 256 * 1024 * 1024:
            raise ValueError('pandas V1.1 안전 상한: 입력 CSV 256 MiB 초과. Polars/Dask를 사용하거나 데이터 범위를 분할하세요')
        import pandas as pd
        df=pd.read_csv(path,encoding=encoding,usecols=[group_col,value_col],dtype={group_col:'string'})
        df[value_col]=pd.to_numeric(df[value_col],errors='coerce')
        result=df.groupby(group_col,dropna=False)[value_col].agg(['count','mean']).reset_index()
        if len(result)>max_groups:raise ValueError('그룹 수 상한 초과: 더 좁은 범위를 선택하세요')
        return _normalize(result.to_dict(orient='records'),group_col)
    if backend=='Dask':
        if encoding.lower() not in ('utf-8','utf-8-sig'):
            raise ValueError('Dask V1.1은 UTF-8 CSV만 지원합니다. CP949 원본은 별도 변환·승인 후 실행하세요')
        import dask.dataframe as dd
        df=dd.read_csv(str(path),encoding=encoding,blocksize='32MB',dtype={group_col:'string'},assume_missing=True,usecols=[group_col,value_col])
        numeric=dd.to_numeric(df[value_col],errors='coerce')
        df=df.assign(_numeric_value=numeric)
        # Groupby with dropna=False aligns the explicit pandas missing-group policy.
        agg=df.groupby(group_col,dropna=False)['_numeric_value'].agg(['count','mean']).compute().reset_index()
        if len(agg)>max_groups:raise ValueError('그룹 수 상한 초과: 더 좁은 범위를 선택하세요')
        return _normalize(agg.to_dict(orient='records'),group_col)
    if encoding.lower() not in ('utf-8','utf-8-sig'):
        raise ValueError('Polars V1.1은 UTF-8 CSV만 지원합니다. CP949 원본은 별도 변환·승인 후 실행하세요')
    import polars as pl
    frame=(pl.scan_csv(str(path),encoding='utf8',infer_schema_length=0)
       .with_columns(pl.col(value_col).cast(pl.Float64,strict=False))
       .group_by(group_col).agg(pl.col(value_col).count().alias('count'),pl.col(value_col).mean().alias('mean')))
    result=frame.collect(engine='streaming')
    if result.height>max_groups:raise ValueError('그룹 수 상한 초과: 더 좁은 범위를 선택하세요')
    return _normalize(result.to_dicts(),group_col)


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--csv',type=Path,required=True)
    p.add_argument('--group',required=True);p.add_argument('--value',required=True)
    p.add_argument('--backend',choices=sorted(SUPPORTED),default='pandas')
    p.add_argument('--encoding',default='utf-8-sig')
    p.add_argument('--max-groups',type=int,default=10000)
    p.add_argument('--out',type=Path)
    args=p.parse_args()
    data=execute(args.csv,args.group,args.value,args.backend,args.encoding,args.max_groups)
    raw=json.dumps({'status':'executed','backend':args.backend,'result':data},ensure_ascii=False,indent=2,allow_nan=False)
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(raw,encoding='utf-8')
    print(raw)
