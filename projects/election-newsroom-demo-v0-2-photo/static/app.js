(() => {
'use strict';
const $=s=>document.querySelector(s);
const $$=s=>[...document.querySelectorAll(s)];
const fmt=n=>Number(n||0).toLocaleString('ko-KR');
const pct=n=>Number(n||0).toFixed(1);
const colors=['#42cbe7','#ffb15e','#f47a9f'];
const candidates=['모의 후보 A','모의 후보 B','모의 후보 C'];
const escapeHtml=t=>String(t??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let current=null, selectedRegion='',selectedDistrict='서울-001',view='dashboard',article=null,ws=null,lastToast=0;
function toast(msg){const t=$('#toast');t.textContent=msg;t.classList.add('show');lastToast=Date.now();setTimeout(()=>{if(Date.now()-lastToast>=2400)t.classList.remove('show')},2600)}
async function request(url, options){const r=await fetch(url,{headers:{'Content-Type':'application/json'},...options});let json;try{json=await r.json()}catch{throw new Error('서버 응답 오류')};if(!r.ok)throw new Error(typeof json.detail==='string'?json.detail:JSON.stringify(json.detail||'요청 실패'));return json}
function showView(name){view=name;$$('.view').forEach(n=>n.classList.toggle('active',n.id==='view-'+name));$$('.nav').forEach(n=>n.classList.toggle('active',n.dataset.view===name));if(name==='articles')refreshAudit();if(current)render();window.scrollTo({top:0,behavior:'smooth'})}
function chooseRegion(r){selectedRegion=r;const first=current?.districts.find(d=>!r||d.region===r);if(first)selectedDistrict=first.id;$('#regionSelect').value=r;renderDistrictList();showView('district')}
function chooseDistrict(id){selectedDistrict=id;showView('district')}
const progressHtml=(v,max=100)=>`<div class="track"><div style="width:${Math.max(0,Math.min(100,v/max*100))}%;background:${colors[0]}"></div></div>`;
function votesHtml(votes,total,prefix=''){return candidates.map((name,i)=>{let v=votes[i]||0,share=total?100*v/total:0;return `<div class="candidate-row"><div class="candidate-top"><div class="candidate-name"><span class="candidate-dot" style="background:${colors[i]}"></span>${name}</div><div class="candidate-score">${pct(share)}% <small>${fmt(v)}표</small></div></div><div class="track"><div style="width:${share}%;background:${colors[i]}"></div></div></div>`}).join('')}
function summary(){if(!current)return;const n=current.national;$('#metricProgress').innerHTML=n.progress_pct.toFixed(2)+'<em>%</em>';$('#progressFill').style.width=n.progress_pct+'%';$('#metricCounted').textContent=fmt(n.counted);$('#metricLeader').textContent=n.leader;$('#metricLead').textContent=`2위와 ${fmt(n.lead_votes)}표 차이`;
$('#metricProgressSub').textContent=n.districts+'개 모의 선거구';$('#nationalUpdated').textContent='기준 시각 '+current.updated_at.slice(11,19);$('#stepHeader').textContent='업데이트 '+current.step+'회';$('#nationalVotes').innerHTML=votesHtml(n.votes,n.counted);
$('#clock').textContent=current.updated_at.replace('T',' ').slice(0,19)+' KST';$('#tickerText').textContent=`전국 개표율 ${pct(n.progress_pct)}%  |  현재 선두 ${n.leader}  |  모의 집계 ${fmt(n.counted)}표  |  전국 17개 시·도 / 254개 가상 선거구  |  공식 개표가 아닙니다.`;
$('#pauseBtn').textContent=current.running?'Ⅱ 일시정지':'▶ 자동 진행';
$('#regionTiles').innerHTML=current.regions.map(r=>`<button class="region-tile ${r.progress_pct>29?'hot':''}" data-region="${escapeHtml(r.id)}"><strong>${escapeHtml(r.id)}</strong><small>${pct(r.progress_pct)}% 집계</small></button>`).join('');
$('#regionRows').innerHTML=current.regions.map(r=>`<tr><td><span class="region-first">${escapeHtml(r.full_name)}</span></td><td>${r.districts}개</td><td><strong>${pct(r.progress_pct)}%</strong><span class="small-bar"><b style="width:${r.progress_pct}%"></b></span></td><td>${escapeHtml(r.leader)}</td><td>${fmt(r.lead_votes)}표</td><td><button data-region="${escapeHtml(r.id)}">상세 →</button></td></tr>`).join('');
$$('[data-region]').forEach(b=>b.onclick=()=>chooseRegion(b.dataset.region))}
function renderDistrictList(){if(!current)return;let q=$('#districtSearch').value.trim().toLowerCase();let all=current.districts.filter(d=>(!selectedRegion||d.region===selectedRegion)&&(!q||d.name.toLowerCase().includes(q)||d.id.toLowerCase().includes(q)));
$('#districtCountLabel').textContent=all.length+'개 선거구';$('#districtList').innerHTML=all.map(d=>`<button class="district-item ${d.id===selectedDistrict?'active':''}" data-district="${escapeHtml(d.id)}"><span class="left"><strong>${escapeHtml(d.name)}</strong><small>${fmt(d.counted)}표 집계</small></span><span class="right">${pct(d.progress_pct)}%<small>개표율</small></span></button>`).join('');
$$('[data-district]').forEach(b=>b.onclick=()=>chooseDistrict(b.dataset.district));}
function renderDistrict(){if(!current)return;let d=current.districts.find(x=>x.id===selectedDistrict);if(!d){d=current.districts[0];selectedDistrict=d.id}$('#districtTitle').textContent=d.name;$('#districtRegion').textContent=d.region+' · 가상 선거구';$('#districtProgress').textContent=pct(d.progress_pct)+'%';$('#districtTotal').textContent=fmt(d.counted);$('#districtBar').style.width=d.progress_pct+'%';$('#districtVotes').innerHTML=votesHtml(d.votes,d.counted)}
function renderStudio(){if(!current)return;let n=current.national;$('#cgTime').textContent='모의 기준 '+current.updated_at.slice(11,19);$('#cgPct').textContent='개표율 '+pct(n.progress_pct)+'%';$('#cgRanks').innerHTML=candidates.map((name,i)=>`<div class="cg-row"><span class="label">${name}</span><div class="b"><div style="background:${colors[i]};width:${n.counted?n.votes[i]/n.counted*100:0}%"></div></div><strong class="score">${pct(n.percentages[i])}%</strong></div>`).join('');
const lead=n.leader;$('#anchorScript').textContent=`교육용 모의 개표 상황입니다. 현재 전국 17개 시·도, 가상의 254개 선거구에서 모의 개표가 진행되고 있습니다. 전국 모의 개표율은 ${pct(n.progress_pct)}퍼센트입니다. 현재 ${lead}가 선두를 달리고 있으며, 2위 후보와는 ${fmt(n.lead_votes)}표 차이입니다. 수치는 실시간 난수 시뮬레이션으로, 실제 선거 결과와는 무관합니다.`}
function render(){summary();renderDistrictList();renderDistrict();renderStudio()}
function received(data){current=data;if($('#regionSelect').options.length===1){$('#regionSelect').innerHTML='<option value="">전국 전체</option>'+current.regions.map(r=>`<option value="${escapeHtml(r.id)}">${escapeHtml(r.full_name)}</option>`).join('');$('#regionSelect').value=selectedRegion}render()}
function connect(){const proto=location.protocol==='https:'?'wss:':'ws:';ws=new WebSocket(`${proto}//${location.host}/ws`);ws.onopen=()=>{$('#connectStatus').textContent='● WebSocket 연결됨';$('#connectStatus').style.color='#82e6c0'};ws.onmessage=e=>{try{const m=JSON.parse(e.data);if(m.type==='snapshot')received(m.data)}catch(err){console.warn(err)}};ws.onerror=()=>{$('#connectStatus').textContent='연결 오류'};ws.onclose=()=>{$('#connectStatus').textContent='재연결 중…';setTimeout(connect,1700)}}
async function control(action,extra={}){try{await request('/api/control',{method:'POST',body:JSON.stringify({action,...extra})});if(action==='reset'){article=null;$('#articleEmpty').classList.remove('hidden');$('#articleEditor').classList.add('hidden');toast('새로운 모의 개표가 시작됐습니다.')}else if(action==='speed')toast('갱신 주기를 변경했습니다.')}catch(e){toast(e.message)}}
async function draft(){try{let scope=$('#articleScope').value;let payload={scope,region:selectedRegion||'서울',district_id:selectedDistrict};article=await request('/api/articles/draft',{method:'POST',body:JSON.stringify(payload)});$('#articleEmpty').classList.add('hidden');$('#articleEditor').classList.remove('hidden');$('#articleId').textContent=article.id;$('#articleText').value=article.text;$('#articleStatus').textContent='검토 전 초안';$('#articleStatus').className='status-draft';showEvidence();validateDisplay(article.validation);refreshAudit();toast('초안 생성 완료. 근거 확인 후 승인하세요.')}catch(e){toast(e.message)}}
function showEvidence(){if(!article)return;let e=article.evidence;$('#evidenceDetails').innerHTML=[['근거 ID',e.id],['데이터 종류','교육용 합성 데이터'],['범위',e.label],['집계 단계',e.step+'회'],['기준 시각',e.updated_at.replace('T',' ').slice(0,19)],['누적 표수',fmt(e.data.counted)+'표'],['실제 선거 확인','아니요 · 모의 자료']].map(([a,b])=>`<div class="evidence-line"><span>${escapeHtml(a)}</span><strong>${escapeHtml(b)}</strong></div>`).join('')}
function validateDisplay(v){const box=$('#validationBox');box.classList.toggle('bad',!v.passed);box.textContent=v.passed?'✓ 형식·지역·수치·근거 ID 일치 — 사람의 최종 승인 필요':'⚠ 승인 차단: '+v.errors.join(' / ')}
async function checkArticle(){if(!article)return;const text=$('#articleText').value;const a=article.evidence;const original=article.text;const issues=[];if(!text.includes(a.id))issues.push('근거 ID 누락');if(!text.includes(a.label))issues.push('지역 누락');if(text!==original)issues.push('저장된 원문과 불일치');validateDisplay({passed:!issues.length,errors:issues});toast(issues.length?'수정으로 근거 불일치 가능성 발견':'원문 형식 검사 통과')}
async function approve(){if(!article)return;const reason=prompt('교육용 편집자 승인 사유를 입력하세요. (예: 원본 모의 개표값과 근거 ID 직접 대조)');if(reason===null)return;try{article=await request('/api/articles/'+encodeURIComponent(article.id)+'/review',{method:'POST',body:JSON.stringify({approve:true,editor:'실습 편집자',reason,revised_text:$('#articleText').value})});$('#articleStatus').textContent='사람 승인 완료';$('#articleStatus').className='status-draft status-approved';validateDisplay(article.validation);refreshAudit();toast('교육용 초안이 승인되었습니다. 공식 기사가 아닙니다.')}catch(e){toast('승인 불가: '+e.message);refreshAudit()}}
async function refreshAudit(){try{const a=await request('/api/audit');$('#auditList').innerHTML=a.length?a.map(x=>`<div class="audit-item"><div><strong>${escapeHtml(x.action)}</strong><span> · ${escapeHtml(x.article_id||'')}</span></div><span>${escapeHtml(x.at?.replace('T',' ').slice(0,19)||'')}</span></div>`).join(''):'<span class="muted">아직 기록이 없습니다.</span>'}catch{}}
$$('.nav').forEach(b=>b.addEventListener('click',()=>showView(b.dataset.view)));
$('#goDistrict').onclick=()=>showView('district');$('#allRegionsBtn').onclick=()=>chooseRegion('');$('#regionSelect').onchange=e=>{selectedRegion=e.target.value;renderDistrictList()};$('#districtSearch').oninput=renderDistrictList;
$('#pauseBtn').onclick=()=>control(current?.running?'pause':'resume');$('#tickBtn').onclick=()=>control('tick');$('#resetBtn').onclick=()=>{if(confirm('모의 개표를 초기화하고 기사와 검수 기록을 지울까요?'))control('reset')};$('#speed').onchange=e=>control('speed',{interval:Number(e.target.value)});
async function searchEvidence(){const q=$('#ragQuery').value.trim();if(!q)return toast('검색할 질문을 입력하세요.');try{const data=await request('/api/rag/search?question='+encodeURIComponent(q));$('#ragResults').innerHTML=data.results.length?data.results.map(x=>`<div class="rag-hit"><strong>[${escapeHtml(x.id)}] ${escapeHtml(x.title)}</strong><p>${escapeHtml(x.text)}</p><small>${escapeHtml(x.publisher)} · ${escapeHtml(x.published)} · 교육용 근거</small></div>`).join(''):'<span class="muted">제공된 문서에서 관련 근거를 찾지 못했습니다.</span>'; }catch(e){toast(e.message)}}
$('#ragButton').onclick=searchEvidence;$('#ragQuery').addEventListener('keydown',e=>{if(e.key==='Enter')searchEvidence()});
$('#makeDraft').onclick=draft;$('#draftDistrict').onclick=()=>{$('#articleScope').value='district';showView('articles');draft()};$('#checkArticle').onclick=checkArticle;$('#approveArticle').onclick=approve;$('#refreshAudit').onclick=refreshAudit;
$('#fullscreen').onclick=()=>{if(!document.fullscreenElement)document.documentElement.requestFullscreen?.();else document.exitFullscreen?.()};$('#fullscreenCG').onclick=()=>$('#cgScreen').requestFullscreen?.();$('#copyScript').onclick=async()=>{try{await navigator.clipboard.writeText($('#anchorScript').textContent);toast('대본을 복사했습니다.')}catch{toast('브라우저에서 복사를 허용하지 않았습니다.')}};
fetch('/api/snapshot').then(r=>r.json()).then(received).catch(()=>{});connect();
// V0.2 media display: only shipped assets + local-only preview, no upload endpoint.
let localMediaUrl=null;
async function loadMediaGallery(){
 try{
  const response=await fetch('/static/media/media_manifest.json',{cache:'no-store'});
  if(!response.ok)throw new Error('자료 원장 로드 실패');
  const items=await response.json();
  if(!Array.isArray(items))throw new Error('자료 원장 형식 오류');
  $('#mediaCount').textContent=items.length+'개 원본';
  $('#mediaGallery').innerHTML=items.filter(item=>item.kind!=='video').map(item=>{
   const src='/static/media/'+encodeURIComponent(item.filename);
   return `<article class="media-card"><img loading="lazy" src="${src}" alt="${escapeHtml(item.title)} · 교육용 가상 자료"/><div class="media-card-body"><h3>${escapeHtml(item.title)}</h3><small>${item.ai_generated?'AI 생성 이미지':'자체 제작 CG'}</small><p>${escapeHtml(item.caption)}<br/>출처: ${escapeHtml(item.source)}</p><a href="${src}" download>원본 이미지 내려받기</a></div></article>`;
  }).join('');
 }catch(err){ $('#mediaGallery').textContent='자료실을 표시하지 못했습니다: '+err.message;}
}
function clearLocalMedia(){if(localMediaUrl){URL.revokeObjectURL(localMediaUrl);localMediaUrl=null;}$('#mediaLocalPreview').replaceChildren();$('#mediaLocalFile').value='';}
$('#mediaLocalFile').addEventListener('change',event=>{
 const file=event.target.files[0];
 if(localMediaUrl){URL.revokeObjectURL(localMediaUrl);localMediaUrl=null;}
 $('#mediaLocalPreview').replaceChildren();
 if(!file)return;
 const allowed=['image/png','image/jpeg','image/webp','video/mp4','video/webm'];
 if(!allowed.includes(file.type)||file.size>100*1024*1024){toast('PNG/JPG/WebP/MP4/WebM, 100MB 이하 파일만 미리보기 가능합니다.');return;}
 localMediaUrl=URL.createObjectURL(file);
 const element=document.createElement(file.type.startsWith('video/')?'video':'img');
 if(element.tagName==='VIDEO'){element.controls=true;element.playsInline=true;}
 element.src=localMediaUrl;element.alt='사용자가 선택한 로컬 미리보기';
 $('#mediaLocalPreview').appendChild(element);
});
$('#mediaLocalClear').onclick=clearLocalMedia;
loadMediaGallery();
})();
