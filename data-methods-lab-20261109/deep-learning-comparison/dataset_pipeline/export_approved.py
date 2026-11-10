"""Export only human-reviewed rows; no AI generation and no remote calls."""
import argparse
import json
from pathlib import Path
import pandas as pd

INST = "보도자료를 읽고 사실을 추가하지 않은 기사 첫 문장(리드)을 한 문장으로 쓰세요."

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    df = pd.read_csv(args.input, dtype=str, encoding="utf-8-sig").fillna("")
    needed = ["본문", "리드", "승인", "검수자", "출처검증"]
    missing = [c for c in needed if c not in df.columns]
    if missing:
        raise SystemExit(f"열 누락: {missing}")
    approved = df[
        df["승인"].str.strip().str.upper().eq("Y")
        & df["검수자"].str.strip().ne("")
        & df["출처검증"].str.strip().str.upper().eq("Y")
        & df["리드"].str.strip().ne("")
        & df["본문"].str.strip().ne("")
    ].drop_duplicates(subset=["본문"])
    if approved.empty:
        raise SystemExit("승인된 데이터가 0건입니다. 사람의 사실·출처 검수 후 진행하세요.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        for _, row in approved.iterrows():
            obj = {"instruction": INST, "input": row["본문"], "output": row["리드"]}
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    print(f"검수 승인 JSONL: {len(approved)}쌍 -> {args.output}")
    if len(approved) < 100:
        print("참고: 강의 목표 100쌍에 미달합니다. 목표 달성을 주장하지 마세요.")

if __name__ == "__main__":
    main()
