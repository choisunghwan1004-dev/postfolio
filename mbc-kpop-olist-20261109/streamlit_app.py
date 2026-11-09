"""Olist 포르투갈어 리뷰 감성분석 · 원본 토크나이저/딥러닝 모델 재사용.
원본 코드 근거: STEP2_Model_Serving/01_sentiment_demo_gradio.ipynb.
"""
from pathlib import Path
import pickle
import streamlit as st
import numpy as np

st.set_page_config(page_title='Olist 리뷰 감성 분석 | 데이터저널리즘 실습', page_icon='📊', layout='wide')
ROOT = Path(__file__).resolve().parent
MODEL_DIR = ROOT / 'model'
TOKENIZER = MODEL_DIR / 'part7_2_tokenizer.pkl'
KERAS = MODEL_DIR / 'part7_2_sentiment_model.keras'
MAX_LEN = 50  # 원본 STEP2 노트북 확인: padding='post', truncating='post'

st.title('📊 Olist 고객 리뷰 감성 분석')
st.caption('실습 과제 · 원본 07_2 토크나이저와 Keras 딥러닝 모델 사용 · 포르투갈어 입력 전용')
st.info('분석 결과는 별점 기반으로 학습한 모델의 추정 확률입니다. 품질 보증이나 사실 판정이 아닙니다.')

with st.expander('🔍 모델 정보·출처·주의사항', expanded=False):
    st.markdown('''- [원본 모델 저장소](https://github.com/journal-izm/Olist-Data-Analysis/tree/main/model)
- [학습·예측 방식 원본 노트북](https://github.com/journal-izm/Olist-Data-Analysis/blob/main/STEP2_Model_Serving/01_sentiment_demo_gradio.ipynb)
- 학습 대상은 포르투갈어 리뷰. 한국어/영어·새로운 도메인에서는 예측값을 신뢰하면 안 됩니다.
- `.pkl` 파일은 실행 가능한 역직렬화 형식입니다. **신뢰하는 출처에서만 다운로드하고 로드**하세요.
- 실행 중 외부 API 호출이나 사용자 리뷰의 자동 저장은 수행하지 않습니다.''')

st.subheader('1. 모델 파일 준비')
left,right=st.columns(2)
with left: st.write('토크나이저:', '✅ 확인' if TOKENIZER.is_file() else '❌ 미설치')
with right: st.write('Keras 딥러닝 모델:', '✅ 확인' if KERAS.is_file() else '❌ 미설치')
if not TOKENIZER.exists() or not KERAS.exists():
    st.warning('모델 파일 두 개를 이 프로젝트의 model/ 폴더에 넣어야 실제 추론할 수 있습니다. 아래 원본 링크에서 다운로드하세요.')
    st.markdown('''1. [part7_2_tokenizer.pkl](https://github.com/journal-izm/Olist-Data-Analysis/blob/main/model/part7_2_tokenizer.pkl) 다운로드
2. [part7_2_sentiment_model.keras](https://github.com/journal-izm/Olist-Data-Analysis/blob/main/model/part7_2_sentiment_model.keras) 다운로드
3. 실행 폴더의 `model/` 안에 **파일명 그대로** 저장하고 화면을 새로고침하세요.''')
    st.stop()

@st.cache_resource(show_spinner='딥러닝 모델 불러오는 중…')
def load_assets(tokenizer_path: str, keras_path: str):
    # 보안: 로컬에서 사용자 신뢰 검토 후 저장한 pkl만 사용.
    import tensorflow as tf
    with open(tokenizer_path,'rb') as f:
        tokenizer=pickle.load(f)
    model=tf.keras.models.load_model(keras_path,compile=False)
    return tokenizer,model

try:
    tokenizer,model=load_assets(str(TOKENIZER),str(KERAS))
except Exception as exc:
    st.error('모델 파일을 불러오지 못했습니다. Python·TensorFlow 버전과 파일 손상 여부를 확인하세요.')
    st.code(f'{type(exc).__name__}: {exc}')
    st.stop()

st.subheader('2. 포르투갈어 리뷰 입력')
examples={
    '상품이 매우 좋고 일찍 도착': 'produto muito bom, chegou antes do prazo',
    '아직 상품을 못 받음': 'ainda não recebi o produto',
    '상품이 깨져서 옴': 'produto veio quebrado, péssimo',
}
choice=st.selectbox('예제 선택',tuple(examples))
text=st.text_area('리뷰 입력 (포르투갈어)',value=examples[choice],height=115,max_chars=4000)
if st.button('감성 분석 실행',type='primary',use_container_width=True):
    if not text.strip(): st.warning('리뷰를 입력해 주세요.');st.stop()
    try:
        from tensorflow.keras.preprocessing.sequence import pad_sequences
        seq=tokenizer.texts_to_sequences([text])
        if not seq or not seq[0]:
            st.warning('학습 단어집에서 인식되는 단어가 없습니다. 결과를 출력하지 않습니다.')
            st.stop()
        arr=pad_sequences(seq,maxlen=MAX_LEN,padding='post',truncating='post')
        pred=model.predict(arr,verbose=0)
        p=float(np.asarray(pred).reshape(-1)[0])
        if not np.isfinite(p) or not 0<=p<=1: raise ValueError('모델 출력이 0~1 범위를 벗어났습니다.')
        a,b=st.columns(2)
        a.metric('예측 판정','긍정 😊' if p>=.5 else '부정 😞')
        b.metric('긍정 추정 확률',f'{p:.1%}')
        st.progress(p,text='긍정 추정 확률')
        st.caption(f'부정 추정 확률 {1-p:.1%} · 사용 단어 {len(seq[0])}개 / 최대 {MAX_LEN} 토큰 처리')
        st.markdown('**해석:** 확률은 모델의 분류 점수입니다. 개별 리뷰의 사실 여부나 배송 지연을 검증한 수치가 아닙니다.')
    except Exception as exc:
        st.error('분석 오류: 모델 입력 형태와 버전을 확인해 주세요.')
        st.code(f'{type(exc).__name__}: {exc}')

st.divider()
st.subheader('3. 실습에서 이미 만든 사실표 차트')
chart_names=[('01_배송과_리뷰.png','배송과 리뷰'),('02_감성분석_모델비교.png','감성분석 모델비교'),('03_지역별_주문비중.png','지역별 주문비중'),('04_판매자_유형.png','판매자 유형')]
for i in range(0,len(chart_names),2):
    cols=st.columns(2)
    for col,(fname,label) in zip(cols,chart_names[i:i+2]):
        image=ROOT/'charts'/fname
        with col:
            if image.exists():st.image(str(image),caption=label,use_container_width=True)
            else:st.caption(f'{fname} : 파일 없음')

st.caption('원본 데이터/코드: journal-izm/Olist-Data-Analysis · Olist 분석 사실표 F01~F35 · 과제용 별도 구현')


# 추가 실습: 실제 TensorFlow 모델을 예시 3문장에 실행합니다.
st.divider()
st.subheader('4. 감성분석 실제 예측 검증 (3문장)')
st.caption('예측 버튼을 누르면 위에 불러온 동일한 tokenizer/Keras 모델로 실제 추론합니다. 결과를 임의 생성하지 않습니다.')
if st.button('예시 3문장 실제 예측 테스트',type='secondary',use_container_width=True):
    cases = [
        ('긍정 예시','produto muito bom, chegou antes do prazo'),
        ('지연 예시','ainda não recebi o produto'),
        ('부정 예시','produto veio quebrado, péssimo'),
    ]
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    from datetime import datetime, timezone
    import pandas as pd
    result_rows=[]
    for description,review in cases:
        tokens=tokenizer.texts_to_sequences([review])
        if not tokens[0]:
            result_rows.append({'예제':description,'리뷰':review,'결과':'분류 보류(인식 토큰 0)','긍정 추정 확률':None,'인식 토큰 수':0})
            continue
        padded=pad_sequences(tokens,maxlen=MAX_LEN,padding='post',truncating='post')
        prediction=float(np.asarray(model.predict(padded,verbose=0)).reshape(-1)[0])
        if not np.isfinite(prediction) or not 0.0<=prediction<=1.0:
            st.error('비정상 출력: 확률 범위를 벗어났습니다.');st.stop()
        result_rows.append({'예제':description,'리뷰':review,'결과':'긍정' if prediction>=.5 else '부정',
                            '긍정 추정 확률':round(prediction,6),'인식 토큰 수':len(tokens[0])})
    st.dataframe(pd.DataFrame(result_rows),hide_index=True,use_container_width=True)
    payload=pd.DataFrame(result_rows).to_csv(index=False).encode('utf-8-sig')
    st.download_button('실제 예측 결과 CSV 저장',data=payload,file_name='olist_tensorflow_actual_predictions.csv',mime='text/csv')
    st.caption('검증에 사용한 파일은 화면 상단의 part7_2_tokenizer.pkl 및 part7_2_sentiment_model.keras입니다. 모델의 예측은 정답 검증이 아닙니다.')
