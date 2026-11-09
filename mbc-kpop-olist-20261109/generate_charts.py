"""Olist GitHub 사실표(F08 F14 F23 F24 F25 F27)에서 재현 가능한 과제 차트 4종.
K-pop GitHub 접근 오류 시 실제 데이터가 있는 척하지 않고 관련 차트를 생성하지 않는다.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

BASE=Path(__file__).resolve().parent
OUT=BASE/'charts'
OUT.mkdir(exist_ok=True)
FONT = next((f for f in ['NanumSquare','Noto Sans CJK KR','Malgun Gothic','UnDotum'] if f in {a.name for a in font_manager.fontManager.ttflist}), 'DejaVu Sans')
plt.rcParams.update({'font.family':FONT,'axes.unicode_minus':False,'font.size':12,'figure.facecolor':'white','axes.spines.top':False,'axes.spines.right':False})


def draw():
    f=pd.read_csv(BASE/'data/olist_verified_facts.csv')
    assert len(f)==14 and f['source_id'].isin(['F14','F23','F24','F25','F08','F27']).all()
    outputs=[]
    def save(fig,name):
        fig.tight_layout(pad=2.1)
        p=OUT/name
        fig.savefig(p,dpi=170,facecolor='white',bbox_inches='tight')
        plt.close(fig)
        outputs.append(p)
    x=f[f.topic=='배송과 리뷰']
    fig,ax=plt.subplots(figsize=(9.6,5.4))
    ax.bar(x.group,x.value,color=['#48a99e','#dc7b73'],width=.56)
    ax.set_ylim(0,5)
    ax.set_ylabel('평균 리뷰 점수 (5점 만점)')
    ax.set_title('01 | 배송 지연과 리뷰 점수 비교',fontsize=20,fontweight='bold',loc='left',pad=17)
    for i,v in enumerate(x.value):ax.text(i,float(v)+.12,f'{v:.2f}점',ha='center',fontweight='bold',fontsize=16)
    ax.text(.02,-.16,'질문: 늦게 도착한 주문의 평점은 얼마나 낮은가?',transform=ax.transAxes,fontsize=12,color='#40526b')
    ax.text(.02,-.25,'결과: 늦게 도착한 주문의 평균 평점은 1.73점 낮다. (관계만 확인, 원인 단정 금지)',transform=ax.transAxes,fontsize=11,color='#40526b')
    ax.text(.02,-.34,'출처: journal-izm/Olist-Data-Analysis · 사실표 F14 · 배송 완료 주문',transform=ax.transAxes,fontsize=9,color='#75849a')
    save(fig,'01_배송과_리뷰.png')

    m=f[f.topic=='감성분석 모델 정확도']
    fig,ax=plt.subplots(figsize=(10.5,5.7))
    idx=np.arange(len(m));vs=m.value.to_numpy()*100
    ax.bar(idx,vs,color=['#aab5c4','#6084ba','#3ca49b','#a07dc7'],width=.68)
    ax.set_xticks(idx,['전부 긍정','TF-IDF·LR','Bigram·LR','Embedding 평균'],rotation=0)
    ax.set_ylim(0,105)
    ax.set_ylabel('테스트 정확도 (%)')
    ax.set_title('02 | 감성분석 기준선과 모델 정확도',fontsize=20,fontweight='bold',loc='left',pad=17)
    for i,v in enumerate(vs):ax.text(i,v+1.8,f'{v:.1f}%',ha='center',fontweight='bold')
    ax.text(.02,-.18,'질문: 복잡한 딥러닝이 항상 더 정확한가?',transform=ax.transAxes,fontsize=12,color='#40526b')
    ax.text(.02,-.27,'결과: Bigram 머신러닝 92.6%, Embedding 평균 92.4%로 차이는 0.2%p였다.',transform=ax.transAxes,fontsize=11,color='#40526b')
    ax.text(.02,-.36,'출처: 사실표 F23·F24·F25 · 동일 테스트 리뷰 7,428건',transform=ax.transAxes,fontsize=9,color='#75849a')
    save(fig,'02_감성분석_모델비교.png')

    s=f[f.topic=='지역별 주문 비중']
    fig,ax=plt.subplots(figsize=(9.6,5.4))
    ax.barh(s.group[::-1],s.value[::-1],color=['#aebbd0','#82b9c4','#5687bc','#386cac'])
    ax.set_xlim(0,50)
    ax.set_xlabel('배송 완료 주문 비중 (%)')
    ax.set_title('03 | 주문은 어느 지역에 집중되는가?',fontsize=20,fontweight='bold',loc='left',pad=17)
    for i,v in enumerate(s.value[::-1]):ax.text(float(v)+.9,i,f'{float(v):.1f}%',va='center',fontweight='bold')
    ax.text(.02,-.19,'질문: 상파울루·리우·미나스제라이스에 주문이 얼마나 집중되는가?',transform=ax.transAxes,fontsize=12,color='#40526b')
    ax.text(.02,-.29,'결과: 상위 3개 주가 주문의 66.6%를 차지한다.',transform=ax.transAxes,fontsize=11,color='#40526b')
    ax.text(.02,-.39,'출처: 사실표 F08 · 2017-01~2018-08 배송 완료 주문 · 그 외=100%-합계',transform=ax.transAxes,fontsize=9,color='#75849a')
    save(fig,'03_지역별_주문비중.png')

    seg=f[f.topic=='판매자 군집']
    fig,ax=plt.subplots(figsize=(9.6,5.4))
    ax.bar(seg.group,seg.value,color=['#4ca5a0','#5980c9','#a1aac1','#de8274'],width=.64)
    ax.set_ylim(0,1150)
    ax.set_ylabel('판매자 수 (명)')
    ax.set_title('04 | 판매자 2,502명은 어떤 유형인가?',fontsize=20,fontweight='bold',loc='left',pad=17)
    for i,v in enumerate(seg.value):ax.text(i,float(v)+24,f'{int(v):,}명',ha='center',fontweight='bold')
    ax.text(.02,-.18,'질문: 판매자 중 가장 큰 집단은 무엇인가?',transform=ax.transAxes,fontsize=12,color='#40526b')
    ax.text(.02,-.27,'결과: 신규 성장 판매자 947명이 가장 많고, 저평점 위험 판매자는 218명이다.',transform=ax.transAxes,fontsize=11,color='#40526b')
    ax.text(.02,-.36,'출처: 사실표 F27 · 기준일 2018-06-01 이전 판매 기록',transform=ax.transAxes,fontsize=9,color='#75849a')
    save(fig,'04_판매자_유형.png')
    return outputs

if __name__=='__main__':
    for f in draw():print('CREATED',f,f.stat().st_size)
