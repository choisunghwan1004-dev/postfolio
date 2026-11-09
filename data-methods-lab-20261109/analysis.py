"""통합수업일지(2026-10-29~11-09) 교육용 실습. 가상 CSV 재계산; 실제 통계 아님."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, silhouette_score
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors

ROOT=Path(__file__).resolve().parent
D=ROOT/"data"
raw=pd.read_csv(D/"sports_center_members_demo.csv")
meta=pd.read_csv(D/"program_metadata_demo.csv")
movies=pd.read_csv(D/"movie_ratings_demo.csv")
assert len(raw)==50
duplicates=int(raw.member_id.duplicated().sum())
clean=raw.drop_duplicates(subset="member_id").copy()
invalid=int(clean.visits_per_month.lt(0).sum())
clean.loc[clean.visits_per_month.lt(0),"visits_per_month"]=np.nan
missing={col:int(clean[col].isna().sum()) for col in
         ("monthly_fee_krw_1000","visits_per_month","satisfaction_1to5")}
for col in missing:
    clean[col]=clean[col].fillna(clean[col].median())
assert len(clean)==48 and clean.isna().sum().sum()==0
merged=clean.merge(meta,on="program",validate="many_to_one")
group=merged.groupby(["program","program_name"],as_index=False).agg(
    count=("member_id","size"),avg_visits=("visits_per_month","mean"),
    avg_satisfaction=("satisfaction_1to5","mean"))
corr=float(clean.months_active.corr(clean.visits_per_month))
a=clean.loc[clean.program.eq("A"),"visits_per_month"]
b=clean.loc[clean.program.eq("B"),"visits_per_month"]
t,p=ttest_ind(a,b,equal_var=False)
features=clean[["age","months_active","monthly_fee_krw_1000"]].copy()
features["program_B"]=clean.program.eq("B").astype(int)
xtr,xte,ytr,yte=train_test_split(features,clean.visits_per_month,test_size=.25,random_state=42)
reg=make_pipeline(SimpleImputer(strategy="median"),StandardScaler(),LinearRegression())
reg.fit(xtr,ytr)
prediction=reg.predict(xte)
z=StandardScaler().fit_transform(clean[["visits_per_month","monthly_fee_krw_1000","satisfaction_1to5"]])
elbow={str(k):round(float(KMeans(n_clusters=k,random_state=42,n_init=20).fit(z).inertia_),4)
       for k in range(2,7)}
km=KMeans(n_clusters=3,random_state=42,n_init=20)
clean["cluster"]=km.fit_predict(z)
groups=clean.groupby("cluster").agg(count=("member_id","size"),avg_visits=("visits_per_month","mean"))
nn=NearestNeighbors(metric="cosine",n_neighbors=4).fit(movies.drop(columns="movie").values)
dist,index=nn.kneighbors(movies.drop(columns="movie").values[[0]])
recommended=[{"movie":str(movies.iloc[i]["movie"]),"similarity":round(float(1-v),4)}
             for i,v in zip(index[0],dist[0]) if i!=0][:3]
result={
  "dataset":"가상 스포츠센터 회원·가상 영화 평점",
  "not_real_data":True,
  "raw_rows":len(raw),"duplicates":duplicates,"clean_rows":len(clean),
  "invalid_visits":invalid,"missing_counts":missing,
  "group_stats":[{"program":r.program,"name":r.program_name,"n":int(r.count),
                  "mean_visits":round(float(r.avg_visits),4)} for r in group.itertuples()],
  "corr":round(corr,4),"welch_t":round(float(t),4),"welch_p":round(float(p),6),
  "regression":{"train":len(xtr),"test":len(xte),
                "mae":round(float(mean_absolute_error(yte,prediction)),4),
                "r2":round(float(r2_score(yte,prediction)),4)},
  "kmeans":{"k":3,"silhouette":round(float(silhouette_score(z,clean.cluster)),4),
            "elbow":elbow,"clusters":[{"cluster":int(i),"n":int(r["count"]),
             "avg_visits":round(float(r["avg_visits"]),2)} for i,r in groups.iterrows()]},
  "movieA_neighbors":recommended
}
assert result["duplicates"]==2 and result["clean_rows"]==48
assert abs(result["corr"]-0.6374)<.0001
(D/"analysis_results.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(result,ensure_ascii=False,indent=2))
print("ANALYSIS_PASS: all synthetic analytics stages completed")
