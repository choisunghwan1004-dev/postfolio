"""Offline educational fact-grounded question answering baseline.

Not an embedding/vector RAG or LLM. Based on examples in the Olist RAG lesson.
Data are classroom examples, not independently verified production facts.
"""
import re

FACTS = {
    "F14": {"kind": "fact", "text": "교재 예시: 지연 도착 주문의 리뷰 점수는 2.57점"},
    "M09": {"kind": "model", "text": "교재 예시: 판매자 이탈 모델은 판매 기록에서 만든 특징 14개를 사용"},
    "R06": {"kind": "policy", "text": "수업용 가상 규정 예시: 3일 이상 지연 시 배송비 환불"},
}
CHANNELS = {"A": {"fact"}, "B": {"fact", "model"}, "C": {"fact", "model", "policy"}}
FALLBACK = "제공된 자료로는 확인할 수 없습니다."

def retrieve(question, channel="A"):
    """Only explicit classroom example intents; avoid open-ended guesswork."""
    if channel not in CHANNELS:
        raise ValueError("채널은 A/B/C 중 하나여야 합니다.")
    q = question.replace(" ", "")
    if ("리뷰" in q or "평점" in q) and ("늦" in q or "지연" in q):
        key = "F14"
    elif "이탈" in q and ("모델" in q or "입력" in q or "특징" in q):
        key = "M09"
    elif ("배송" in q or "도착" in q) and ("지연" in q or "늦" in q) and ("환불" in q or "보상" in q or "3일" in q):
        key = "R06"
    else:
        return {}
    item = FACTS[key]
    return {key: item} if item["kind"] in CHANNELS[channel] else {}

def validate_citations(answer, retrieved_ids):
    cited = set(re.findall(r"\[([FMR]\d{2})\]", answer))
    return bool(cited) and cited.issubset(set(retrieved_ids))

def answer(question, channel="A"):
    docs = retrieve(question, channel)
    if not docs:
        return FALLBACK, []
    evidence_id, item = next(iter(docs.items()))
    response = item["text"] + f" [{evidence_id}]"
    if not validate_citations(response, docs.keys()):
        return FALLBACK, []
    return response, [evidence_id]

if __name__ == "__main__":
    questions = [
        "늦게 도착한 주문의 리뷰 점수는?",
        "이탈 모델의 입력 특징은?",
        "배송이 3일 지연되면 어떤 보상을 받아?",
        "2019년 매출은 얼마야?",
    ]
    for q in questions:
        for channel in "ABC":
            result, ids = answer(q, channel)
            print(f"{channel} | {q} => {result} | 검색 근거 {ids}")
