"""Recalculate 5th-assessment facts from a locally supplied air_quality_long.csv.
No AI/API or network required. Never claim results before local execution.
"""
from pathlib import Path
import argparse
import json
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, required=True, help="Local original air_quality_long.csv")
    parser.add_argument("--out", type=Path, default=Path("results/facts.json"))
    args = parser.parse_args()
    if not args.csv.is_file():
        parser.error(f"CSV file does not exist: {args.csv}")
    try:
        df = pd.read_csv(args.csv)
    except UnicodeDecodeError as exc:
        raise SystemExit("인코딩 오류: 원본 파일의 인코딩을 확인하세요.") from exc
    required = {"city", "country", "date.utc", "location", "parameter", "value", "unit"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise SystemExit(f"필수 열 누락: {missing}. 실제 CSV 헤더 확인.")
    pm = df[df["parameter"].eq("pm25")]
    london = pm[pm["city"].eq("London")]
    facts = {
        "status": "computed_from_local_csv",
        "source_filename": args.csv.name,
        "F-1": {"rows": int(len(df)), "columns": int(len(df.columns))},
        "missing_by_column": {k: int(v) for k, v in df.isna().sum().items()},
        "F-2": {"pm25_observations": int(len(pm))},
        "F-3": {
            "london_pm25_observations": int(len(london)),
            "london_pm25_mean": round(float(pd.to_numeric(london["value"], errors="coerce").mean()), 2),
            "london_pm25_median": round(float(pd.to_numeric(london["value"], errors="coerce").median()), 2),
            "unit": "µg/m³",
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(facts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(facts, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
