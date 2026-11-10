"""Coursework: chart grammar and reproducible data journalism.
Sources: user-provided teaching PDFs for METHODS ONLY, synthetic news/PM10 data;
user-provided historical Lotto CSV for numeric comparisons (past not prediction).
Run: python run_analysis.py. Outputs CSV, JSON, before/after PNG+SVG charts.
"""
from pathlib import Path
from datetime import datetime
import json
import re
import math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

BASE = Path(__file__).resolve().parent
DATA = BASE/'data'
CHARTS=BASE/'charts'
DATA.mkdir(exist_ok=True); CHARTS.mkdir(exist_ok=True)
FONT='NanumBarunGothic'
if not any(FONT in f.name for f in font_manager.fontManager.ttflist): FONT='DejaVu Sans'
plt.rcParams.update({'font.family':FONT,'axes.unicode_minus':False,'font.size':11,
                     'figure.dpi':150,'savefig.facecolor':'white', 'svg.fonttype':'none'})
TEAL='#207e77'; ORANGE='#df8c4a'; BLUE='#5682be'; GRAY='#b1bec5'; DARK='#273e49'

# Synthetic data intentionally kept separate from actual measurement/article datasets.
rng=np.random.default_rng(20261110)
dates=pd.date_range('2026-08-01',periods=85,freq='D')
news_counts=rng.poisson(4.5,size=len(dates)).astype(int)
pm10=np.clip(np.rint(40+rng.normal(0,13,len(dates))),9,105).astype(int)
# Contrasting extremes deliberately created for training, NOT real events.
news_overrides={5:0,14:0,22:1,27:0,41:47,58:2,68:52,72:1}
pm10_overrides={41:21,58:127,68:18,72:116}
for i,v in news_overrides.items():news_counts[i]=v
for i,v in pm10_overrides.items():pm10[i]=v
news_articles=[]
for i,d in enumerate(dates):
    for k in range(int(news_counts[i])):
        news_articles.append({'news_id':f'SYN-{i:03d}-{k+1:03d}', 'day':d.strftime('%Y-%m-%d'),
                            'headline':f'[가상 기사] 대기질 관련 소식 {i+1}일차 {k+1}번'})
news=pd.DataFrame(news_articles)
news.to_csv(DATA/'synthetic_news_articles.csv',index=False,encoding='utf-8-sig')
air=pd.DataFrame({'day':dates.strftime('%Y-%m-%d'),'pm10_ug_m3':pm10})
air.to_csv(DATA/'synthetic_pm10_daily.csv',index=False,encoding='utf-8-sig')
# Article rows grouped by exact date and left-merged to retain every measurement day.
news_daily=news.groupby('day',as_index=False).size().rename(columns={'size':'news_count'})
joined=air.merge(news_daily,on='day',how='left',validate='one_to_one')
joined.news_count=joined.news_count.fillna(0).astype(int)
assert len(joined)==len(air)==85
assert joined.news_count.sum()==len(news)
assert (joined.day==air.day).all()
joined.to_csv(DATA/'synthetic_news_pm10_joined.csv',index=False,encoding='utf-8-sig')
r=float(joined.news_count.corr(joined.pm10_ug_m3))
low=joined.pm10_ug_m3 < joined.pm10_ug_m3.median()
heavy=joined.news_count > joined.news_count.quantile(.9)
mislead=joined.loc[low&heavy].sort_values('news_count',ascending=False)
q1,q3=joined.pm10_ug_m3.quantile([.25,.75]);iqr=q3-q1
upper=float(q3+1.5*iqr)
high_pm_low_news=joined[(joined.pm10_ug_m3>upper)&(joined.news_count<joined.news_count.median())]

# Historical Lotto only: 949~1248. Use local original archive solely for reproducibility.
original=DATA/'lotto_949_1248_sample.csv'
if not original.exists():
    raise FileNotFoundError('data/lotto_949_1248_sample.csv is needed for reproducibility')
draws=pd.read_csv(original)
cols=['drwNo','drwNoDate','n1','n2','n3','n4','n5','n6','bonus']
assert set(cols).issubset(draws.columns)
draws=draws.loc[(draws.drwNo>=949)&(draws.drwNo<=1248),cols].sort_values('drwNo').reset_index(drop=True)
assert draws.drwNo.tolist()==list(range(949,1249))
nums=draws[[f'n{i}' for i in range(1,7)]].to_numpy(int)
assert all(len(set(row))==6 for row in nums) and nums.min()>=1 and nums.max()<=45
selected=draws.tail(60)
freq=pd.Series(selected[[f'n{i}' for i in range(1,7)]].to_numpy().ravel()).value_counts().reindex(range(1,46),fill_value=0)
top4=freq.sort_values(ascending=False,kind='stable').head(4)
# Walk-forward sample results are recomputed from prior 60 draws with a seeded independent baseline.
import random
rr=random.Random(260911)
strategies={'최근 60회 빈도':[],'지수가중 빈도':[],'무작위 기준선':[]}
for i in range(150,len(nums)):
    past=nums[i-60:i]
    ff=np.bincount(past.ravel(),minlength=46)[1:]
    score=np.zeros(45)
    for j,row in enumerate(past):score[row-1]+=0.97**(len(past)-1-j)
    picks=[set(sorted(range(1,46),key=lambda n:(-ff[n-1],n))[:6]),set(sorted(range(1,46),key=lambda n:(-score[n-1],n))[:6]),set(rr.sample(range(1,46),6))]
    for key,p in zip(strategies,picks):strategies[key].append(len(p&set(nums[i])))
means={k:round(float(np.mean(v)),4) for k,v in strategies.items()}
assert all(len(x)==150 for x in strategies.values())

# Chart-grammar examples: each BEFORE is a deliberately misleading training chart.
def finish(name):
    plt.savefig(CHARTS/(name+'.png'),dpi=170,bbox_inches='tight',pad_inches=.19)
    plt.savefig(CHARTS/(name+'.svg'),bbox_inches='tight',pad_inches=.19)
    plt.close()

def source(fig,source,kind='교육용 차트'):
    fig.text(.02,.016,f'{kind}  |  {source}  |  출처·기간·단위 표기 확인',fontsize=9,color='#526c70')

# 1 BAR AXIS trap: truncated vs zero baseline.
labels=[f'{n}번' for n in top4.index]; values=top4.to_numpy()
fig,ax=plt.subplots(figsize=(9,5)); ax.bar(labels,values,color=[ORANGE,BLUE,'#43a891','#8560ae'])
ax.set_ylim(max(0,min(values)-1),max(values)+1);ax.set_title('수업용 잘못된 차트: 0에서 시작하지 않는 막대',loc='left',fontsize=17)
ax.set_ylabel('등장 횟수 (회)')
for i,v in enumerate(values):ax.text(i,v+.07,str(v),ha='center')
source(fig,'로또 6/45 1189~1248회 · 60회차 · 위 사례는 의도된 과장','수정 전 / 실제 과거 데이터')
finish('01_before_truncated_axis')
fig,ax=plt.subplots(figsize=(9,5));ax.bar(labels,values,color=[ORANGE]+[GRAY]*3)
ax.set_ylim(0,max(values)*1.22);ax.set_title(f'최근 60회에는 {labels[0]}이 {values[0]}회로 가장 많았다',loc='left',fontsize=17)
ax.set_ylabel('등장 횟수 (회)');ax.set_xlabel('로또 번호');
for i,v in enumerate(values):ax.text(i,v+.12,str(v),ha='center')
source(fig,'사용자 제공 로또 기록 1189~1248회 · 단위 회 · 당첨확률 변화 아님','수정 후 / 실제 과거 데이터')
finish('01_after_zero_axis')

# 2 DOUBLE AXIS trap vs aligned two-panel chart using synthetic news/PM10.
fig,ax=plt.subplots(figsize=(10,5))
ax.plot(joined.day,joined.news_count,color=ORANGE,lw=2,label='가상 기사 수')
twin=ax.twinx();twin.plot(joined.day,joined.pm10_ug_m3,color=BLUE,lw=1.8,label='가상 PM10')
ax.set_ylabel('기사 수(건)');twin.set_ylabel('PM10(㎍/㎥)');
ax.set_xticks(np.arange(0,85,14));ax.set_xticklabels(joined.day.iloc[::14],rotation=32)
ax.set_title('수업용 잘못된 차트: 이중축 겹침은 착시를 유발',loc='left',fontsize=17)
source(fig,'가상 뉴스/PM10 2026-08-01~2026-10-24 · 양쪽 축은 임의 배율','수정 전 / 가상 데이터')
finish('02_before_dual_axis')
fig,axes=plt.subplots(2,1,figsize=(10,6.5),sharex=True)
axes[0].bar(np.arange(85),joined.news_count,color=ORANGE,width=.9);axes[0].set_ylabel('기사 수(건)');axes[0].set_ylim(bottom=0)
axes[1].plot(np.arange(85),joined.pm10_ug_m3,color=BLUE,lw=1.7);axes[1].set_ylabel('PM10(㎍/㎥)');axes[1].set_ylim(bottom=0)
axes[1].set_xticks(np.arange(0,85,14));axes[1].set_xticklabels(joined.day.iloc[::14],rotation=24)
fig.suptitle('가상 보도량 급증과 미세먼지 상승은 항상 겹치지 않는다',fontsize=17,x=.04,y=.98,ha='left')
source(fig,'가상 뉴스 수집 표 + 가상 PM10 표 · 2026-08-01~10-24 · 같은 날짜축 사용','수정 후 / 가상 데이터')
fig.subplots_adjust(hspace=.16,top=.89,bottom=.17)
finish('02_after_shared_dates')

# 3 highlight scatter trap: multi colors vs one highlight, with zero baseline and exact labels.
names=list(means); y=list(means.values())
fig,ax=plt.subplots(figsize=(9,5))
ax.bar(names,y,color=['#ec666b','#60a7cd','#d6b04d']);ax.set_ylim(.55,1.0)
ax.set_ylabel('평균 일치 번호 수 (개)');ax.set_title('수업용 잘못된 차트: 축 절단 + 산만한 색',loc='left',fontsize=17)
source(fig,'로또 역사 1099~1248회 · 동일 회차 150개 · 축 일부 생략','수정 전 / 실제 과거 데이터')
finish('03_before_unfocused')
fig,ax=plt.subplots(figsize=(9,5))
ax.bar(names,y,color=[GRAY,GRAY,ORANGE]);ax.set_ylim(0,1.1)
for i,v in enumerate(y):ax.text(i,v+.035,f'{v:.3f}개',ha='center',fontsize=12)
ax.axhline(.8,color=BLUE,ls='--',label='균등추첨 이론 기대 0.8개')
ax.legend(loc='upper right');ax.set_ylabel('회차별 평균 일치 번호 수 (개)')
ax.set_title('이번 150회 시험에서는 무작위 기준선의 평균 일치수가 더 컸다',loc='left',fontsize=16)
source(fig,'사용자 로또 기록 1099~1248회 / 과거60회 학습 · 기준선 1게임/회차 · 미래 예측 아님','수정 후 / 실제 과거 데이터')
finish('03_after_one_highlight')

# Additional chart types from 'Data Visualization at a Glance' pp.3-4: scatter and heatmap.
fig,ax=plt.subplots(figsize=(9,5));ax.scatter(joined.pm10_ug_m3,joined.news_count,color=TEAL,alpha=.75,s=43)
for row in mislead.head(2).itertuples():
    ax.annotate(row.day[5:],(row.pm10_ug_m3,row.news_count),xytext=(6,6),textcoords='offset points')
ax.set(xlabel='가상 PM10 일평균 (㎍/㎥)',ylabel='가상 미세먼지 기사 수(건)')
ax.set_xlim(left=0);ax.set_ylim(bottom=0);ax.set_title(f'가상 뉴스량과 PM10 관계: 피어슨 r={r:+.2f}',loc='left',fontsize=17)
source(fig,'합성 뉴스·측정표 날짜 병합 / 2026-08-01~10-24 / 원인 해석 금지','관계 / 산점도, 가상 데이터')
finish('04_scatter_relationship')

from collections import Counter
odd=np.sum(nums%2==1,axis=1)
consec=np.array([int(any(b-a==1 for a,b in zip(sorted(row),sorted(row)[1:]))) for row in nums])
mat=np.zeros((7,2),dtype=int)
for n,c in zip(odd,consec):mat[n,c]+=1
fig,ax=plt.subplots(figsize=(8,5));heat=ax.imshow(mat,aspect='auto',cmap='Blues')
ax.set_xticks([0,1],['연속 없음','연속 있음']);ax.set_yticks(range(7),[str(i)+'개' for i in range(7)])
ax.set_xlabel('연속번호 포함 여부');ax.set_ylabel('홀수 번호 개수')
for i in range(7):
    for j in range(2):ax.text(j,i,str(mat[i,j]),ha='center',va='center',color='white' if mat[i,j]>mat.max()*.54 else DARK)
ax.set_title('실제 300회차의 홀수 개수·연속번호 분포',loc='left',fontsize=17)
source(fig,'사용자 로또 기록 949~1248회 / 단위 회차 수 · 과거 기술통계일 뿐','분포 / 히트맵, 실제 과거 데이터')
finish('05_heatmap_lotto')

checks={
 'lotto_rows':len(draws),'lotto_first':int(draws.drwNo.min()),'lotto_last':int(draws.drwNo.max()),
 'lotto_last_date':str(draws.drwNoDate.iloc[-1]),'recent60_top4':{str(k):int(v) for k,v in top4.items()},
 'backtest_means':means,'theory_mean_matches':.8,
 'synthetic_days':len(joined),'synthetic_news_article_rows':len(news),
 'synthetic_zero_news_days':int((joined.news_count==0).sum()),
 'synthetic_corr_news_pm10':round(r,6),'synthetic_lowpm_highnews':mislead[['day','pm10_ug_m3','news_count']].to_dict(orient='records'),
 'synthetic_highpm_lownews':high_pm_low_news[['day','pm10_ug_m3','news_count']].to_dict(orient='records'),
 'synthetic_pm10_iqr_upper':upper,
 'pdf_techniques_source':'데이터 분석 기법 더하기.pdf 14p / existing Lotto methods',
 'chart_rules_source':'빅데이터와 저널리즘 · 기사용 차트 문법 20p / 데이터 시각화 한눈에 보기 12p',
 'ai_disclosure':'AI 작성·수정 보조. 언론 보도에 사용 전 원래 출처를 기자가 확인',
 'is_synthetic_news':True,'is_synthetic_pm10':True,
 'charts':sorted([x.name for x in CHARTS.glob('*.png')])
}
(DATA/'analysis_results.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
assert len(checks['charts'])==8
assert any(x['news_count']>40 for x in checks['synthetic_lowpm_highnews'])
assert r<.5
print(json.dumps(checks,ensure_ascii=False,indent=2))
print('CHART_JOURNALISM_ASSIGNMENT_PASS')