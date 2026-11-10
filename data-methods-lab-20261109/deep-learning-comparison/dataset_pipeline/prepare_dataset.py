"""Local-only preparer. Never fetches the network or generates unreviewed 'ground truth'."""
import argparse
import json
import re
from pathlib import Path
import pandas as pd

COLUMNS = ["제목", "본문"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output-dir", default="output", type=Path)
    args = ap.parse_args()

    df = pd.read_csv(args.input, dtype=str, encoding="utf-8-sig")
    missing = [c for c in COLUMNS if c not in df.columns]
    if missing:
        raise SystemExit(f"필수 열 누락: {missing}. 필요 열: {COLUMNS}")
    initial = len(df)
    df = df[COLUMNS].copy()
    for col in COLUMNS:
        df[col] = df[col].fillna("").map(lambda x: re.sub(r"\s+", " ", x).strip())
    df = df[(df["제목"] != "") & (df["본문"] != "")]
    nonempty = len(df)
    df = df.drop_duplicates(subset=["본문"])
    unique = len(df)
    df = df[df["본문"].str.len().between(200, 2500)]
    df = df.reset_index(drop=True)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output_dir / "press_clean.csv", index=False, encoding="utf-8-sig")
    review = df.assign(리드="", 승인="", 검수자="", 검수일="", 출처검증="")
    review.to_csv(args.output_dir / "review_queue.csv", index=False, encoding="utf-8-sig")

    audit = {
        "status": "unreviewed", "initial": initial, "nonempty": nonempty,
        "unique_body": unique, "kept_200_to_2500_chars": len(df),
        "excluded_total": initial - len(df), "approved": 0,
        "note": "All input assumed locally provided with rights verified separately. No network activity.",
    }
    (args.output_dir / "audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(audit, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
