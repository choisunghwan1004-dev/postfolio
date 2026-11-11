"""Standalone Streamlit UI. Does not change existing Olist dashboard or SHAI UI."""
from __future__ import annotations
import os
from pathlib import Path
import streamlit as st
from utils.rag import build_documents,create_store,create_chain,answer_question,NOT_FOUND

st.set_page_config(page_title='Olist 근거 Q&A · 학습',page_icon='📚',layout='wide')
st.title('Olist 분석 Q&A — LangChain RAG')
st.caption('수업용 별도 검증 UI. 규정 PDF는 가상 교육용 자료입니다. 답에 인용된 ID가 실제 숫자 검산을 대신하지는 않습니다.')
channel=st.radio('검색할 근거 범위', ['A','B','C'],horizontal=True,format_func=lambda x:{'A':'A 사실표','B':'B + 모델 설명서','C':'C + 가상 규정집'}[x])
folder=st.text_input('자료 폴더', value=os.getenv('OLIST_RAG_DATA_DIR',str(Path(__file__).resolve().parents[1]/'data')))
key=st.text_input('OpenAI API Key (화면 세션에만 입력)',type='password',value='')
model=st.text_input('LLM 모델 ID',value='gpt-5.4-mini')
question=st.text_input('질문',value='늦게 도착한 주문의 리뷰 점수는?')
k=st.slider('검색 조각 수 k',1,10,4)
@st.cache_resource(show_spinner='근거 검색 인덱스 구성 중…')
def cached_index(data_folder: str, ch: str, private_key: str):
    return create_store(build_documents(Path(data_folder),ch),private_key)
if st.button('근거 검색 후 답하기',type='primary'):
    if not key.strip():
        st.warning('API 키가 필요합니다. 키는 GitHub/로그에 저장하지 마세요.')
    else:
        try:
            with st.spinner('검색 및 답변 생성 중…'):
                store=cached_index(folder,channel,key)
                result=answer_question(question,channel,store,create_chain(key,model),k)
            st.subheader('답변')
            st.write(result['answer'])
            st.caption('검증 상태: '+result['status'])
            with st.expander('찾아온 근거 ID'):
                st.write(result['found_ids'])
            if result['status'].startswith('blocked'):
                st.error('근거 ID 검증 실패: 해당 답변을 차단했습니다.')
        except Exception as exc:
            st.error('실행 실패: '+str(exc))
