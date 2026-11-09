"""Advanced statistics for *synthetic* existing class data, not causal evidence."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, entropy as shannon_entropy

DEFAULT_DATA = Path(__file__).resolve().parent.parent / "data-methods-lab-20261109" / "data" / "sports_center_members_demo.csv"
DEFAULT_OUT = Path(__file__).resolve().parent / "results.json"
SEED = 20261109
N_REPETITIONS = 10_000

def clean_data(source: Path) -> tuple[pd.DataFrame, dict]:
    raw = pd.read_csv(source)
    required = {"member_id", "program", "district", "visits_per_month", "satisfaction_1to5"}
    if not required.issubset(raw.columns):
        raise ValueError(f"Missing required columns: {sorted(required - set(raw.columns))}")
    dupes = int(raw.duplicated(subset="member_id").sum())
    df = raw.drop_duplicates(subset="member_id").copy()
    invalid = int(df["visits_per_month"].lt(0).sum())
    df.loc[df["visits_per_month"].lt(0), "visits_per_month"] = np.nan
    missing = {c: int(df[c].isna().sum()) for c in ["visits_per_month", "satisfaction_1to5"]}
    for col in ["visits_per_month", "satisfaction_1to5"]:
        df[col] = df[col].fillna(df[col].median())
    if df[["program", "district"]].isna().any().any():
        raise ValueError("Unresolved missing categorical values")
    if not set(df["program"]) == {"A", "B"}:
        raise ValueError("Expected the two class demonstration programs A and B")
    return df, {"raw_rows": len(raw), "duplicate_ids": dupes, "invalid_negative_visits": invalid,
                "imputed_missing_before_fill": missing, "clean_rows": len(df)}

def benjamini_hochberg(p_values: dict[str, float]) -> dict[str, float]:
    ordered = sorted(p_values, key=p_values.get)
    m = len(ordered)
    adjusted = {}
    running = 1.0
    for rank in range(m, 0, -1):
        key = ordered[rank - 1]
        running = min(running, p_values[key] * m / rank)
        adjusted[key] = float(running)
    return adjusted

def analyze(source: Path, repetitions: int = N_REPETITIONS, seed: int = SEED) -> dict:
    if repetitions < 100:
        raise ValueError("repetitions must be >= 100")
    df, cleaning = clean_data(source)
    rng = np.random.default_rng(seed)
    av = df.loc[df.program == "A", "visits_per_month"].to_numpy(dtype=float)
    bv = df.loc[df.program == "B", "visits_per_month"].to_numpy(dtype=float)
    observed = float(bv.mean() - av.mean())
    a_idx = rng.integers(0, len(av), size=(repetitions, len(av)))
    b_idx = rng.integers(0, len(bv), size=(repetitions, len(bv)))
    boot = bv[b_idx].mean(axis=1) - av[a_idx].mean(axis=1)
    ci = np.quantile(boot, [0.025, 0.975]).tolist()
    combined = np.concatenate([av, bv])
    ge = 0
    for _ in range(repetitions):
        shuffled = rng.permutation(combined)
        diff = float(shuffled[len(av):].mean() - shuffled[:len(av)].mean())
        ge += abs(diff) >= abs(observed) - 1e-12
    permutation_p = (ge + 1) / (repetitions + 1)
    table = pd.crosstab(df.program, df.district)
    chi2, chi_p, dof, expected = chi2_contingency(table, correction=False)
    chi_valid = bool((expected >= 5).all())
    district_counts = df.district.value_counts().sort_index()
    h = float(shannon_entropy(district_counts.to_numpy(), base=2))
    hmax = float(np.log2(len(district_counts)))
    bayes, probabilities = {}, {}
    for name, segment in df.groupby("program"):
        successes = int(segment.satisfaction_1to5.ge(4).sum())
        n = int(len(segment))
        bayes[str(name)] = {"successes": successes, "n": n,
                            "empirical_rate": round(successes / n, 6),
                            "beta_prior": [1, 1], "beta_posterior": [1 + successes, 1 + n - successes],
                            "posterior_mean": round((successes + 1) / (n + 2), 6)}
        probabilities[str(name)] = successes / n
    q1, q3 = np.quantile(df.visits_per_month, [0.25, 0.75])
    iqr = float(q3 - q1)
    lower, upper = float(q1 - 1.5 * iqr), float(q3 + 1.5 * iqr)
    flagged = df.loc[~df.visits_per_month.between(lower, upper), "member_id"].astype(str).tolist()
    raw_p = {"permutation_visit_difference": float(permutation_p),
             "chi_square_program_district": float(chi_p)}
    adj_p = benjamini_hochberg(raw_p)
    def rnd(v: float) -> float:
        return round(float(v), 6)
    return {
        "data_kind": "교육용 가상 데이터 (실제 회원·운영 통계 아님)",
        "source_csv": "../data-methods-lab-20261109/data/sports_center_members_demo.csv",
        "random_seed": seed, "repetitions": repetitions,
        "cleaning": cleaning,
        "group_visit_mean": {"A": rnd(av.mean()), "B": rnd(bv.mean())},
        "bootstrap_difference_B_minus_A": {"observed": rnd(observed), "percentile_95_interval": [rnd(v) for v in ci]},
        "permutation_two_sided": {"p_value": rnd(permutation_p), "exceedances": ge,
                                  "p_formula": "(extreme_count+1)/(repetitions+1)"},
        "chi_square_program_vs_district": {"statistic": rnd(chi2), "p_value": rnd(chi_p),
                                           "degrees_of_freedom": int(dof),
                                           "min_expected_count": rnd(expected.min()),
                                           "expected_all_at_least_5": chi_valid,
                                           "interpretation": "Only use asymptotic p-value if expected-count assumption is acceptable"},
        "district_entropy": {"counts": {str(k): int(v) for k, v in district_counts.items()},
                             "entropy_bits": rnd(h), "max_bits": rnd(hmax),
                             "normalized": rnd(h / hmax) if hmax else None},
        "conditional_probability_satisfied_given_program": {k: rnd(v) for k, v in probabilities.items()},
        "bayesian_beta_binomial": bayes,
        "iqr_outlier_flags": {"lower": rnd(lower), "upper": rnd(upper), "flagged_member_ids": flagged,
                              "note": "Exploratory flag, not grounds to delete observations"},
        "multiple_comparisons_BH": {"raw_p": {k: rnd(v) for k, v in raw_p.items()},
                                    "adjusted_p": {k: rnd(v) for k, v in adj_p.items()}, "m": len(raw_p)},
        "limitations": ["수업용 가상 자료", "프로그램 배정이 무작위가 아니므로 인과관계 불가",
                        "순서가 시간축이 아니므로 자기상관·시계열 모델 적용하지 않음",
                        "기계학습 예측 성능은 이 분석에서 평가하지 않음",
                        "결측 대치의 영향과 다중검정·모델 가정 검토 필요"]
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--repetitions", type=int, default=N_REPETITIONS)
    args = parser.parse_args()
    report = analyze(args.data, repetitions=args.repetitions)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"ADVANCED_ANALYSIS_PASS: {args.output}")
    print(f"B-A = {report['bootstrap_difference_B_minus_A']['observed']}")
    print(f"Permutation p = {report['permutation_two_sided']['p_value']}")
    print(f"Chi-square assumption met = {report['chi_square_program_vs_district']['expected_all_at_least_5']}")

if __name__ == "__main__":
    main()
