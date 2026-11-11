"""Small PUBLIC demo with human-identified evidence mappings, not vector search/LLM."""
from pathlib import Path
import csv,json,re
BASE=Path(__file__).resolve().parent
UNKNOWN='제공된 자료로는 확인할 수 없습니다.'
QUESTIONS=[('늦은 주문의 리뷰 점수?','F14','ABC'),('재구매 비율?','F07','ABC'),('이탈 모델의 변수 개수?','M09','BC'),('3일 이상 배송 지연 보상?','R06','C'),('2019년 전체 매출?','', '')]

def load_data():
    with (BASE/'data'/'facts_sample.csv').open(encoding='utf-8-sig',newline='') as f:
        facts={row['id']:row['text'] for row in csv.DictReader(f)}
    models=(BASE/'data'/'models_sample.md').read_text(encoding='utf-8')
    policy=(BASE/'data'/'policy_sample.txt').read_text(encoding='utf-8')
    return {'F14':facts['F14'],'F07':facts['F07'],'M09':models.splitlines()[1],'R06':policy.splitlines()[1]}

def compare():
    evidence=load_data()
    rows=[]
    for question,key,allowed in QUESTIONS:
        for channel in 'ABC':
            found=[key] if key and channel in allowed else []
            answer=f'{evidence[key]} [{key}]' if found else UNKNOWN
            rows.append({'question':question,'channel':channel,'found_ids':found,'answer':answer,'mode':'human-mapped sample; not LangChain or LLM'})
    return rows

if __name__=='__main__':
    print(json.dumps(compare(),ensure_ascii=False,indent=2))
