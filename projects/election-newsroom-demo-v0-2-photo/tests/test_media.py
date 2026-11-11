from pathlib import Path
import json, csv
from fastapi.testclient import TestClient
from server import app
ROOT=Path(__file__).resolve().parents[1]

def test_gallery_and_rights():
    items=json.loads((ROOT/'static/media/media_manifest.json').read_text(encoding='utf-8'))
    assert len(items)==3
    assert sum(x['kind']=='photo' for x in items)==1
    assert not any(x['kind']=='video' for x in items)
    assert all((ROOT/'static/media'/x['filename']).is_file() for x in items)
    assert all(x.get('source') and x.get('rights') and x.get('approved_for') for x in items)
    assert next(x for x in items if x['kind']=='photo')['ai_generated'] is True

def test_new_view_preserves_original():
    h=(ROOT/'static/index.html').read_text(encoding='utf-8')
    assert 'data-view="dashboard"' in h and 'data-view="district"' in h
    assert 'data-view="articles"' in h and 'data-view="studio"' in h
    assert 'data-view="media"' in h and 'id="view-media"' in h
    assert '교육용 모의 개표' in h and '실제 선거 아님' in h

def test_web_media_routes():
    with TestClient(app) as c:
        assert c.get('/').status_code==200
        assert c.get('/static/media/studio_photo.jpg').headers['content-type'].startswith('image/jpeg')
        assert c.get('/static/media/fictional_election_intro_1080p.mp4').status_code==404
        assert c.get('/static/docs/20minute_storyboard.csv').status_code==200
        assert c.get('/api/snapshot').json()['national']['districts']==254

def test_storyboard_20_minutes_and_watermark():
    with (ROOT/'static/docs/20minute_storyboard.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    assert len(rows)==9
    def minute(t):return 60*int(t[:2])+int(t[3:])
    assert minute(rows[0]['시작'])==0
    assert minute(rows[-1]['종료'])==20*60
    assert all(minute(x['종료'])>minute(x['시작']) for x in rows)
    assert any('교육용 표시' in x['검수 확인'] for x in rows)

def test_video_is_deferred_and_media_rights_ledger_is_photo_only():
    html=(ROOT/'static/index.html').read_text(encoding='utf-8')
    assert '영상은 아직 제작하지 않습니다' in html
    assert 'id="view-media"' in html
    assert not (ROOT/'static/media/fictional_election_intro_1080p.mp4').exists()
    with (ROOT/'static/docs/media_rights_ledger.csv').open(encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==3
    assert not any(r['ID'].startswith('VIDEO') for r in rows)
    assert all(r['SHA-256'] for r in rows)
