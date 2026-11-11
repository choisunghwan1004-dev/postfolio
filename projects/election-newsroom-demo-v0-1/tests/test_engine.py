import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from engine import REGIONS,generate,evolve,aggregate,snapshot,evidence_for,draft_from_evidence,validate_draft

def test_17_regions_and_254_districts():
    ds=generate();assert len(REGIONS)==17;assert len(ds)==254;assert len({d['id'] for d in ds})==254

def test_deterministic_seed():
    assert generate(1122)==generate(1122)
    assert generate(1122)!=generate(3344)

def test_sum_consistency():
    ds=generate();s=snapshot(ds,0,123);assert s['national']['counted']==sum(d['counted'] for d in ds)
    assert sum(s['national']['votes'])==s['national']['counted']
    assert sum(r['counted'] for r in s['regions'])==s['national']['counted']
    for d in ds:assert sum(d['votes'])==d['counted'] and d['counted']<=d['target_votes']

def test_increment_no_decrease_and_caps():
    ds=generate();before=[d['counted'] for d in ds];changes=evolve(ds,20261111,1)
    assert changes and all(d['counted']>=v and d['counted']<=d['target_votes'] for d,v in zip(ds,before))
    assert all(sum(d['votes'])==d['counted'] for d in ds)

def test_evidence_scopes():
    ds=generate();s=snapshot(ds,0,123)
    assert evidence_for(s,'national')['id']=='SIM-N-S0'
    assert evidence_for(s,'region',region='서울')['id']=='SIM-R-서울-S0'
    assert evidence_for(s,'district',district_id='제주-001')['id']=='SIM-D-제주-001-S0'

def test_missing_district_rejected():
    ds=generate();s=snapshot(ds,0,123)
    try:evidence_for(s,'district',district_id='XX-111');assert False
    except ValueError:pass

def test_draft_evidence_valid():
    ds=generate();e=evidence_for(snapshot(ds,0,123),'national')
    txt=draft_from_evidence(e);assert validate_draft(txt,e)['passed'];assert '실제 선거 결과가 아닙니다' in txt

def test_fake_id_blocks_approval():
    e=evidence_for(snapshot(generate(),0,123))
    bad=draft_from_evidence(e).replace(e['id'],'FAKE-ID')
    assert not validate_draft(bad,e)['passed']

def test_wrong_region_blocks_approval():
    e=evidence_for(snapshot(generate(),0,123),'region',region='서울')
    bad=draft_from_evidence(e).replace('서울특별시','부산광역시')
    assert not validate_draft(bad,e)['passed']

def test_modified_number_blocks_approval():
    e=evidence_for(snapshot(generate(),0,123))
    bad=draft_from_evidence(e).replace('표','표 ',1)
    assert not validate_draft(bad,e)['passed']
