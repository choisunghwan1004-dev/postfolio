"""실제 Kworb 한국 Spotify 주간 TOP20 CSV -> PNG 3장.
출처: https://www.kworb.net/spotify/country/kr_weekly.html
주의: K-pop 전용 차트가 아닌 한국 Spotify 전체 주간 차트이며 원본 5곡 YouTube 비교가 아님.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parent
CSV = ROOT / "data" / "spotify_kr_weekly_2026-11-05_top20.csv"
OUT = ROOT / "charts"
AVAILABLE = {f.name for f in font_manager.fontManager.ttflist}
FONT = next((f for f in ["Malgun Gothic", "NanumGothic", "Noto Sans CJK KR", "AppleGothic"] if f in AVAILABLE), "DejaVu Sans")
plt.rcParams.update({"font.family": FONT, "axes.unicode_minus": False, "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False})
SOURCE = "Kworb · Spotify Weekly Chart South Korea · 2026-11-05 · TOP20"


def load_data():
    d = pd.read_csv(CSV).sort_values("rank")
    assert len(d) == 20 and d["rank"].is_unique
    assert set(d["rank"]) == set(range(1, 21))
    assert d["weekly_streams"].notna().all() and d["weekly_streams"].gt(0).all()
    assert d["chart_week_end"].nunique() == 1 and d["chart_week_end"].iloc[0] == "2026-11-05"
    d["previous_week"] = d["weekly_streams"] - d["weekly_streams_change"]
    valid = d["weekly_streams_change"].notna()
    assert d.loc[valid, "previous_week"].gt(0).all()
    d["wow_pct"] = np.where(valid, 100 * d["weekly_streams_change"] / d["previous_week"], np.nan)
    assert int(d["weekly_streams"].sum()) == 8380754, "Input/source snapshot has changed"
    return d


def save(fig, name):
    path = OUT / name
    fig.savefig(path, dpi=170, facecolor="white", bbox_inches="tight", pad_inches=.3)
    plt.close(fig)
    print("CREATED", path, path.stat().st_size)
    return path


def draw_spotify():
    d = load_data()
    OUT.mkdir(exist_ok=True)
    paths = []
    top = d.head(10).iloc[::-1]
    fig, ax = plt.subplots(figsize=(11, 7))
    labels = [f"{r.artist} · {str(r.song)[:22]}" for r in top.itertuples()]
    yy = np.arange(len(top))
    ax.barh(yy, top["weekly_streams"], color="#54a79b", height=.65)
    ax.set_yticks(yy, labels)
    ax.set_xlim(0, 1300000)
    ax.set_xlabel("주간 재생수 (회)")
    ax.set_title("05 | 한국 Spotify 주간 TOP10", loc="left", fontsize=17, pad=13)
    for i, value in enumerate(top["weekly_streams"]):
        ax.text(value + 8000, i, f"{value:,.0f}", va="center", fontsize=9)
    fig.subplots_adjust(left=.34, bottom=.21, top=.89)
    fig.text(.04, .13, "질문: 주간 재생수 1위는 누구인가?", fontsize=10)
    fig.text(.04, .09, "결과: A2O의 NEON은 1,078,815회로 1위.", fontsize=10)
    fig.text(.04, .04, SOURCE, fontsize=9, color="#667781")
    paths.append(save(fig, "05_Spotify_한국주간_상위10.png"))

    valid = d.dropna(subset=["wow_pct"]).copy()
    changes = valid.assign(abschange=valid["wow_pct"].abs()).nlargest(10, "abschange").sort_values("wow_pct")
    fig, ax = plt.subplots(figsize=(11, 7))
    yy = np.arange(len(changes))
    values = changes["wow_pct"].to_numpy()
    ax.barh(yy, values, color=np.where(values >= 0, "#54a79b", "#dc8b7a"), height=.65)
    ax.axvline(0, color="#667781", linewidth=1)
    ax.set_yticks(yy, [f"{r.artist} · {str(r.song)[:19]}" for r in changes.itertuples()])
    ax.set_xlim(-55, 162)
    ax.set_xlabel("전주 대비 주간 재생수 변화율 (%)")
    ax.set_title("06 | 전주 대비 변화율 · 절댓값 TOP10", loc="left", fontsize=17, pad=13)
    for i, value in enumerate(values):
        ax.text(value + (3 if value >= 0 else -3), i, f"{value:+.1f}%",
                va="center", ha="left" if value >= 0 else "right", fontsize=9)
    fig.subplots_adjust(left=.36, bottom=.22, top=.87)
    fig.text(.04, .14, "질문: 전주 대비 크게 늘고 줄어든 곡은?", fontsize=10)
    fig.text(.04, .10, "결과: ILLIT +147.15%, Jung Kook -37.89%; 신규 1곡 제외.", fontsize=10)
    fig.text(.04, .04, SOURCE + " · 비교 가능 19곡", fontsize=9, color="#667781")
    paths.append(save(fig, "06_Spotify_주간증감률.png"))

    total = int(d["weekly_streams"].sum())
    top5 = int(d.head(5)["weekly_streams"].sum())
    share = 100 * top5 / total
    fig, ax = plt.subplots(figsize=(10, 4.9))
    ax.barh([0], [top5], color="#54a79b", height=.45, label="상위 5곡")
    ax.barh([0], [total - top5], left=[top5], color="#9ac9d4", height=.45, label="6~20위")
    ax.set_yticks([])
    ax.set_xlim(0, total * 1.06)
    ax.set_xlabel("TOP20 주간 재생수 합계 (회)")
    ax.set_title("07 | Spotify TOP20 내부 집중도", loc="left", fontsize=17, pad=15)
    ax.text(top5 / 2, 0, f"{share:.2f}%\n{top5:,}회", ha="center", va="center", color="white", fontweight="bold")
    ax.text(top5 + (total - top5) / 2, 0, f"{100-share:.2f}%\n{total-top5:,}회", ha="center", va="center", fontweight="bold")
    ax.legend(loc="upper right", frameon=False)
    fig.subplots_adjust(left=.08, top=.79, bottom=.33)
    fig.text(.04, .20, "질문: 상위 5곡의 TOP20 내부 비중은?", fontsize=10)
    fig.text(.04, .15, f"결과: {top5:,}/{total:,} = {share:.2f}% (시장 점유율 아님).", fontsize=10)
    fig.text(.04, .07, SOURCE, fontsize=9, color="#667781")
    paths.append(save(fig, "07_Spotify_TOP20_집중도.png"))
    return paths


if __name__ == "__main__":
    draw_spotify()
