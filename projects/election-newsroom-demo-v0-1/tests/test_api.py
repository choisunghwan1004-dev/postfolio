import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from fastapi.testclient import TestClient
from server import app,state

def test_home_and_snapshot():
    with TestClient(app) as c:
        res=c.get('/');assert res.status_code==200;assert '교육용 모의 개표' in res.text
        obj=c.get('/api/snapshot').json();assert len(obj['districts'])==254

def test_websocket_live_update_and_pause_resume():
    with TestClient(app) as c:
        with c.websocket_connect('/ws') as ws:
            first=ws.receive_json();assert first['type']=='snapshot'
            x=c.post('/api/control',json={'action':'tick'});assert x.status_code==200
            next=ws.receive_json();assert next['data']['step']==first['data']['step']+1
        assert c.post('/api/control',json={'action':'pause'}).status_code==200
        assert c.post('/api/control',json={'action':'resume'}).status_code==200

def test_article_review_and_blocking():
    with TestClient(app) as c:
        a=c.post('/api/articles/draft',json={'scope':'district','district_id':'서울-001'}).json()
        assert a['validation']['passed']
        bad=c.post(f"/api/articles/{a['id']}/review",json={'approve':True,'reason':'대조','revised_text':'근거 없는 가짜 서울 뉴스'})
        assert bad.status_code==409
        assert c.get('/api/articles').json()[0]['status']=='review_required'
        good=c.post(f"/api/articles/{a['id']}/review",json={'approve':True,'reason':'근거 ID·숫자 대조 완료','revised_text':a['text']})
        assert good.status_code==200;assert good.json()['status']=='approved'
        assert c.get('/api/audit').json()[0]['action']=='APPROVED'

def test_no_approval_without_reason():
    with TestClient(app) as c:
        a=c.post('/api/articles/draft',json={'scope':'national'}).json()
        assert c.post(f"/api/articles/{a['id']}/review",json={'approve':True,'reason':''}).status_code==400

def test_reset():
    with TestClient(app) as c:
        c.post('/api/control',json={'action':'tick'})
        res=c.post('/api/control',json={'action':'reset','seed':20261111})
        assert res.status_code==200
        assert c.get('/api/snapshot').json()['step']==0

def test_lexical_rag_sources_and_no_evidence():
    with TestClient(app) as c:
        x=c.get('/api/rag/search',params={'question':'기사 승인 조건'}).json()
        assert x['mode']=='offline_lexical_evidence_search'
        assert x['count']>=1 and all(r['id'].startswith('DEMO-G') for r in x['results'])
        unknown=c.get('/api/rag/search',params={'question':'외계 달 탐사'}).json()
        assert unknown['count']==0

def test_export_csv_is_labeled_as_mock():
    with TestClient(app) as c:
        res=c.get('/api/export/districts.csv')
        assert res.status_code==200
        assert 'SIMULATION_ONLY' in res.text
        assert '서울-001' in res.text
        assert len(res.text.splitlines())==255
