"""Optional PC/mobile browser UI. Run with streamlit when separately installed.
Read-only local files; do not host publicly without access control.
"""
from pathlib import Path
import streamlit as st
from engine import GOALS, inspect_csv, advise

st.set_page_config(page_title='통계기법 AI V1',layout='wide')
st.title('통계기법 AI — 데이터 조건 추천 엔진')
st.caption('실제 추천 기능 · 데이터 표본 진단 / 분석 실행 및 분산 학습은 단계별 검증')
with st.sidebar:
    st.header('1. 데이터와 장치 조건')
    filepath=st.text_input('로컬 CSV 파일 경로',value=str(Path(__file__).parent/'examples'/'sample_air.csv'))
    encoding=st.selectbox('문자 인코딩',['utf-8-sig','cp949','utf-8','euc-kr'])
    ram=st.number_input('RAM(GB)',min_value=1.0,max_value=2048.0,value=8.0,step=1.0)
    distributed=st.checkbox('클러스터/분산 환경 보유')
    gpu=st.checkbox('GPU 보유·사용 가능')
    pandas_familiar=st.checkbox('pandas 문법을 유지하고 싶음',value=True)
    st.header('2. 원하는 분석')
    goal=st.selectbox('목적',list(GOALS),format_func=lambda k:GOALS[k])
    run=st.button('데이터 조건 검사·추천',type='primary')
if run:
    try:
        profile=inspect_csv(Path(filepath),encoding=encoding)
        report=advise(profile,goal,ram,distributed,pandas_familiar,gpu)
        st.success('추천 생성 완료 (분산 모델 실행·학습을 뜻하지 않음)')
        m1,m2,m3=st.columns(3)
        m1.metric('표본 검사',f"{profile['sampled_rows']}행")
        m2.metric('파일 크기',f"{profile['size_bytes']/1024/1024:.2f} MB")
        m3.metric('추천 실행 기반',report['backend']['recommended'])
        st.subheader('데이터 표본 열 정보')
        st.dataframe(profile['columns'],use_container_width=True)
        st.subheader('추천 통계 기법과 조건')
        for item in report['method_candidates']:
            with st.expander(item['name'],expanded=True):
                st.write('예시:',item['example']);st.write('필수 조건:',item['required']);st.warning('검증 주의: '+item['caution'])
        st.subheader('실행 기반 선택 이유')
        for reason in report['backend']['reasons']:st.write('•',reason)
        st.subheader('분석 전 확인 질문')
        for i,q in enumerate(report['questions_to_confirm'],1):st.write(f'{i}. {q}')
        for w in report['warnings']:st.warning(w)
        st.download_button('추천 결과 JSON 저장',data=__import__('json').dumps(report,ensure_ascii=False,indent=2),file_name='recommendation.json',mime='application/json')
    except Exception as err:
        st.error(f'자료 조건 검사를 수행하지 못했습니다: {type(err).__name__}: {err}')
else:
    st.info('왼쪽에서 CSV 경로·분석 목적·장치 조건을 선택한 뒤 실행하세요. 원본 파일은 덮어쓰지 않습니다.')
    st.markdown('**기법 예시:** 종로구 PM10 날짜별 변화 → 시계열 / 지역 비교 → Welch 검정(조건 확인) / 기사 수 vs PM10 → 상관(인과 아님) / 대용량 집계 → Dask 또는 Polars / GPU 분산 학습 → Ray / 클러스터 ML Pipeline → PySpark')

# V1.2 additive panel. All V1.1 widgets/state and previous controls remain unchanged.
st.divider()
st.header('3. 조건을 바꾸며 기법 비교하기 (V1.2)')
st.caption('데이터 필터·기간·값 범위·분석 기법을 바꾸고 여러 실행 결과를 비교합니다. 64MiB 이하 CSV에서만 pandas로 실제 계산합니다.')
from dataclasses import asdict
import json
from scenario_engine import METHODS_V12, Scenario, recommend_methods, run_scenario

if 'scenario_comparisons' not in st.session_state:
    st.session_state.scenario_comparisons=[]
try:
    profile_v12=inspect_csv(Path(filepath),encoding=encoding)
    colnames=[c['column'] for c in profile_v12['columns']]
    numeric_cols=[c['column'] for c in profile_v12['columns'] if c['inferred_type']=='numeric']
    date_cols=[c['column'] for c in profile_v12['columns'] if c['date_name_hint']]
    with st.expander('기법별 조건·예시 확인',expanded=False):
        st.dataframe(recommend_methods(profile_v12['columns'],goal=goal),use_container_width=True)
    with st.form('scenario_v12_form'):
        sc_name=st.text_input('조건 이름',value='기본 조건')
        method=st.selectbox('기법 선택',list(METHODS_V12),format_func=lambda x:METHODS_V12[x]['name'])
        left,right=st.columns(2)
        with left:
            value=st.selectbox('분석 수치 열',numeric_cols or colnames)
            second=st.selectbox('두 번째 수치 열(상관분석)', ['선택 안 함']+[x for x in numeric_cols if x!=value])
            group=st.selectbox('집단 열', ['선택 안 함']+colnames)
            datecol=st.selectbox('날짜 열', ['선택 안 함']+date_cols+[x for x in colnames if x not in date_cols])
        with right:
            filtercol=st.selectbox('필터 열', ['선택 안 함']+colnames)
            filterequals=st.text_input('필터가 일치할 값 (비우면 적용 안 함)')
            datefrom=st.text_input('시작 날짜(YYYY-MM-DD, 선택)',value='')
            dateto=st.text_input('끝 날짜(YYYY-MM-DD, 선택)',value='')
            mintext=st.text_input('수치 최소값(선택)',value='')
            maxtext=st.text_input('수치 최대값(선택)',value='')
            window=st.slider('이동평균 창 크기',2,30,7)
        submitted=st.form_submit_button('이 조건·기법으로 다시 계산',type='primary')
    if submitted:
        try:
            scenario=Scenario(name=sc_name.strip() or '조건',method=method,value_col=value,
                second_col=None if second=='선택 안 함' else second,
                group_col=None if group=='선택 안 함' else group,
                date_col=None if datecol=='선택 안 함' else datecol,
                filter_col=None if filtercol=='선택 안 함' else filtercol,
                filter_equals=filterequals if filterequals else None,
                start_date=datefrom or None,end_date=dateto or None,
                min_value=float(mintext) if mintext.strip() else None,
                max_value=float(maxtext) if maxtext.strip() else None,window=window)
            record=run_scenario(Path(filepath),scenario,encoding=encoding)
            st.session_state.scenario_comparisons.append(record)
            st.session_state.scenario_comparisons=st.session_state.scenario_comparisons[-12:]
            st.success('실제 집계 완료 · 비교 목록에 추가')
        except Exception as exc:
            st.error(f'조건을 다시 확인하세요: {type(exc).__name__}: {exc}')
    if st.session_state.scenario_comparisons:
        st.subheader('조건·기법별 실행 비교')
        rows=[]
        for item in st.session_state.scenario_comparisons:
            r=item['result'];s=item['scenario']
            rows.append({'조건':s['name'],'기법':METHODS_V12[s['method']]['name'],'선택 후 행 수':item['filtered_rows'],
                         '평균':r.get('mean'), '중앙값':r.get('median'),'Pearson':r.get('pearson'),
                         '시계열 점 수':len(r.get('series',[])),'그룹 수':len(r.get('groups',[]))})
        st.dataframe(rows,use_container_width=True)
        st.download_button('실행 결과 모두 JSON 저장',data=json.dumps(st.session_state.scenario_comparisons,ensure_ascii=False,indent=2,allow_nan=False),file_name='scenario_comparisons.json',mime='application/json')
        if st.button('비교 기록 지우기'):
            st.session_state.scenario_comparisons=[]
            st.rerun()
except Exception as exc:
    st.warning(f'조건 실험 화면 자료 읽기 대기: {type(exc).__name__}: {exc}')
