"""Actual TensorFlow/Keras CPU inference; no mock outputs, results saved only after real model.predict()."""
from pathlib import Path
from datetime import datetime, timezone
import csv,json,pickle,hashlib,sys
ROOT=Path(__file__).resolve().parent
MODEL=ROOT/'model'/'part7_2_sentiment_model.keras'
TOKENIZER=ROOT/'model'/'part7_2_tokenizer.pkl'
if not MODEL.exists() or not TOKENIZER.exists():
    sys.exit('NOT VERIFIED: Required model files absent. Run 01_설치_모델다운로드.bat')
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
print('TensorFlow runtime version:',tf.__version__)
# These are pickle files from the course GitHub. Python pickle can execute code. Do not use untrusted files.
with TOKENIZER.open('rb') as f:tokenizer=pickle.load(f)
model=tf.keras.models.load_model(MODEL,compile=False)
assert len(model.inputs)==1 and len(model.outputs)==1,'Unexpected model signature'
examples=[
    ('긍정 예시','produto muito bom, chegou antes do prazo'),
    ('지연 예시','ainda não recebi o produto'),
    ('부정 예시','produto veio quebrado, péssimo'),
]
rows=[]
for tag,review in examples:
    sequences=tokenizer.texts_to_sequences([review])
    if not sequences or not sequences[0]:raise ValueError(f'No known tokens for: {review}')
    data=pad_sequences(sequences,maxlen=50,padding='post',truncating='post')
    probability=float(np.asarray(model.predict(data,verbose=0)).reshape(-1)[0])
    if not np.isfinite(probability) or not 0<=probability<=1:raise ValueError(f'Invalid probability: {probability}')
    rows.append({'예제':tag,'포르투갈어 리뷰':review,'판정':'긍정' if probability>=0.5 else '부정',
                 '긍정 확률':round(probability,8),'부정 확률':round(1-probability,8),'인식 토큰 수':len(sequences[0]),
                 'TensorFlow 버전':tf.__version__, 'Keras 모델 SHA256':hashlib.sha256(MODEL.read_bytes()).hexdigest(),
                 '토크나이저 SHA256':hashlib.sha256(TOKENIZER.read_bytes()).hexdigest(),
                 '실행 시각 UTC':datetime.now(timezone.utc).isoformat()})
    print(tag,':',review,'→',rows[-1]['판정'],'긍정 추정 확률',f'{probability:.6f}')
output=ROOT/'actual_prediction_results.csv'
with output.open('w',newline='',encoding='utf-8-sig') as f:
    writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
print('LIVE_MODEL_INFERENCE_PASS: TensorFlow model.predict called 3 times')
print('검증 결과:',output)
