"""Execute one low-risk aggregation, backend explicit. Never fall back silently.
The result is a small output; input is not modified. Supports pandas/Dask/Polars.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path


def execute(path,group_col,value_col,backend='pandas',encoding='utf-8-sig'):
    if not Path(path).is_file():raise FileNotFoundError(str(path))
    if backend=='pandas':
        import pandas as pd
        data=pd.read_csv(path,encoding=encoding,usecols=[group_col,value_col])
        data[value_col]=pd.to_numeric(data[value_col],errors='coerce')
        output=data.groupby(group_col,dropna=False)[value_col].agg(['count','mean']).reset_index()
        return output.to_dict(orient='records')
    if backend=='Dask':
        import dask.dataframe as dd
        df=dd.read_csv(str(path),encoding=encoding,assume_missing=True,blocksize='32MB')
        values=dd.to_numeric(df[value_col],errors='coerce')
        # Keep output aggregated; compute only the reduced table.
        g=df.assign(_numeric_value=values).groupby(group_col)['_numeric_value'].agg(['count','mean']).compute().reset_index()
        return g.to_dict(orient='records')
    if backend=='Polars':
        import polars as pl
        frame=(pl.scan_csv(str(path),encoding='utf8-lossy' if encoding!='utf-8-sig' else 'utf8')
               .with_columns(pl.col(value_col).cast(pl.Float64,strict=False))
               .group_by(group_col).agg(pl.col(value_col).count().alias('count'),pl.col(value_col).mean().alias('mean')))
        return frame.collect(engine='streaming').to_dicts()
    raise ValueError('run_group.py 지원 엔진: pandas, Dask, Polars. Ray/PySpark 분산 작업은 REA 검증 이후 연결')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--csv',type=Path,required=True)
    p.add_argument('--group',required=True);p.add_argument('--value',required=True)
    p.add_argument('--backend',choices=['pandas','Dask','Polars'],default='pandas')
    p.add_argument('--encoding',default='utf-8-sig')
    p.add_argument('--out',type=Path)
    args=p.parse_args()
    data=execute(args.csv,args.group,args.value,args.backend,args.encoding)
    raw=json.dumps({'status':'executed','backend':args.backend,'result':data},ensure_ascii=False,indent=2,default=str)
    if args.out:args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(raw,encoding='utf-8')
    print(raw)
