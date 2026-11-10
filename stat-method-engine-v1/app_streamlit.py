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
