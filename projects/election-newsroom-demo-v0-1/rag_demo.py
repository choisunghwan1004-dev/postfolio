"""Local lexical evidence search. Not embedding RAG / LangChain / external LLM."""
import json, re
from pathlib import Path
DATA=Path(__file__).parent/'data'/'mock_documents.json'

def load_documents():
    records=json.loads(DATA.read_text(encoding='utf-8'))
    if len({x['id'] for x in records})!=len(records):raise ValueError('중복 근거 ID')
    return records

def search_documents(question, k=3):
    if not question.strip():raise ValueError('질문 입력 필요')
    if not 1<=k<=10:raise ValueError('검색 건수 1~10')
    parts=re.findall(r'[가-힣a-zA-Z0-9]{2,}',question.lower())
    stop={'어떻게','무엇을','어떤','해줘','있는','인가요','대한','할까','어디','얼마','무슨'}
    words=[p for p in parts if p not in stop]
    if not words:return []
    ranked=[]
    for doc in load_documents():
        title=doc['title'].lower(); body=doc['text'].lower(); score=sum((3 if w in title else 0)+(1 if w in body else 0) for w in words)
        if score>0:ranked.append((score,doc['id'],doc))
    return [x[2] for x in sorted(ranked,key=lambda x:(-x[0],x[1]))[:k]]
