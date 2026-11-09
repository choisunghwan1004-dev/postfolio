"""GitHub 공개 원본 Keras/Tokenizer 파일 다운로드 + 실제 크기 검증. 모델 pkl은 신뢰하는 출처에서만 로드하세요."""
from pathlib import Path
from urllib.request import Request, urlopen
from tempfile import NamedTemporaryFile
import os, shutil, sys, hashlib
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'model'; OUT.mkdir(exist_ok=True)
MODELS=[('part7_2_tokenizer.pkl',474308),('part7_2_sentiment_model.keras',2601637)]
for name,expected in MODELS:
    dest=OUT/name
    if dest.is_file() and dest.stat().st_size==expected:
        print('[OK] 원본 크기 일치',name,expected);continue
    url=f'https://raw.githubusercontent.com/journal-izm/Olist-Data-Analysis/main/model/{name}'
    print('다운로드:',url)
    temp=OUT/(name+'.partial')
    try:
        with urlopen(Request(url,headers={'User-Agent':'Olist-classroom-verification/1.0'}),timeout=45) as response, temp.open('wb') as f:
            shutil.copyfileobj(response,f)
        received=temp.stat().st_size
        if received!=expected:raise ValueError(f'크기 불일치! 기대 {expected}바이트 / 실제 {received}바이트')
        temp.replace(dest)
        print('[OK]',name,received,'SHA256',hashlib.sha256(dest.read_bytes()).hexdigest())
    except Exception as exc:
        temp.unlink(missing_ok=True)
        print('[ERROR]',type(exc).__name__,str(exc))
        print('직접 다운로드: '+url)
        sys.exit(2)
print('모델 두 파일 다운로드·크기 검증 완료. 모델의 실행 검증은 별도 테스트합니다.')
