"""로또 확률·통계 + '데이터 분석 기법 더하기.pdf' 10기법 과제.
데이터: 사용자 제공 1~1248회 CSV에서 추출한 949~1248회(2021-02-06~2026-10-31).
최신 회차 자동 갱신·다음 번호 예측 없음. 난수 시드 고정 / 과거자료만 이용.
실제 당첨번호 분석과 합성 고객·지역·댓글 예제를 엄격히 분리.
"""
from __future__ import annotations
from pathlib import Path
from collections import Counter
from itertools import combinations
from math import comb
import json
import random

import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
CHART = BASE / "charts"
DATA.mkdir(exist_ok=True)
CHART.mkdir(exist_ok=True)
plt.rcParams.update({"font.family": "NanumSquare", "axes.unicode_minus": False,
                     "figure.facecolor": "#ffffff", "axes.spines.top": False,
                     "axes.spines.right": False, "font.size": 11})
NAMES = [f"n{i}" for i in range(1, 7)]
draws = pd.read_csv(DATA / "lotto_949_1248_sample.csv")
prizes = pd.read_csv(DATA / "lotto_949_1248_sales_prize.csv")
draws = draws.sort_values("drwNo").reset_index(drop=True)
prizes = prizes.sort_values("drwNo").reset_index(drop=True)
assert len(draws) == len(prizes) == 300
assert draws.drwNo.tolist() == list(range(949,1249)), "누락·중복 회차"
assert (draws.drwNo == prizes.drwNo).all(), "회차 불일치"
assert (draws.drwNoDate == prizes.drwNoDate).all(), "추첨일 불일치"
numbers = draws[NAMES].to_numpy(dtype=int)
bonuses = draws.bonus.to_numpy(dtype=int)
assert np.all((numbers >= 1) & (numbers <= 45)) and np.all((bonuses >= 1) & (bonuses <= 45))
assert all(len(set(r))==6 and int(b) not in r for r,b in zip(numbers,bonuses))
freq = np.bincount(numbers.ravel(),minlength=46)[1:].astype(int)
assert freq.sum()==1800
recent60 = np.bincount(numbers[-60:].ravel(),minlength=46)[1:].astype(int)
pair_counter = Counter(pair for draw in numbers for pair in combinations(sorted(draw),2))
consecutive = [sum((int(b)-int(a)==1) for a,b in zip(sorted(r),sorted(r)[1:])) for r in numbers]
draw_sum = numbers.sum(axis=1)
odd_counts = (numbers % 2).sum(axis=1)
low_counts = (numbers <= 22).sum(axis=1)
multiples3 = (numbers % 3 == 0).sum(axis=1)
end_digits = np.bincount((numbers % 10).ravel(),minlength=10)
hot = sorted(range(1,46),key=lambda x:(-freq[x-1],x))[:6]
cold = sorted(range(1,46),key=lambda x:(freq[x-1],x))[:6]
theory = {str(k):comb(6,k)*comb(39,6-k)/comb(45,6) for k in range(7)}
assert sum(theory.values())>0.9999999
consecutive_theory = 1-comb(40,6)/comb(45,6) # 인접 숫자 없는 경우의 여사건

# 공정한 무작위 6/45 추첨에서만 나오는 변동폭을 Monte Carlo로 재현.
# 시뮬레이션도 한 회차 6개 '비복원' 추출.
rng = np.random.default_rng(20261109)
expected = 300*6/45
obs_chi = float(((freq-expected)**2/expected).sum())
sim_stats = []
for _ in range(600):
    sim=np.array([rng.choice(np.arange(1,46),size=6,replace=False) for __ in range(300)])
    ff=np.bincount(sim.ravel(),minlength=46)[1:]
    sim_stats.append(float(((ff-expected)**2/expected).sum()))
mc_p=(1+sum(x>=obs_chi for x in sim_stats))/(1+len(sim_stats))

# 시간순 백테스트: 1099~1248회 예제; 매 회차의 실제 번호는 선택 전에 절대 사용하지 않음.
# 과거 최근 60회: 단순 빈도 / 지수 가중 빈도 / 무작위 기준선(각 6개)
py_rng=random.Random(260911)
strategies={"recent_frequency":[],"exp_weighted":[],"uniform_random":[]}
for i in range(150,len(numbers)):
    past=numbers[max(0,i-60):i]
    f=np.bincount(past.ravel(),minlength=46)[1:]
    freq_pick=set(sorted(range(1,46),key=lambda n:(-f[n-1],n))[:6])
    scores=np.zeros(45,dtype=float)
    for j,d in enumerate(past):
        scores[d-1] += 0.97**(len(past)-1-j)
    weight_pick=set(sorted(range(1,46),key=lambda n:(-scores[n-1],n))[:6])
    rand_pick=set(py_rng.sample(range(1,46),6))
    truth=set(numbers[i])
    for name,pick in [("recent_frequency",freq_pick),("exp_weighted",weight_pick),("uniform_random",rand_pick)]:
        strategies[name].append(len(pick&truth))
backtest={key:{"draws":len(v),"mean_matches":round(float(np.mean(v)),6),
               "hits_ge_3":sum(x>=3 for x in v),"hits_6":sum(x==6 for x in v),
               "hist":{str(k):sum(x==k for x in v) for k in range(7)}} for key,v in strategies.items()}

# 고정된 핵심번호를 활용한 10게임 생성 방식은 확률 개선 검증이 아닌 조합 구조 설명.
# 100게임 후보 -> 분산(중복 0), 3핵심/4핵심/일부/미고정 4:2:2:2.
full_freq=sorted(range(1,46),key=lambda x:(-freq[x-1],x))
core=full_freq[:4]
comb_rng=random.Random(1248)
generated=[]
def add_ticket(pinned):
    for _ in range(3000):
        ticket=tuple(sorted(set(pinned)|set(comb_rng.sample([n for n in range(1,46) if n not in pinned],6-len(set(pinned))))))
        if len(ticket)==6 and ticket not in generated:
            generated.append(ticket)
            return
    raise RuntimeError("유일 조합 생성 실패")
for i in range(100):
    if i<40: pinned=core[:3]
    elif i<60: pinned=core[:4]
    elif i<80: pinned=core[i%4:i%4+2] if i%4<3 else core[0:2]
    else: pinned=[]
    add_ticket(pinned)
# 40/20/20/20 후보 중 다양성을 고려해 각 4/2/2/2개 샘플 추출
selected=[*generated[0:4],*generated[40:42],*generated[60:62],*generated[80:82]]
assert len(selected)==len(set(selected))==10
sample_tickets=[{"type":typ,"numbers":list(t)} for t,typ in zip(selected,
    ["핵심 3개"]*4+["핵심 4개"]*2+["일부 활용"]*2+["미고정"]*2)]

# PDF 기법 ① 로그축 vs 로그변환 / ② 이상치 IQR / ③ Standard·MinMax
q1,q3=prizes.firstWinamnt.quantile([.25,.75])
iqr=q3-q1
lower,upper=q1-1.5*iqr,q3+1.5*iqr
outliers=prizes[(prizes.firstWinamnt<lower)|(prizes.firstWinamnt>upper)]
scaler=StandardScaler().fit_transform(prizes[["firstWinamnt","totSellamnt"]])
minmax=MinMaxScaler().fit_transform(prizes[["firstWinamnt","totSellamnt"]])
log1p=np.log1p(prizes.firstWinamnt)
assert np.isfinite(log1p).all() and np.isfinite(scaler).all() and np.isfinite(minmax).all()
# PDF 기법 ④ Welch 검정: 과거 150회와 후반 150회 1등 당첨액의 평균 비교
t_stat,t_p=ttest_ind(prizes.firstWinamnt.iloc[:150],prizes.firstWinamnt.iloc[150:],equal_var=False)
# PDF 기법 ⑤ 이동평균 · 전년 동기 비교 (12회 / 12개월)
prizes["draw_rolling_12"]=prizes.totSellamnt.rolling(12).mean()
prizes["date"]=pd.to_datetime(prizes.drwNoDate)
monthly=prizes.groupby(prizes.date.dt.to_period("M")).agg(
    mean_sales=("totSellamnt","mean"),draws=("drwNo","size"))
monthly["rolling_3m"]=monthly.mean_sales.rolling(3).mean()
monthly["yoy_12m_pct"]=monthly.mean_sales.pct_change(12)*100

# PDF 기법 ⑥ 비율·10만 명당 / ⑧ 지도: 지역은 가상 데이터.
cities=pd.DataFrame([
    {"region":"가상 A시","population":10000000,"event_count":50,"tile_x":0,"tile_y":0},
    {"region":"가상 B시","population":1000000,"event_count":10,"tile_x":1,"tile_y":0},
    {"region":"가상 C시","population":2000000,"event_count":15,"tile_x":0,"tile_y":1},
    {"region":"가상 D시","population":600000,"event_count":4,"tile_x":1,"tile_y":1},
])
cities["per_100k"]=cities.event_count/cities.population*100000
cities.to_csv(DATA/"synthetic_regions.csv",index=False,encoding="utf-8-sig")

# PDF 기법 ⑦ RFM·코호트: 가상 구매 이력 생성(로또 판매·복권구매 데이터 아님)
orders=[]
for i in range(1,31):
    first=pd.Timestamp("2026-01-01")+pd.DateOffset(months=i%4)+pd.Timedelta(days=4+(i*3)%15)
    count=1+(i%3)
    for j in range(count):
        when=first+pd.Timedelta(days=34*j)
        orders.append({"customer_id":f"C{i:03d}","order_date":when.date().isoformat(),
                       "amount_krw":15000+(i*700+j*3900)%29000})
order_df=pd.DataFrame(orders)
order_df.to_csv(DATA/"synthetic_orders.csv",index=False,encoding="utf-8-sig")
order_df["order_date"]=pd.to_datetime(order_df.order_date)
snapshot=pd.Timestamp("2026-11-09")
rfm=order_df.groupby("customer_id").agg(last=("order_date","max"),
   frequency=("order_date","size"),monetary=("amount_krw","sum"))
rfm["recency_days"]=(snapshot-rfm["last"]).dt.days
first_month=order_df.groupby("customer_id").order_date.min().dt.to_period("M")
order_df=order_df.join(first_month.rename("cohort"),on="customer_id")
order_df["month_offset"]=((order_df.order_date.dt.year-order_df.cohort.dt.year)*12+
                          (order_df.order_date.dt.month-order_df.cohort.dt.month))
cohort_counts=order_df.groupby(["cohort","month_offset"]).customer_id.nunique().unstack(fill_value=0)
cohort_rates=cohort_counts.div(cohort_counts[0],axis=0).round(4)

# PDF 기법 ⑩ TF-IDF: 리뷰도 가상이며 실제 사용자 댓글·감성모델 아님.
positive=[
 "안내 친절 편리 도움 빠른 검색","설명 자세함 친절 편리 화면",
 "사용 편리 빠른 검색 안내 좋아요","친절한 안내 도움 사용 쉬움",
 "설명 간단 정확 화면 편리","검색 빠름 깔끔 화면 좋아요"]
negative=[
 "오류 멈춤 느림 화면 불편","오류 반복 멈춤 불편 검색",
 "접속 지연 느림 계속 오류","화면 멈춤 버튼 오류 불편",
 "로그인 실패 접속 오류 지연","불편 느림 오류 수정 필요"]
reviews=pd.DataFrame({"label":["긍정"]*len(positive)+["불편"]*len(negative),
                      "text":positive+negative})
reviews.to_csv(DATA/"synthetic_comments.csv",index=False,encoding="utf-8-sig")
vec=TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
tf=vec.fit_transform(reviews.text)
terms=np.asarray(vec.get_feature_names_out())
scores=np.asarray(tf[reviews.label.eq("불편").to_numpy()].mean(axis=0)).ravel()-np.asarray(
    tf[reviews.label.eq("긍정").to_numpy()].mean(axis=0)).ravel()
top_idx=np.argsort(-scores)[:6]
top_terms=[{"term":str(terms[i]),"score":round(float(scores[i]),4)} for i in top_idx]

# Figure rendering: all graphs have titles and dates; human interpretation in README.
def figsave(name):
    plt.tight_layout()
    plt.savefig(CHART/name,dpi=140,bbox_inches="tight",facecolor="white")
    plt.close()
fig,ax=plt.subplots(figsize=(12,5))
ax.bar(range(1,46),freq,color="#58a6a1");ax.axhline(expected,color="#db877d",linestyle="--",label="균등추첨 기대횟수")
ax.set(xlabel="번호 (1~45)",ylabel="등장 횟수 (회)",title="949~1248회 로또 번호 빈도 (300회)")
ax.legend();figsave("01_lotto_frequency.png")
fig,ax=plt.subplots(figsize=(8,5))
names=list(backtest);values=[backtest[k]["mean_matches"] for k in names]
ax.bar(names,values,color=["#4e9e91","#678dc9","#d5a874"])
ax.axhline(6*6/45,linestyle="--",color="#c25f5f",label="이론 기대 0.8")
ax.set(ylabel="평균 일치 번호 수",title="시간순 백테스트: 1099~1248회, 각 전략 1게임")
ax.set_ylim(0,1.3);ax.legend();figsave("02_walkforward.png")
fig,ax=plt.subplots(figsize=(9,5))
ax.hist(draw_sum,bins=16,color="#7996c5",edgecolor="white")
ax.set(xlabel="한 회차 6개 번호 합",ylabel="회차 수",title="로또 300회차 합계 분포")
figsave("03_sum_histogram.png")
fig,ax=plt.subplots(figsize=(11,5))
ax.plot(prizes.drwNo,prizes.totSellamnt/1e8,alpha=.35,label="회차별 판매액")
ax.plot(prizes.drwNo,prizes.draw_rolling_12/1e8,color="#267b85",linewidth=2,label="최근12회 이동평균")
ax.set(xlabel="회차",ylabel="판매액 (억원)",title="추첨 회차별 판매액과 12회 이동평균")
ax.legend();figsave("04_sales_rolling.png")
fig,axes=plt.subplots(1,3,figsize=(12,4))
for ax,values,title in zip(axes,[prizes.firstWinamnt/1e8,log1p,scaler[:,0]],
 ["원본(억원)","log1p(원)","StandardScaler(Z)"]):
    ax.hist(values,bins=18,color="#4e9e91",edgecolor="white");ax.set_title(title)
fig.suptitle("로그 변환은 분포를 바꾸고, 표준화는 측정 단위를 바꿈")
figsave("05_log_scaler.png")
fig,axes=plt.subplots(1,2,figsize=(10,4.5))
axes[0].bar(cities.region,cities.event_count,color="#92a8be")
axes[1].bar(cities.region,cities.per_100k,color="#e1a66d")
axes[0].set_title("가상 사건 원건수");axes[1].set_title("가상 사건 10만명당 건수")
fig.suptitle("가상 지역 4곳: 분모를 고려하면 순위가 바뀔 수 있음")
figsave("06_rate_per100k.png")
fig,ax=plt.subplots(figsize=(7,4))
ax.bar([x["term"] for x in top_terms],[x["score"] for x in top_terms],color="#7398c7")
ax.set(xlabel="불편 예제에서 상대적으로 두드러지는 단어",ylabel="평균 TF-IDF 차이",title="가상 댓글: TF-IDF 단어 특징")
figsave("07_tfidf_demo.png")
fig,ax=plt.subplots(figsize=(7,4))
heat=cohort_rates.fillna(0).to_numpy()
im=ax.imshow(heat,aspect="auto",cmap="Blues",vmin=0,vmax=1)
ax.set_yticks(range(len(cohort_rates.index)),[str(i) for i in cohort_rates.index])
ax.set_xticks(range(len(cohort_rates.columns)),cohort_rates.columns)
ax.set(xlabel="첫 구매 후 경과 월",ylabel="첫 구매 월",title="가상 고객 코호트 잔존율")
fig.colorbar(im,ax=ax,label="코호트별 해당 월 구매 비율")
figsave("08_cohort_heatmap.png")

# ⑨ Plotly: 인터넷 있는 환경에서 CDN JS 사용. 정적 GitHub Pages에 삽입 가능.
try:
    import plotly.express as px
    fig=px.scatter(prizes,x="firstPrzwnerCo",y="firstWinamnt",
        hover_data=["drwNo","drwNoDate"],title="실제 300회차: 1등 당첨자 수 vs 1등 지급액",
        labels={"firstPrzwnerCo":"1등 당첨자 수(명)","firstWinamnt":"1등 1인 지급액(원)"})
    fig.write_html(BASE/"plotly_interactive.html",include_plotlyjs="cdn",
        full_html=True)
    plotly_status="created"
except ImportError:
    plotly_status="requires plotly installation"

result={
 "meta":{"source":"user cashlogy-lotto-all.csv","sample_draws":300,"first_draw":949,
        "last_draw":1248,"last_date":"2026-10-31","not_latest":True,
        "disclaimer":"과거 특성 분석. 미래 번호 예측성능 입증 없음."},
 "frequency":{"all":freq.tolist(),"last60":recent60.tolist(),"top6":hot,
              "bottom6":cold,"expected_per_number":expected},
 "patterns":{"mean_sum":round(float(draw_sum.mean()),4),
             "odd_mean":round(float(odd_counts.mean()),4),
             "low_1_22_mean":round(float(low_counts.mean()),4),
             "multiples3_mean":round(float(multiples3.mean()),4),
             "at_least_one_consecutive_count":sum(x>0 for x in consecutive),
             "at_least_one_consecutive_pct":round(100*np.mean(np.array(consecutive)>0),3),
             "theory_consecutive_pct":round(100*consecutive_theory,3),
             "last_digit_counts":end_digits.tolist(),
             "top_pairs":[{"pair":[int(n) for n in k],"count":int(v)} for k,v in pair_counter.most_common(8)]},
 "probability":{"combination_total":comb(45,6),"first_prize_probability":1/comb(45,6),
                "expected_matches":6*6/45,"match_distribution":theory,
                "mc_stat":round(obs_chi,4),"monte_carlo_simulations":600,
                "mc_pvalue":round(mc_p,5)},
 "backtest":{"train_min":150,"test_first_draw":1099,"test_last_draw":1248,
             "window":60,"strategies":backtest},
 "sample_tickets":{"candidate_count":100,"tickets":sample_tickets,
                   "not_prediction":True,"fixed_core":core},
 "pdf_extra10":{
   "iqr_prize":{"q1":float(q1),"q3":float(q3),"lower":float(lower),
                "upper":float(upper),"candidate_count":len(outliers)},
   "standard_scaler":{"mean_approx":[round(float(v),7) for v in scaler.mean(axis=0)],
                      "minmax_range":[round(float(v),4) for v in [minmax.min(),minmax.max()]]},
   "welch_prize_first150_vs_last150":{"t":round(float(t_stat),5),
                                      "p":round(float(t_p),6)},
   "monthly_yoy":{"latest_month":str(monthly.index[-1]),
                  "pct_vs_same_month_last_year":round(float(monthly.iloc[-1].yoy_12m_pct),4),
                  "latest_month_mean_sales":round(float(monthly.iloc[-1].mean_sales),2)},
   "rate_per100k_synthetic":cities[["region","event_count","population","per_100k"]].to_dict("records"),
   "rfm_synthetic":{"customers":len(rfm),"orders":len(order_df),
                    "one_purchase_customers":int((rfm.frequency==1).sum()),
                    "average_days_since_last":round(float(rfm.recency_days.mean()),2)},
   "cohort_synthetic":{"cohorts":len(cohort_rates.index),
                       "month_0_retention":1.0},
   "tfidf_synthetic":{"documents":len(reviews),"negative_distinctive":top_terms},
   "plotly":plotly_status
 }
}
(DATA/"analysis_results.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"meta":result["meta"],"patterns":result["patterns"],
  "probability":result["probability"],"backtest":result["backtest"],
  "pdf_extra10":result["pdf_extra10"]},ensure_ascii=False,indent=2))
print("LOTTO_PDF_10_TECHNIQUES_REPRODUCED")
